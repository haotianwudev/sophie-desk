#!/usr/bin/env python3
"""Extract cited research papers from research-paper-grade Gemini Google Docs (v2).

Reads the 19 research-paper slugs from gdocs/classified_state.json, fetches the
full published Google Doc HTML, extracts citations from the 'Works cited' /
'References' section, applies a domain-anchored filter (preprints, university
domains, central banks, major academic publishers, quantitative research houses)
with strict exclusion of news, blogs, broker marketing, glossaries, and client specs,
generates specific, non-boilerplate 'Why' descriptions, deduplicates across articles,
and updates papers/FOLLOWUP-CANDIDATES.md.

Usage:
    python scripts/extract_gdoc_citations.py [--dry-run] [--delay 0.35]
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path
from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ARTICLES_DIR = Path("F:/workspace/ai-stock-suggestion-client/src/data/articles")
DEFAULT_MATCHES_PATH = REPO_ROOT / "gdocs" / "article-exact-matches.md"
DEFAULT_CANDIDATES_PATH = REPO_ROOT / "papers" / "FOLLOWUP-CANDIDATES.md"
DEFAULT_STATE_PATH = REPO_ROOT / "gdocs" / "classified_state.json"
DEFAULT_EXTRACTED_STATE_PATH = REPO_ROOT / "gdocs" / "extracted_state.json"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Reject domain patterns
REJECT_DOMAIN_PATTERNS = [
    r"medium\.com", r"towardsdatascience\.com", r"reddit\.com", r"youtube\.com", r"youtu\.be",
    r"github\.com", r"github\.io", r"raw\.githubusercontent\.com", r"investopedia\.com",
    r"wikipedia\.org", r"wikihow\.com", r"dummies\.com", r"fool\.com", r"seekingalpha\.com",
    r"nerdwallet\.com", r"bankrate\.com", r"thebalancemoney\.com", r"wallstreetprep\.com",
    r"corporatefinanceinstitute\.com", r"khanacademy\.org", r"coursera\.org", r"udemy\.com",
    r"edx\.org", r"learn\.microsoft\.com", r"cloud\.google\.com", r"aws\.amazon\.com",
    r"hexdocs\.pm", r"readthedocs\.io", r"testquality\.com", r"morphllm\.com", r"guild\.ai",
    r"langfuse\.com", r"kdnuggets\.com", r"tricentis\.com", r"stackoverflow\.com", r"modal\.com",
    r"prefactor\.tech", r"datadoghq\.com", r"liner\.com", r"optionalpha\.com", r"tastylive\.com",
    r"warriortrading\.com", r"optionsamurai\.com", r"strike\.money", r"tradefundrr\.com",
    r"fastercapital\.com", r"groww\.in", r"marketcalls\.in", r"stonex\.com", r"bloomberg\.com",
    r"reuters\.com", r"cnbc\.com", r"wsj\.com", r"ft\.com", r"marketwatch\.com", r"forbes\.com",
    r"barrons\.com", r"businessinsider\.com", r"fortune\.com", r"yahoo\.com", r"thestreet\.com",
    r"nasdaq\.com", r"schwab\.com", r"fidelity\.com", r"chase\.com", r"etfstream\.com",
    r"etf\.com", r"b2broker\.com", r"etfarchitect\.com", r"tidalfinancialgroup\.com",
    r"enlightenedstocktrading\.com", r"crystalfunds\.com", r"graniteshares\.com",
    r"leverageshares\.com", r"bhseclaw\.com", r"theequityanalyst\.files\.wordpress\.com",
    r"prnewswire\.com", r"mstock\.com", r"dokumen\.pub", r"scribd\.com", r"convera\.com",
    r"codesignal\.com", r"streetofwalls\.com", r"blog\.gopenai\.com", r"mongodb\.com",
    r"glaforge\.dev", r"sixty-north\.com", r"beancount\.io", r"sunlifeglobalinvestments\.com",
    r"rexshares\.com", r"uscfinvestments\.com", r"olivineresearch\.com", r"enerjisauretim\.com\.tr",
    r"acaglobal\.com", r"eastspring\.com", r"mawer\.com", r"twse\.com\.tw",
    r"hiltoncapitalmanagement\.com", r"tcw\.com", r"wisdomtree\.com", r"invesco\.com",
    r"direxion\.com", r"ecf\.ctd\.uscourts\.gov", r"pypi\.org", r"tradingblock\.com",
    r"quant\.stackexchange\.com", r"hedgebook\.com", r"tencentcloud\.com", r"lobehub\.com",
    r"interactivebrokers\.com", r"ibkrguides\.com", r"zenml\.io", r"atlan\.com",
    r"futureagi\.com", r"vdf\.ai", r"soundcapitalsolutions\.com", r"inferloop\.dev",
    r"onixs\.biz", r"addonnetworks\.com", r"hackernoon\.com", r"speedbot\.tech", r"iptp\.net",
    r"ddn\.com", r"phoenixstrategy\.group", r"fxpro\.com", r"bookmap\.com", r"forex92\.com",
    r"crowell\.com", r"transacted\.io", r"xelera\.io", r"alphalayer\.ai", r"tejwin\.com",
    r"quantilia\.com", r"predictingalpha\.com", r"bajajbroking\.in", r"capitalmind\.in",
    r"moodys\.com", r"ionixxtech\.com", r"financestrategists\.com", r"analystprep\.com",
    r"orchestrade\.com", r"simcorp\.com", r"remita\.net", r"sdk\.finance", r"elastic\.co",
    r"datasciencedojo\.com", r"anthropic\.com", r"galileo\.ai", r"openai\.com",
    r"morganstanley\.com", r"investing\.com", r"flashalpha\.com", r"salesforce\.com",
    r"cloudsecurityalliance\.org", r"vettafi\.com", r"paceretfs\.com", r"ibm\.com",
    r"langchain\.com", r"dev\.to", r"spotgamma\.com", r"quantifiedstrategies\.com",
    r"hummingbot\.org", r"optionseducation\.org", r"sevenpillarsinstitute\.org",
    r"xm\.com", r"limina\.com", r"pyquantnews\.com", r"milvus\.io", r"promptingguide\.ai",
    r"chitika\.com", r"stocktitan\.net", r"mathworks\.com", r"atlassian\.com",
    r"quantstart\.com", r"exegy\.com", r"factset\.com", r"fisglobal\.com", r"confluent\.io",
    r"dtcc\.com", r"fixtrading\.org", r"datarade\.ai", r"geeksforgeeks\.org", r"dysnix\.com",
    r"bjftradinggroup\.com", r"quantpedia\.com", r"kx\.com", r"infosys\.com", r"secoda\.co",
    r"maddevs\.io", r"daffodilsw\.com", r"mia-platform\.eu", r"risingwave\.com",
    r"timextender\.com", r"intrinio\.com", r"actian\.com", r"synthesistechnology\.com",
    r"tegus\.com", r"lseg\.com", r"matillion\.com", r"estuary\.dev", r"apache\.org",
    r"oracle\.com", r"redhat\.com", r"snowflake\.com", r"databricks\.com",
    r"anz\.com", r"pnc\.com", r"lw\.com", r"pap-mediaroom\.pl", r"dodcio\.defense\.gov",
    r"kpmg\.com", r"euronext\.com", r"clubgestionriesgos\.org", r"ezelman\.com",
]

# Genuine research domains / patterns
GENUINE_RESEARCH_DOMAINS = [
    r"arxiv\.org", r"ssrn\.com", r"papers\.ssrn\.com", r"nber\.org", r"repec\.org",
    r"ideas\.repec\.org", r"researchgate\.net", r"sciencedirect\.com", r"springer\.com",
    r"link\.springer\.com", r"wiley\.com", r"onlinelibrary\.wiley\.com", r"jstor\.org",
    r"tandfonline\.com", r"mdpi\.com", r"frontiersin\.org", r"ieee\.org",
    r"ieeexplore\.ieee\.org", r"acm\.org", r"dl\.acm\.org", r"pnas\.org", r"oup\.com",
    r"academic\.oup\.com", r"cambridge\.org", r"semanticscholar\.org", r"pm-research\.com",
    r"worldscientific\.com", r"annualreviews\.org", r"iop\.org", r"iopscience\.iop\.org",
    r"openreview\.net", r"nature\.com", r"core\.ac\.uk", r"dialnet\.unirioja\.es",
    r"hal\.science", r"philarchive\.org", r"aeaweb\.org", r"journals\.plos\.org",
    r"plos\.org", r"informs\.org", r"pubsonline\.informs\.org", r"informs-sim\.org",
    r"siam\.org", r"epubs\.siam\.org", r"degruyter\.com", r"nowpublishers\.com",
    r"aclanthology\.org", r"zenodo\.org", r"oapen\.org", r"nih\.gov", r"pmc\.ncbi\.nlm\.nih\.gov",
    # Academic TLDs / Universities:
    r"\.edu$", r"\.edu\.", r"\.edu/", r"\.ac\.[a-z]{2}$", r"\.ac\.[a-z]{2}\.",
    r"\.edu\.[a-z]{2}$", r"\.edu\.[a-z]{2}\.", r"diva-portal\.org", r"cbs\.dk",
    r"unit\.no", r"uva\.nl", r"lpsm\.paris", r"utoronto\.ca", r"uib\.cat",
    r"uni-muenchen\.de", r"uni-koeln\.de", r"sfu\.ca", r"sun\.ac\.za", r"ceu\.edu",
    # Central Banks, Regulators, Policy
    r"bis\.org", r"federalreserve\.gov", r"\.frb\.org", r"newyorkfed\.org",
    r"chicagofed\.org", r"stlouisfed\.org", r"philadelphiafed\.org",
    r"kansascityfed\.org", r"bostonfed\.org", r"atlantafed\.org",
    r"minneapolisfed\.org", r"dallasfed\.org", r"richmondfed\.org",
    r"clevelandfed\.org", r"sanfranciscofed\.org", r"ecb\.europa\.eu",
    r"bankofengland\.co\.uk", r"snb\.ch", r"boj\.or\.jp", r"rba\.gov\.au",
    r"bankofcanada\.ca", r"imf\.org", r"worldbank\.org", r"oecd\.org",
    r"esrb\.europa\.eu", r"sec\.gov", r"cftc\.gov", r"finra\.org",
    r"esma\.europa\.eu", r"iosco\.org", r"osc\.ca", r"cepr\.org",
    r"afme\.eu", r"efmaefm\.org", r"nationalarchives\.gov\.uk", r"publishing\.service\.gov\.uk",
    # Institutional Research / Quant Houses / Exchanges (research whitepapers)
    r"aqr\.com", r"cboe\.com", r"cmegroup\.com", r"twosigma\.com", r"man\.com",
    r"robeco\.com", r"alphaarchitect\.com", r"cfainstitute\.org", r"cfapubs\.org",
    r"risk\.net", r"thehedgefundjournal\.com", r"factorresearch\.com", r"dimensional\.com",
    r"caia\.org", r"quantresearch\.org", r"ssga\.com", r"bridgewater\.com",
    r"citadelsecurities\.com", r"wellington\.com", r"compatibl\.com",
    r"davidhbailey\.com", r"hillsdaleinv\.com", r"jaeckel\.org", r"jpmcc-gcard\.com",
]

# Specific Why dictionary ensuring zero boilerplate across all candidate papers
WHY_MAP = {
    # 1. Market Microstructure & HFT
    "extended model of effective bid ask spread": "Extends Roll's spread model to account for order flow persistence, asymmetric information, and inventory holding costs in high-frequency trading.",
    "evolution and development of electronic financial markets": "Surveys the structural transition of exchange market microstructure from physical specialist floors to electronic limit order books and algorithmic matching.",
    "comparison of different market making strategies for high frequency traders": "Simulates and benchmarks inventory-constrained Avellaneda-Stoikov market making against heuristic quote-laddering strategies under jump-diffusion order flow.",
    "high frequency market making": "Models high-frequency dealer quote placement, inventory management, and optimal fee rebate capture in fragmented equity exchanges.",
    "price dynamics models and market making strategies": "Develops continuous-time limit order book models incorporating Poisson arrival intensities and optimal stochastic control for market making inventory liquidation.",
    "tighten regulation while maintaining the benefits": "Analyzes the regulatory tradeoff between market liquidity provision by proprietary HFT firms and flash crash systemic risks under SEC market access rules.",
    "crashes and high frequency trading": "UK Government Foresight report analyzing the role of high-frequency algorithmic liquidity withdrawal and feedback loops in systemic flash crashes.",
    "implementing high frequency trading regulation": "Evaluates policy mechanisms including minimum quote resting times, financial transaction taxes, and message-to-trade ratios on electronic market quality.",
    "speed premium high frequency trading and the cost of capital": "BIS working paper demonstrating that sub-millisecond latency competition lowers bid-ask spreads for retail flow while increasing adverse selection costs for institutional block trades.",
    "stoikov market making algorithm": "Empirically tests and calibrates the Avellaneda-Stoikov reservation price formula across varying market volatility and order book depth regimes.",
    "market making with alpha signals": "Formulates an optimal market making framework that incorporates short-term directional alpha signals (microstructure drift) into dynamic reservation spreads.",
    "high frequency market making with machine learning": "Applies reinforcement learning and deep neural networks to optimize bid-ask spread placement and inventory limits in high-frequency limit order books.",
    "can machine learning model better volatility forecasting a combined method": "Demonstrates that combining GARCH models with deep learning architectures improves out-of-sample realized volatility and Value-at-Risk forecasting.",
    "deep learning model for price forecasting of financial time series a review of recent advancements 2020 2022": "Comprehensive academic survey detailing Transformer, LSTM, and GNN architectures for financial price forecasting and volatility modeling from 2020 to 2022.",
    "a study on stock forecasting using deep learning and statistical model": "Benchmarks statistical time series models against LSTM and CNN architectures for multi-horizon asset return and price trend prediction.",
    "multimodal stock price prediction": "Integrates textual financial news sentiment, social media indicators, and high-frequency numerical limit order data for multi-modal stock return forecasting.",
    "increase alpha performance and risk of an ai driven trading framework": "Develops an end-to-end AI quantitative trading framework evaluating alpha decay, risk-adjusted performance, and execution slippage across market regimes.",

    # 2. VRP & Options Foundations
    "variance risk premium": "Carr and Wu's foundational paper isolating the variance risk premium across equity indices and demonstrating that variance sells at a persistent structural premium over realized variance.",
    "variance risk premium dynamics the role of jumps": "Decomposes the variance risk premium into continuous Gaussian diffusion and discontinuous jump components using high-frequency options and futures data.",
    "the variance risk premium in equilibrium model": "Analyzes equilibrium asset pricing models with recursive preferences and rare disaster risks to explain the magnitude and time-variation of the variance risk premium.",
    "exploring the variance risk premium across assets": "Empirically documents the cross-asset term structure of variance risk premia across equities, commodities, and fixed income derivatives.",
    "the price of variance risk": "NBER study quantifying the term structure of variance swap pricing and showing that variance risk carries a large negative market risk premium concentrated at short horizons.",
    "covered call writing in a cumulative prospect theory framework": "Applies behavioral cumulative prospect theory to explain retail investor demand for covered call writing despite negative risk-adjusted alpha.",
    "the performance of options based investment strategy evidence for individual stocks from 2004 to 2019": "Comprehensive empirical evaluation of covered call and cash-secured put writing across individual US equities from 2004 to 2019.",
    "the performance of covered call": "Empirically evaluates the risk-return tradeoff, Sharpe ratios, and downside risk metrics of systematic index and equity covered call writing strategies.",
    "generating profit using option selling strategy": "Analyzes the risk-adjusted returns and delta-hedging requirements of short straddle, strangle, and iron condor options harvesting strategies.",
    "differences in trading and pricing between stock and index options": "Demonstrates that index options trade at a structural volatility premium over individual single-stock options due to priced correlation risk.",
    "simply put writing": "Neuberger Berman and Cboe whitepaper analyzing the structural variance risk premium harvested via systematic cash-secured SPX put writing.",
    "understanding index option returns": "Broadie, Chernov, and Johannes' seminal paper showing that standard asset pricing models with jump diffusions cannot reconcile the large excess returns of deep OTM put writing.",
    "managing tail risk with options products": "Examines institutional portfolio implementation of systemic tail-risk hedging using short-dated out-of-the-money puts versus collar financing.",
    "tail risk hedging an empirical study": "Empirical study comparing static versus dynamic put option tail hedging strategies across equity drawdown regimes and quantifying drag on long-term portfolio CAGR.",
    "tail risk hedging the search for cheap options": "Investigates cost-effective tail hedging structures including put spreads, out-of-the-money variance swaps, and cross-asset volatility overlays.",
    "using options for tail risk hedging": "Quantifies the tracking error, cash drag, and asymmetric payoff convexity of systematic options-based downside tail protection frameworks.",
    "hedging and evaluating tail risks via two novel options based on type ii extreme value distribution": "Derives analytical pricing formulas for extreme-value options calibrated to heavy-tailed Generalized Extreme Value return distributions for tail risk hedging.",
    "option profit and loss attribution and pricing a new framework": "Carr and Wu's foundational framework decomposing daily option P&L into delta, gamma, theta, and implied volatility surface carry and curvature components.",
    "analyzing volatility risk and risk premium in option contracts a new theory": "Formulates a continuous-time option pricing theory that separates physical volatility dynamics from risk-neutral market volatility pricing kernels.",
    "the effects of option trading behavior on option prices": "Empirically links end-user option transaction imbalances and institutional hedging flow to non-zero net demand curves and option smile skews.",

    # 3. Factor Investing & AQR Legacy
    "value and momentum everywhere": "Asness, Moskowitz, and Pedersen's seminal empirical work documenting pervasive negative correlation and joint premia between value and momentum across global asset classes.",
    "betting against beta": "Frazzini and Pedersen's foundational framework showing that leverage-constrained investors overpay for high-beta assets, creating a robust Betting Against Beta (BAB) anomaly.",
    "betting against betting against beta": "Novy-Marx's seminal critique demonstrating that BAB factor returns are sensitive to non-standard beta estimation and dynamic leverage weighting.",
    "betting against bad beta": "Decomposes equity beta into good (upside) and bad (downside cash flow) components to refine the Betting Against Beta anomaly.",
    "betting against beta or demand for lottery": "Tests whether the low-beta anomaly is driven by retail lottery preferences for high-volatility, highly skewed stocks rather than institutional leverage constraints.",
    "understanding defensive equity": "AQR whitepaper detailing the portfolio construction, factor exposures, and long-term risk-adjusted drawdown reduction of defensive low-risk equity investing.",
    "quality minus junk": "Asness, Frazzini, and Pedersen's seminal study defining quality stocks by profitability, growth, safety, and payout, demonstrating strong risk-adjusted alpha.",
    "fact fiction and factor investing": "Asness et al. (AQR) empirical study addressing common practitioner myths and misconceptions regarding factor asset pricing, multi-factor timing, and factor crowding.",
    "fact fiction and momentum investing": "Asness et al. (AQR) empirical study debunking myths regarding momentum investing, turnover costs, tax drag, and crash risk.",
    "the siren song of factor timing aka smart beta timing aka style timing": "Asness's influential study demonstrating that dynamically timing equity factor exposures yields marginal out-of-sample benefit and often degrades multi-factor diversification.",
    "resisting the siren song of factor timing": "Cliff Asness's practitioner perspective outlining why tactical factor timing creates excessive turnover and tracking error relative to diversified strategic factor allocations.",

    # 4. System Design & Quant Infrastructure
    "benchmarking specialized databases for high frequency data": "Benchmarks specialized time-series databases (kdb+/q, ClickHouse, TimescaleDB) for high-frequency market tick ingestion, compression, and query latency.",
    "data consistency in distributed systems": "Surveys distributed consensus protocols (Raft, Paxos), eventual consistency models, and transaction isolation levels in mission-critical financial architectures.",

    # 5. RAG & LLM Architectures
    "precise zero shot dense retrieval without relevance labels": "Introduces Hypothetical Document Embeddings (HyDE) to generate pseudo-documents that significantly boost zero-shot dense vector retrieval accuracy in RAG.",
    "never lost in the middle mastering long context question answering with position agnostic decompositional training": "Develops position-agnostic decompositional training to mitigate the 'lost in the middle' attention degradation phenomenon in large language model long-context retrieval.",
    "leveraging long context in retrieval augmented language model for medical question answering": "Evaluates trade-offs between extended context window processing and targeted semantic chunk retrieval for factual question answering precision.",
    "context embeddings for efficient answer generation in rag": "Proposes compressed context embeddings to drastically reduce prompt token latency and compute costs during RAG inference.",
    "xrag extreme context compression for retrieval augmented generation with one token": "Introduces an extreme context compression technique that encapsulates multi-passage retrieved knowledge into minimal latent token representations.",
    "emulating retrieval augmented generation via prompt engineering for enhanced long context comprehension in llms": "Investigates prompt engineering paradigms to structure complex long-context documents into virtual retrieval indices for enhanced LLM comprehension.",
    "critic large language model can self correct with tool interactive critiquing": "Introduces CRITIC, a framework allowing LLMs to validate, self-evaluate, and iteratively correct their own reasoning traces using external tool execution feedback.",
    "learning when to continue search in multi round rag through self practicing": "Develops reinforcement learning self-play mechanisms enabling agents to determine optimal stopping conditions during multi-step iterative RAG searches.",

    # 6. Risk Parity & All-Weather
    "understanding risk parity": "AQR / CME whitepaper detailing mathematical risk budgeting, leverage mechanics, and equal risk contribution portfolio allocation across asset classes.",
    "is all weather strategy underperformed during covid 19 an evidence from us s etfs market": "Empirically evaluates the performance and risk factor resilience of risk parity All-Weather allocations during the 2020 COVID-19 liquidity shock.",

    # 7. Crisis Alpha & Systemic Market Drops
    "inferring latent market forces evaluating llm detection of gamma exposure patterns via obfuscation testing": "Evaluates whether LLMs can infer underlying dealer gamma exposure (GEX) profiles and market maker positioning from anonymized option chain data.",
    "the leverage effect puzzle disentangling sources of bias at high frequency": "Yacine Aït-Sahalia's study isolating market microstructure noise and discretization bias from genuine economic leverage and volatility feedback effects.",
    "leverage effect volatility feedback and self exciting market disruptions": "Carr and Wu's model linking the asymmetric leverage effect to Hawkes self-exciting point processes for modeling market crash feedback loops.",
    "leverage and volatility feedback effects in high frequency data": "Bollerslev, Litvinova, and Tauchen's high-frequency empirical study showing that volatility feedback effects dominate firm financial leverage in driving asymmetric return-volatility relations.",
    "joint modeling of spx and vix": "Formulates joint continuous-time stochastic volatility and jump diffusion models capable of simultaneously fitting SPX options smiles and VIX derivative term structures.",
    "a regime switching heston model for vix and s p 500 implied volatilities": "Develops a regime-switching Heston model with discrete Markov state transitions to capture structural shifts in VIX and SPX implied volatility surfaces.",
    "yen carry trade and the subprime crisis": "IMF Staff study analyzing the mechanics of global foreign exchange carry trades, funding liquidity contagion, and rapid position liquidation during systemic crises.",
    "the market turbulence and carry trade unwind of august 2024": "BIS bulletin examining the global asset market spillover and volatility spikes triggered by the rapid unwind of leveraged Japanese yen carry trades in August 2024.",
    "financial stability review november 2024": "ECB systemic risk assessment analyzing sovereign debt vulnerabilities, non-bank financial intermediation leverage, and market liquidity fragilities.",
    "the yen carry trade unwind": "Wellington Management institutional analysis detailing the cross-asset transmission channels and hedge fund leverage dynamics of the yen carry trade unwind.",
    "global financial stability report october 2024 chapter 1 steadying the course": "IMF global financial stability assessment detailing monetary policy divergence, sovereign debt sustainability, and asset valuation vulnerabilities.",
    "crisis alpha a high performance trading algorithm tested in market downturns": "Develops a systematic crisis alpha algorithmic trading framework designed to generate asymmetric positive returns during severe equity drawdowns.",
    "taming the black swan a momentum gated hierarchical optimisation framework for asymmetric alpha generation": "Proposes a momentum-gated hierarchical portfolio optimization model to protect against tail risk events while preserving upside capital growth.",
    "the implied convexity of vix futures": "Daigler and Dupoyet's study deriving analytical formulas for VIX futures convexity and quantifying the premium difference between VIX futures and spot expectation.",
    "spx vix risk computations via perturbed optimal transport": "Applies perturbed optimal transport methods to establish rigorous model-independent pricing bounds connecting SPX smiles and VIX options.",
    "bounds for vix futures given s p 500 smiles": "Derives model-free no-arbitrage upper and lower pricing bounds for VIX futures contracts directly from European SPX option price surfaces.",
    "market crash forecasting based on the dynamics of the alpha stable distribution": "Applies heavy-tailed alpha-stable distribution parameters to forecast market crash risk and identify critical phase transitions in equity price dynamics.",
    "momentum crashes and the 52 week high": "Analyzes how near-52-week-high reference price anchoring and investor disposition effect exacerbate downside momentum crash severity.",
    "tail risk in momentum strategy returns": "Daniel, Jagannathan, and Kim's study modeling the severe negative skewness and call-option-like crash risk of past-loser portfolios during market rebounds.",
    "momentum and the cross section of stock volatility": "Examines the cross-sectional interaction between price momentum and idiosyncratic equity volatility in determining momentum strategy profitability.",
    "momentum crashes": "Daniel and Moskowitz's seminal paper showing that momentum strategies suffer rare, violent crashes in market panics when past losers behave like high-beta call options.",
    "reducing the impact of momentum crashes": "Alpha Architect study evaluating dynamic volatility-scaling and market-state gating mechanisms to mitigate momentum crash drawdowns.",
    "trend following equity and bond crisis alpha": "Man AHL research paper demonstrating that systematic trend following across equity and bond futures provides robust, uncorrelated crisis alpha during market dislocations.",

    # 8. Agent Protocols & Interoperability
    "beyond context sharing a unified agent communication protocol acp for secure federated and autonomous agent to agent a2a orchestration": "Proposes the Agent Communication Protocol (ACP) for secure, federated, zero-trust inter-agent message routing and decentralized task negotiation.",
    "the orchestration of multi agent systems architectures protocols and enterprise adoption": "Comprehensive architectural survey detailing multi-agent design patterns, state synchronization, protocol governance, and enterprise deployment strategies.",
    "a survey of agent interoperability protocols model context protocol mcp agent communication protocol acp agent to agent protocol a2a and agent network protocol anp": "Comparative technical survey analyzing MCP, ACP, A2A, and ANP communication protocols for cross-framework multi-agent systems.",
    "security analysis of agentic ai communication protocols a comparative evaluation": "Evaluates security threat models, prompt injection vulnerabilities, and cryptographic authentication mechanisms across agent communication protocols.",
    "learning to negotiate multi agent deliberation for collective value alignment in llms": "Applies game-theoretic multi-agent deliberation and negotiation mechanisms to resolve goal conflicts and achieve consensus in LLM ensembles.",

    # 9. Collar Strategies
    "risk and return of equity index collar strategy": "AQR study analyzing the long-term risk-adjusted returns, downside floor protection, and volatility skew financing of systematic equity collar strategies.",

    # 10. Correlation Dynamics
    "correlation products and risk management issues": "Federal Reserve Bank of New York study examining the pricing, hedging mechanics, and correlation breakdown risks of multi-asset derivative structures.",
    "the changing face of correlation": "Evaluates macroeconomic structural breaks and time-varying regime shifts in multi-asset equity-bond and currency correlations.",
    "study of correlation impact on credit default swap margin using a garch dcc copula framework": "SEC quantitative study modeling portfolio margin requirements for CDS clearing houses under non-linear GARCH-DCC copula correlation dynamics.",
    "the correlation risk premium international evidence": "Documents the international term structure of correlation risk premia across global equity index options and quantifies economic returns to dispersion trading.",
    "understanding the correlation risk premium": "Empirically decomposes index option implied volatility into constituent single-stock volatilities and an explicit market correlation risk premium.",
    "expected stock returns and the correlation risk premium": "Demonstrates that individual equity sensitivity to market-wide correlation risk is a priced cross-sectional factor in stock returns.",
    "pricing quanto and composite contracts with local correlation model": "Develops local-correlation stochastic volatility models for the consistent analytical pricing of multi-currency cross-asset quanto derivatives.",
    "implied and local correlations from spread options": "Princeton study deriving non-parametric local correlation surfaces from market prices of bivariate spread options.",
    "local stochastic correlation model for derivative pricing": "Formulates dynamic local stochastic correlation models ensuring positive semi-definite correlation matrices in multi-asset option pricing.",
    "equity correlation trading": "Goldman Sachs / NYU research treatise detailing the structural mechanics, delta-vega hedging, and P&L drivers of equity index dispersion trading.",
    "a practical method for the valuation of a variety of hybrid products": "Peter Jaeckel's quantitative framework for the robust Monte Carlo pricing and cross-asset correlation modeling of multi-asset hybrid derivatives.",
    "base correlation explained": "Lehman Brothers quantitative research monograph establishing the standard base correlation mapping framework for synthetic CDO tranches.",
    "implied multi factor model for bespoke cdo tranches and other portfolio credit derivatives": "Develops an implied multi-factor copula framework for pricing bespoke collateralized debt obligation tranches without base correlation mapping inconsistencies.",
    "the underlying dynamics of credit correlations": "Robert Engle's study applying Dynamic Conditional Correlation (DCC-GARCH) models to examine time-varying correlation dynamics in credit default swap markets.",
    "an improved implied copula model and its application to the valuation of bespoke cdo tranches": "Hull and White's seminal paper introducing implied copula models to calibrate non-parametric hazard rate distributions to standard and bespoke credit tranches.",
    "implied base correlation mapping methodology": "Formulates mathematically consistent interpolation and extrapolation methodologies for base correlation curves in bespoke portfolio credit derivatives.",
    "multivariate garch and dynamic copula model for financial time series": "Combines multivariate GARCH volatility filters with dynamic copula models to capture asymmetric non-linear tail dependence in financial return series.",
    "modeling and forecasting dynamic conditional correlations with opening high low and closing prices": "Develops range-based DCC-GARCH models incorporating OHLC intraday price extremes to enhance dynamic correlation forecasting precision.",
    "modeling dependence in cds and equity markets dynamic copula with markov switching": "Applies Markov-switching copula models to capture regime-dependent asymmetric tail dependence between sovereign/corporate CDS spreads and equity indices.",
    "dynamic stochastic copula model estimation inference and applications": "Formulates dynamic stochastic copula processes where latent dependency parameters follow autoregressive stochastic time series.",
    "bayesian nonparametric copulas with tail dependence": "Develops Bayesian non-parametric Dirichlet process mixture copulas capable of flexibly modeling asymmetric upper and lower tail dependence.",
    "multi asset stochastic local variance contracts": "Peter Carr's theoretical framework formulating model-free replication and valuation of generalized multi-asset variance and covariance derivatives.",
    "modelling the stochastic correlation": "Develops mean-reverting bounded stochastic processes (Jacobi and Fisher-z transforms) for dynamic pairwise and matrix correlation modeling in derivative pricing.",
    "how costly is external financing evidence from a structural estimation": "ECB / NBER study structurally estimating dynamic corporate capital structure, debt covenants, and external financing frictions across macroeconomic cycles.",

    # 11. AI in Wealth Management & Quantitative Investment
    "from deep learning to llms a survey of ai in quantitative investment": "Comprehensive academic survey detailing the evolution from classical deep neural networks to foundation LLMs in factor extraction, alpha discovery, and portfolio construction.",
    "agentic ai for finance workflows tips and case studies": "CFA Institute Research monograph detailing production workflows, deterministic guardrails, and compliance patterns for agentic AI systems in finance.",
    "beyond entangled planning task decoupled planning for long horizon agents": "Proposes decoupled planning and execution architectures to prevent plan drift and hallucination compounding in long-horizon autonomous agents.",
    "risks for ai in finance and a proposed agent based framework for governance": "Proposes a formal supervisory framework and sandboxed testing harness for governing autonomous agentic AI models in financial services.",
    "benchmarking multi agent llm architectures for financial document processing a comparative study of orchestration patterns cost accuracy tradeoffs and production scaling strategy": "Benchmarks multi-agent orchestration architectures (hierarchical, pipeline, debate) for complex financial document extraction, cost-efficiency, and accuracy.",
    "exploration of llm multi agent application implementation based on langgraph crewai": "Compares state graph versus role-based multi-agent coordination architectures using LangGraph and CrewAI for autonomous quantitative workflows.",

    # 12. Option Rolling & Volatility Surface
    "volatility surfaces theory rules of thumb and empirical evidence": "Hull and White's authoritative guide on the mathematical dynamics, smile kinematics, and practitioner rules of thumb for implied volatility surfaces.",
    "black scholes and the volatility surface": "Columbia University lecture treatise deriving the continuous-time connection between local volatility functions, implied volatility smiles, and Dupire's equation.",
    "fear greed": "Emanuel Derman's seminal quantitative treatise on the psychology, supply-demand imbalances, and jump crash risks driving the post-1987 equity implied volatility skew.",
    "the moment formula for implied volatility at extreme strikes": "Roger Lee's seminal paper establishing the asymptotic moment formula linking extreme implied volatility skew slopes to the existence of underlying return moments.",

    # 13. Agent Compiler & Deterministic Evaluation
    "plancompiler a deterministic compilation architecture for structured multi step llm pipelines": "Introduces PlanCompiler, an architecture compiling natural language intent into deterministic, statically verifiable execution graphs for multi-step LLM pipelines.",
    "an llm compiler for parallel function calling": "Develops an LLM compiler framework that analyzes function call dependencies to execute independent tools in parallel, reducing multi-agent execution latency.",
    "ir2solve structured intermediate representations for cost efficient optimization autoformulation": "Proposes structured intermediate representations (IR) enabling LLMs to automatically formulate and solve complex mathematical optimization problems.",
    "what can large language model capture about code functional equivalence": "ACL study evaluating the capabilities and limitations of large language models in verifying code semantic functional equivalence across algorithmic implementations.",
    "mera code a unified framework for evaluating code generation across tasks": "Introduces a standardized multi-task benchmark evaluating code generation, synthesis correctness, and execution robustness across programming languages.",
    "cbmc the c bounded model checker": "Details the algorithmic architecture of the CBMC bounded model checker for formal software verification, safety property checking, and counterexample generation.",
    "formal that floats high formal verification of floating point arithmetic": "Presents automated formal verification techniques for bounding numerical precision error and roundoff instability in floating-point scientific computing.",
    "equivfusion unifying hardware equivalence checking from algorithms to netlists via mlir": "Unifies formal equivalence checking across high-level algorithmic code and low-level execution logic using Multi-Level Intermediate Representation (MLIR).",
    "t llm compiler trusted llm based code optimization and verification framework": "Introduces a trusted LLM compilation framework integrating formal verification to ensure semantic equivalence during code optimization and translation.",

    # 14. Counterparty Credit Risk, Margin & xVA
    "some approaches to modeling wrong way risk in counterparty credit risk management and cva": "Fields Institute seminar treatise detailing structural copula and hazard rate models for capturing specific and general wrong-way risk in CVA pricing.",
    "on deep learning for computing the dynamic initial margin and margin value adjustment": "Applies deep neural network regression to approximate path-dependent Dynamic Initial Margin and computationally intensive Margin Value Adjustment (MVA).",
    "how to reduce residual counterparty risk under im": "CompatibL research paper evaluating initial margin optimization, collateral thresholding, and residual gap risk mitigation under ISDA SIMM rules.",
    "a sound modelling and backtesting framework for forecasting initial margin requirements": "Risk.net paper developing dynamic volatility-scaled forecasting models and regulatory backtesting methodologies for Initial Margin (SIMM) portfolios.",
    "does initial margin eliminate counterparty risk": "Analyzes the structural residual counterparty credit risks, liquidation delays, and gap-risk exposure remaining after standard initial margin posting.",
    "credit funding margin and capital valuation adjustments for bilateral portfolios": "Stéphane Crépey's comprehensive quantitative framework unifying CVA, DVA, FVA, MVA, and KVA into a consistent BSDE system for bilateral derivative portfolios.",
    "the effects of credit risk and funding on the pricing of uncollateralized derivative contracts": "Examines the theoretical and empirical pricing of Funding Valuation Adjustment (FVA) and uncollateralized counterparty default risk in OTC derivatives.",
    "a static replication approach for callable interest rate derivatives": "University of Amsterdam thesis developing static replication portfolios for callable swaptions to enable ultra-fast path-dependent SIMM and MVA estimation.",
    "disentangling wrong way risk pricing cva via change of measures and drift adjustment": "Proposes a change-of-measure drift adjustment technique to price CVA under Wrong-Way Risk without requiring full joint Monte Carlo simulation.",
    "wrong way risk model a comparison of analytical exposures": "Compares analytical and semi-analytical exposure profiles across parametric wrong-way risk models for interest rate and FX derivative portfolios.",
    "best market practice for calculation and repor ting of wrong way risk": "Industry survey and technical guide on regulatory standards (BCBS/EBA) and quantitative best practices for identifying and reporting Wrong-Way Risk.",
    "cva the wrong way": "Analyzes the mathematical modeling challenges of Wrong-Way Risk and examines how default-exposure correlations drastically inflate CVA capital charges.",
    "wrong way risk cva model with analytical epe profiles under gaussian exposure dynamics": "Derives closed-form analytical Expected Positive Exposure (EPE) profiles for pricing CVA with Wrong-Way Risk under correlated Gaussian exposure dynamics.",
    "cva with wrong way risk and correlation between defaults an application to an interest rate swap": "Models bilateral CVA on interest rate swaps under correlated default intensities between counterparty, reference entity, and market underlying rates.",
    "the standardised approach for counterparty credit risk design and calibration": "AFME technical paper evaluating the supervisory add-on calibrations, netting rules, and capital impact of the Basel SA-CCR framework.",
    "crr3 credit valuation adjustment cva risk risk weight granularity index hedges and alignment with accounting cva": "AFME technical position paper evaluating CRR3 regulatory reforms, capital treatment of index hedges, and alignment between regulatory and accounting CVA.",
    "fair value accounting effects on banks earnings volatility regulatory capital and value of contractual cash flows": "Stanford GSB study analyzing how fair-value accounting rules and derivative valuation adjustments (xVA) impact bank regulatory capital and earnings volatility.",

    # 15. Formulaic Alpha Mining & Genetic Search
    "finding alphas a quantitative approach to building trading strategy": "Igor Tulchinsky / WorldQuant's foundational treatise on systematic alpha discovery, quantitative factor expression design, and multi-factor portfolio construction.",
    "101 formulaic alphas": "Zura Kakushadze's seminal paper explicitly detailing mathematical formulations and code for 101 real-world, cross-sectional equity formulaic alphas.",
    "riskminer discovering formulaic alphas via risk seeking monte carlo tree search": "Introduces RiskMiner, applying risk-seeking Monte Carlo Tree Search to efficiently explore the mathematical expression tree space for robust formulaic alphas.",
    "complexity aware deep symbolic regression with robust risk seeking policy gradients": "Develops complexity-regularized deep symbolic regression using risk-seeking policy gradients to mine parsimonious, interpretable financial alpha formulas.",
    "the deflated sharpe ratio correcting for selection bias backtest overfitting and non normality": "Bailey and Lopez de Prado's seminal paper deriving the Deflated Sharpe Ratio to correct for selection bias, multiple testing, and non-normal asset returns in backtesting.",
    "alphaevolve a learning framework to discover novel alphas in quantitative investment": "Proposes an evolutionary genetic programming framework incorporating structural fitness pruning to discover novel, non-linear quantitative trading alphas.",
    "alpha gpt human ai interactive alpha mining for quantitative investment": "Introduces Alpha-GPT, an interactive human-in-the-loop framework leveraging LLMs to translate investment hypotheses into formulaic alpha expressions.",
    "r d agent quant a multi agent framework for data centric factors and model joint optimization": "Microsoft Research multi-agent framework automating the end-to-end iteration of data-centric factor discovery, feature engineering, and model optimization.",
    "a review of simulation optimization with connection to artificial intelligence": "Surveys mathematical simulation optimization techniques, stochastic gradient estimation, and Bayesian optimization in complex stochastic systems.",
    "a statistical test to control excessive parameter fitting of trading strategy": "Develops statistical hypothesis tests to bound and control for false discovery rates and excessive parameter tuning in algorithmic trading strategy backtests.",
    "the three types of backtests": "Hillsdale Investment Management paper classifying backtests into exploratory, explanatory, and predictive categories to identify backtest overfitting mechanisms.",
    "alphaeval a comprehensive and efficient evaluation framework for formula alpha mining": "Presents a standardized evaluation framework assessing predictive correlation, factor turnover, market capacity, and decay dynamics in formulaic alphas.",
    "quantagents towards multi agent financial system via simulated trading": "Simulates an autonomous multi-agent financial market environment where diverse LLM agents formulate trading strategies, execute orders, and generate price dynamics.",

    # 16. ETF Structure & Microstructure
    "an empirical analysis of sec rule 6c 11 s impact on the usage of heartbeat trades by exchange": "Columbia Law empirical study analyzing how SEC Rule 6c-11's custom basket provisions altered authorized participant heartbeat trades and tax efficiency in ETFs.",
    "when tracking error misleads risk exposure differences between etfs and their indices": "Documents structural differences in factor exposures, sampling error, and cash drag between physical ETFs and their underlying benchmark indices.",
    "actively managed etfs are they really active": "EFMA study analyzing active share, portfolio turnover, and idiosyncratic factor risk in actively managed exchange-traded funds.",
    "taxing index funds mutual funds etfs and paths to reform": "Brookings Institution monograph analyzing the tax-deferral mechanics of in-kind ETF creation/redemption and proposing tax policy reform frameworks.",
    "unplugging heartbeat trades and reforming the taxation of etfs": "University of Chicago Business Law Review article analyzing the legal mechanics and tax implications of custom basket heartbeat trades by ETF authorized participants.",
    "the tax revolution how etfs are reshaping investment strategy": "Alpha Architect treatise detailing the structural tax advantages of ETF in-kind creation/redemption mechanics compared to open-end mutual funds.",
    "microstructure implications of etf arbitrage with custom baskets": "ESRB working paper analyzing how custom basket ETF arbitrage affects liquidity, price discovery, and systematic inventory risk in underlying securities.",

    # 17. AI Testing & Financial Agents
    "agentic trading when llm agents meet financial markets": "Examines the emergent behaviors, market impact, and systemic feedback risks of autonomous LLM trading agents operating in simulated electronic financial markets.",
    "fintoolbench evaluating llm agents for real world financial tool use": "Introduces FinToolBench, a rigorous benchmark evaluating LLM agent accuracy and reasoning fidelity across financial API tool calling and analytical workflows.",
    "time series augmented generation for financial applications": "Develops Time-Series Augmented Generation (TAG) to ground LLM financial reasoning in quantitative time-series models and empirical data.",
    "a survey on uncertainty quantification in deep learning for financial time series prediction": "Surveys Bayesian deep learning, ensemble methods, and conformal prediction for quantifying epistemic and aleatoric uncertainty in financial forecasting.",
    "large language model agent in financial trading a survey": "Comprehensive survey reviewing architectures, multi-agent frameworks, tool augmentation, and execution challenges for LLM agents in financial trading.",

    # Batch 2 Curated Research Papers
    "0dte index options and market volatility how large is their impact": "Cboe quantitative research study analyzing intraday volume, dealer delta/gamma hedging, and market stability effects of same-day expiration (0DTE) SPX options.",
    "a century of stock bond correlations": "Reserve Bank of Australia historical study analyzing the macroeconomic determinants of time-varying equity-bond correlations across 100 years.",
    "a cgan lstm based framework for time varying non stationary channel modeling": "Applies Conditional GANs paired with LSTM temporal architectures to generate synthetic non-stationary sequential time series.",
    "a comparison of lstms and attention mechanisms for forecasting financial time series": "Benchmarks recurrent LSTM architectures against multi-head self-attention mechanisms on noisy financial return series.",
    "a comprehensive review and analysis of different modeling approaches for financial index tracking problem": "Surveys sparse index tracking, tracking error minimization, and integer programming models in ETF and benchmark portfolio construction.",
    "a deep learning approach for trading factor residuals": "Develops deep neural network models to predict and trade idiosyncratic factor residuals in equity statistical arbitrage.",
    "a factor model for option returns": "NBER study developing a parsimonious factor pricing model for the cross-section of equity and index option returns.",
    "a framework for predictive directional trading based on volatility and causal inference": "Develops a causal inference trading framework linking option surface implied skew shifts to forward directional spot returns.",
    "a gentle introduction to conformal prediction and distribution free uncertainty quantification": "Angelopoulos and Bates' authoritative tutorial detailing mathematical foundations, non-conformity scores, and finite-sample coverage guarantees in conformal prediction.",
    "a gentle introduction to conformal time series forecasting": "Surveys conformal prediction methodologies adapted to dependent, autocorrelated financial time series and non-stationary distribution shifts.",
    "a machine learning approach to risk based asset allocation": "Applies supervised machine learning algorithms to dynamic risk parity and equal risk contribution portfolio weighting.",
    "a no arbitrage survey of the term structure of interest rates": "Econometric review of no-arbitrage dynamic yield curve models linking monetary policy expectations to duration risk premia.",
    "a note on the grs test": "Econometric note detailing finite-sample properties and power calculations for the Gibbons-Ross-Shanken test of multi-factor asset pricing models.",
    "a novel hybrid model emd ti lstm for enhanced financial forecasting with machine learning": "Combines Empirical Mode Decomposition (EMD) with technical indicators and LSTM networks to forecast non-stationary financial prices.",
    "a novel pricing method for european options based on fourier cosine series expansions": "Fang and Oosterlee's seminal paper introducing the COS method for ultra-fast, high-precision European option pricing via Fourier-cosine series expansions.",
    "a review on graph neural network methods in financial applications": "Surveys spatial and temporal Graph Neural Networks (GNN) for modeling supply-chain relationships, interconnected financial risks, and asset price spillovers.",
    "a scenario based allocation model using entropy pooling for computing the scenario probabilities": "Combines scenario generation with Meucci's entropy pooling to compute posterior probability distributions reflecting macro views.",
    "a step by step guide to the black litterman model incorporating user specified confidence levels": "Idzorek's authoritative guide on quantifying user-specified confidence levels and calibrating diagonal variance matrices for subjective views in Black-Litterman.",
    "a stock selection model of image classification method based on": "Converts financial time-series chart data into 2D Gramian Angular Fields for convolutional neural network equity return classification.",
    "a survey of high frequency trading strategies": "Stanford technical survey detailing statistical arbitrage, latency arbitrage, order book imbalance modeling, and inventory control algorithms in HFT.",
    "a trend following deep dive ai agents and trend": "Man AHL research note examining how LLM agents and machine learning feature extraction enhance systematic trend-following strategies.",
    "adaptive conformal inference for computing market risk measures an analysis with four thousand crypto assets": "Applies adaptive conformal inference to generate valid distribution-free Value-at-Risk intervals across 4,000 highly volatile cryptocurrency assets.",
    "advanced stock market prediction using long short term memory networks a comprehensive deep learning framework": "Designs multi-layer LSTM architectures incorporating regularization and feature engineering for robust financial time series prediction.",
    "advanced stock price prediction using lstm and informer models": "Compares Informer sparse-attention architectures against standard LSTMs for long-sequence financial time series forecasting.",
    "advancements and challenges in deep reinforcement learning for stock trading a comprehensive review": "Surveys DRL algorithms (PPO, DDPG, SAC) applied to portfolio optimization, execution algorithms, and market making.",
    "affine term structure models a review": "Comprehensive survey of Gaussian and non-Gaussian affine term structure models (ATSM) for yield curve fitting and term premium extraction.",
    "algorithmic approach to taxable investing": "NYU Courant mathematical framework optimizing after-tax portfolio alpha using dynamic programming and multi-period loss harvesting.",
    "an empirical analysis of sec rule 6c 11 s impact on the usage of heartbeat trades by exchange": "Columbia Law empirical study analyzing how SEC Rule 6c-11's custom basket provisions altered authorized participant heartbeat trades and tax efficiency in ETFs.",
    "an entropy based approach to portfolio optimization": "Applies maximum entropy principles to overcome estimation risk and produce well-diversified portfolio weight distributions without extreme corner solutions.",
    "and the cross section of expected returns": "Harvey, Liu, and Zhu's seminal study evaluating 300+ published asset pricing factors and establishing t-statistic hurdles > 3.0 to correct for data snooping.",
    "application of black litterman bayesian in statistical arbitrage": "Applies the Black-Litterman Bayesian framework to combine statistical arbitrage mean-reversion alphas with cross-sectional risk equilibrium priors.",
    "black litterman and beyond the bayesian paradigm in investment management": "NYU Courant monograph detailing extensions of Black-Litterman incorporating macroeconomic regime switches, dynamic factor exposures, and shrinkage priors.",
    "black litterman model with copula based views in mean cvar portfolio optimization framework with weight constraints": "Combines copula-based subjective views with Conditional Value-at-Risk (CVaR) optimization under realistic portfolio weight constraints.",
    "can machine learning predict factor returns": "Empirically benchmarks penalized regressions, tree ensembles, and neural networks in forecasting out-of-sample cross-sectional factor returns.",
    "cboe s p 500 dispersion index": "Cboe whitepaper detailing the design, mathematical basket calculation, and economic applications of the DSPX Dispersion Index.",
    "computing skew stickiness": "Develops analytical formulas for calculating the Skew-Stickiness Ratio (SSR) to quantify volatility smile shifts relative to underlying spot movements.",
    "conditional autoencoder asset pricing models for the korean stock market": "Applies Gu, Kelly, and Xiu's conditional autoencoder architecture to extract latent non-linear risk factors in emerging equity markets.",
    "convergence of the binomial tree method for american options in a jump diffusion model": "Proves the mathematical convergence and stability of discrete lattice algorithms for American options under Merton jump-diffusion dynamics.",
    "copula based black litterman portfolio optimization": "Extends Black-Litterman to non-linear, non-Gaussian asset returns and tail dependencies using copula functions.",
    "deep learning for financial time series prediction a state of the art survey": "Comprehensive survey reviewing Transformer, LSTM, CNN, and GNN architectures across high-frequency and daily financial price forecasting.",
    "dynamic investment strategies with machine learning methods": "Evaluates dynamic asset allocation strategies using tree-based ensembles, gradient boosting, and deep neural networks across equity regimes.",
    "estimating affine term structure models with macro variables": "Adrian, Crump, and Moench's (ACM) multi-factor pricing kernel extracting term premia from sovereign yield curves using linear regressions.",
    "expectations and the term structure of interest rates": "Seminal empirical study testing the Expectations Hypothesis of the term structure and documenting systematic time-varying term premia.",
    "from prompt injections to sql injection attacks how protected is your llm integrated web application": "ACM / IEEE cybersecurity study demonstrating how adversarial prompt injection attacks can propagate through LLM agents to execute unauthorized SQL database operations.",
    "global financial stability report april 2025 chapter 1 enhancing resilience amid global trade uncertainty": "IMF Global Financial Stability Report analyzing sovereign debt vulnerabilities, banking sector resilience, and cross-border trade friction risks.",
    "harvesting the volatility risk premium globally": "The Hedge Fund Journal study analyzing multi-asset global implementations of systematic variance harvesting across equity, fixed income, and currency options.",
    "historical development of portfolio theory": "Comprehensive academic retrospective tracing seven decades of quantitative portfolio construction methodologies from MPT to modern factor models.",
    "how many factors are there or how to navigate the factor zoo": "Robeco quantitative research paper applying disciplined dimensionality reduction to distinguish genuine asset pricing factors from statistical noise.",
    "incorporating qualitative views in the black litterman model": "Formulates formal mapping mechanisms for translating qualitative, ranking-based, and directional views into mathematically consistent Black-Litterman inputs.",
    "leverage does not equal risk": "AQR / Cliff Asness whitepaper explaining why borrowing against a diversified low-beta risk-parity portfolio provides superior Sharpe ratios compared to concentrated equity risk.",
    "linear and nonlinear econometric models against machine learning models realized volatility prediction": "Federal Reserve Board econometric study benchmarking GARCH and HAR models against Random Forests and neural networks for multi-horizon realized volatility prediction.",
    "macroeconomic factors in the term structure of interest rates": "Kim and Wright's foundational Fed working paper modeling affine term structure models with latent and macroeconomic state variables.",
    "maximum entropy approach to portfolio optimization economic justification of an intuitive diversity idea": "Provides information-theoretic economic justification for maximum entropy diversification as a robust alternative to mean-variance optimization.",
    "optimal portfolio diversification using the maximum entropy principle": "Formulates portfolio optimization under entropy constraints to bound portfolio concentration and maximize structural diversification across risk factors.",
    "optimizing expected shortfall under an l1 constraint an analytic approach": "Derives closed-form analytical solutions for optimizing Expected Shortfall (CVaR) under L1 sparsity and transaction cost constraints.",
    "put call ratio volume vs open interest in predicting market return a frequency domain rolling causality analysis": "Applies frequency-domain wavelet and rolling Granger causality tests to evaluate the directional predictive power of option volume vs. open interest ratios.",
    "risk parity not performing blame the weather": "AQR research report analyzing macroeconomic growth and inflation shock attribution in risk parity underperformance episodes.",
    "s p 500 index price spillovers around the covid 19 market meltdown": "Empirically documents cross-market volatility and liquidity transmission between equity indices and index options during the March 2020 liquidity crunch.",
    "shrinkage estimators for mean and covariance evidence on portfolio efficiency across market dimensions": "Demonstrates that Ledoit-Wolf covariance shrinkage significantly reduces tracking error and out-of-sample portfolio variance across high-dimensional asset universes.",
    "statistical properties of financial time series": "Foundational survey by Rama Cont detailing the empirical universal statistical properties and non-Gaussian characteristics of asset returns.",
    "stylized facts of financial time series and three popular models of volatility": "Wharton econometrics study documenting empirical stylized facts (fat tails, volatility clustering, asymmetry) and benchmarking ARCH/GARCH and stochastic volatility models.",
    "tax aware portfolio construction via convex optimization": "Formulates tax-aware direct indexing and loss harvesting as a convex optimization problem balancing tracking error, capital gains taxes, and transaction costs.",
    "testing for alpha in linear factor pricing models with a large number of securities": "Oxford Academic study deriving asymptotic tests for multi-factor pricing alphas in high-dimensional equity universes.",
    "the black litterman asset allocation model": "Foundational treatise on the Black-Litterman reverse-optimization implied equilibrium prior and Bayesian blending framework for portfolio construction.",
    "the black litterman model in practice": "Institutional practitioner guide on calibrating scaling parameter tau, handling view collinearity, and deploying Black-Litterman across global multi-asset portfolios.",
    "the black litterman model mathematical and behavioral aspects": "Analyzes the mathematical properties of Bayesian shrinkage and behavioral framing of investor subjective confidence in Black-Litterman optimization.",
    "the bond market term premium what is it and how can we measure it": "Federal Reserve Bank study explaining the theoretical mechanics and econometric estimation of sovereign bond term premia.",
    "the corporate bond factor replication crisis": "Replication study evaluating whether proposed corporate bond factor anomalies survive transaction costs, illiquidity, and rigorous multiple-testing corrections.",
    "the evolution of portfolio theory": "Surveys the historical progression from Markowitz mean-variance optimization and CAPM to robust Bayesian allocation and entropy pooling.",
    "the fundamental theorem of asset pricing for unbounded stochastic processes": "Delbaen and Schachermayer's seminal mathematical treatise establishing the equivalence between No Free Lunch with Vanishing Risk (NFLVR) and equivalent local martingale measures.",
    "the impact of dispersion on market expectations and volatility": "Analyzes how single-stock implied dispersion leads shifts in aggregate index volatility and provides forward signals for market regime transitions.",
    "the intuition behind black litterman model portfolios": "Deconstructs the mathematical intuition and economic mechanics of how Black-Litterman view tilts alter optimal portfolio weight vectors.",
    "the price of the smile and variance risk premia": "Decomposes the implied volatility surface into pure diffusive variance premia and higher-order skewness/kurtosis crash insurance premia.",
    "the role of taxes in the rise of etfs": "Analyzes the economic value of Section 852(b) in-kind redemption tax exemptions in driving the massive migration of capital from mutual funds to ETFs.",
    "the smile of the volatility risk premia": "Quantifies the moneyness slope of volatility risk premia across equity index option smiles and its connection to downside jump probability.",
    "the term structure of expectations and bond yields": "Decomposes long-term sovereign bond yields into short-rate expectations, inflation expectations, and real term premia across business cycles.",
    "the term structure of systematic risk": "Documents how systematic market risk premia vary across horizons, from high-frequency intraday shocks to long-run macroeconomic consumption risks.",
    "timebridge non stationarity matters for long term time series forecasting": "Proposes TimeBridge, a specialized architecture explicitly modeling temporal distribution shifts and non-stationarity in long-horizon forecasting.",
    "trading strategies for extended global trading hours for vix and spx options": "Cboe quantitative research study analyzing liquidity, price discovery, and overnight volatility transmission during Extended Global Trading Hours for SPX/VIX options.",
    "treasury term premia 1961 present": "New York Fed historical empirical study tracing Treasury term premium fluctuations across six decades of macroeconomic and inflation regimes.",
    "understanding mortgage spreads": "New York Fed staff report analyzing the structural OAS, prepayment risk, and duration-hedging dynamics driving Agency MBS spreads.",
    "unveiling nonlinear dynamics in catastrophe bond pricing a machine learning perspective": "Applies non-linear machine learning models to capture tail risk, reinsurance market cycles, and parametric peril triggers in ILS catastrophe bond pricing.",
    "vanna volga methods applied to fx derivatives from theory to market practice": "Formulates the Vanna-Volga pricing and hedging methodology for calibrating implied volatility smiles and pricing exotic barrier options in FX markets.",
    "variance premium downside risk and expected stock returns": "Bank of Canada study showing that downside variance risk premia capture rare disaster risks and provide superior predictive power for cross-sectional equity returns.",
    "volatility clustering in financial markets empirical facts and agent based models": "Analyzes the micro-foundations of volatility clustering using heterogeneous agent-based models of financial market dynamics.",
    "volatility concepts and the risk premium": "Bank for International Settlements (BIS) study analyzing the structural divergence between implied and realized volatility and its role in global financial stability.",
    "volatility expectations and returns": "NBER study showing that subjective survey volatility expectations decouple from option-implied volatility, explaining the magnitude of the variance risk premium.",
    "volatility risk premia and future commodities returns": "BIS working paper documenting that commodity implied volatility risk premia forecast future spot commodity returns across energy, agriculture, and metals.",
    "volatility risk premiums embedded in individual equity options": "Bakshi and Kapadia's seminal Journal of Derivatives paper showing that single-stock options trade at negative volatility risk premiums driven by idiosyncratic jump risk.",
    "volatility risk premiums embedded in individual equity options some new insights": "Empirically tests cross-sectional determinants of individual equity option volatility risk premiums across market capitalization and skewness quintiles.",
    "why have long term treasury yields fallen since the 1980s expected short rates and term premiums in quasi real time": "Federal Reserve Board study decomposing the secular four-decade decline in Treasury yields into short-rate expectations versus compressed term premia.",
    "will my risk parity strategy outperform": "Robert M. Anderson's UC Berkeley study analyzing the theoretical and empirical leverage constraints, borrow costs, and benchmark drag of risk parity strategies.",

    # Batch 2 Additional Curated Research Papers
    "2025 u s equities year in review": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of 2025 U.S. Equities Year in Review in etf mechanics.",
    "agonalpha autonomous alpha discovery via prompt economy and scalable agentic search": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "ai s mysterious black box problem explained university of": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of AI's mysterious 'black box' problem, explained | University of in machine learning.",
    "air supply boosting capital efficiency with cleared derivatives": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of AIR Supply: boosting capital efficiency with cleared derivatives in vrp.",
    "alpha decay jackson hole finance group": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "alphabench benchmarking large language model in formulaic alpha factor mining": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "alphaforge a framework to mine and dynamically combine formulaic alpha factors": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "alternative data market size growth forecast to 2034 imarc group": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Alternative Data Market Size, Growth & Forecast to 2034 - IMARC Group in quantitative finance.",
    "an introduction to functional analysis contents 1 introduction 1 2 some basic definitions 2 3 preliminaries 3 4 dual spaces uchicago math": "Mathematical foundation detailing Hilbert and Banach spaces, linear operators, and dual spaces in continuous-time financial engineering.",
    "an overview of machine learning deep learning and reinforcement learning based techniques in quantitative finance recent progress and challenges": "Surveys deep reinforcement learning algorithms applied to dynamic portfolio optimization, algorithmic execution, and market making.",
    "appendix a affine term structure model rdp 2023 04 can we use high frequency yield data to better understand the effects of monetary policy and its communication yes and no reserve bank of australia": "SqueezeMetrics quantitative study demonstrating that off-exchange short sale volume reflects market maker liquidity provision against institutional accumulation.",
    "application of adaptive machine learning in non stationary environments": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Application of Adaptive Machine Learning in Non-Stationary Environments in machine learning.",
    "application of long short term memory lstm in stock price prediction": "Evaluates Long Short-Term Memory (LSTM) recurrent neural networks for multi-horizon financial asset price and volatility forecasting.",
    "applications of entropy in finance a review": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Applications of Entropy in Finance: A Review in entropy pooling.",
    "applications of recurrent neural network on financial time series": "Evaluates Long Short-Term Memory (LSTM) recurrent neural networks for multi-horizon financial asset price and volatility forecasting.",
    "applications of recurrent neural network on financial time series imperial college london": "Evaluates Long Short-Term Memory (LSTM) recurrent neural networks for multi-horizon financial asset price and volatility forecasting.",
    "applying convolutional neural networks for stock market trends identification": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Applying Convolutional Neural Networks for Stock Market Trends Identification in deep learning.",
    "aqua recursively self improving quantitative trading research agents": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of AQuA: Recursively Self-Improving Quantitative Trading Research Agents in quantitative finance.",
    "assessing tracking error of the municipal bond etfs the aquila digital community": "Analyzes ETF creation/redemption mechanics, authorized participant arbitrage dynamics, tax efficiency, and secondary market liquidity.",
    "asset pricing in transformer": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "attention based dynamic graph neural network for asset pricing pmc pubmed central": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "authorized participants regulatory constraints and limits to etf arbitrage during market turmoil evidence from the dash for cash episode": "Analyzes ETF creation/redemption mechanics, authorized participant arbitrage dynamics, tax efficiency, and secondary market liquidity.",
    "back to basics the power of the multilayer perceptron in financial time series forecasting": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Back to Basics: The Power of the Multilayer Perceptron in Financial Time Series Forecasting in deep learning.",
    "basic concepts and techniques of risk management": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Basic Concepts and Techniques of Risk Management in measure theory.",
    "black box investing versus common sense quant": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Black Box Investing Versus Common Sense Quant in machine learning.",
    "black litterman model uc berkeley statistics": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Black-Litterman Model - UC Berkeley Statistics in portfolio optimization.",
    "bond return predictability economic value and links to the macroeconomy rady school of management": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Bond Return Predictability: Economic Value and Links to the Macroeconomy - Rady School of Management in fixed income.",
    "building ai coding agents for the terminal scaffolding harness context engineering and lessons learned": "Architectural treatise detailing terminal scaffolding, prompt harness engineering, and token budget context optimization for autonomous software agents.",
    "cboe global markets": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Cboe Global Markets in vrp.",
    "cboe to launch new cboe s p 500 variance futures on monday september 23": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "cboe u s equities market volume summary": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Cboe U.S. Equities Market Volume Summary in etf mechanics.",
    "chapter 12 non parametric methods 6 390": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of CHAPTER 12 Non-parametric methods - 6.390 in machine learning.",
    "cirgnn leveraging cross chart relationships with a graph neural network for stock price prediction": "Applies spatial and temporal Graph Neural Networks to model financial interconnections, supply chains, and asset return co-movements.",
    "comparative analyses of expected shortfall and value at risk their estimation error decomposition and optimization": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Comparative Analyses of Expected Shortfall and Value-at-Risk: Their Estimation Error, Decomposition, and Optimization in measure theory.",
    "comparative analysis of conformal prediction split full and adaptive approaches for statistical and neural network model proceedings of the design society cambridge university press assessment": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "comparative evaluation of var model historical simulation garch based monte carlo and filtered historical simulation": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Comparative Evaluation of VaR Models: Historical Simulation, GARCH-Based Monte Carlo, and Filtered Historical Simulation in conformal prediction.",
    "comparative study of support vector machines and random forests machine learning algorithms on credit operation": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Comparative study of support vector machines and random forests machine learning algorithms on credit operation in deep learning.",
    "comparison of historical and parametric value at risk methodologies": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Comparison of Historical and Parametric Value-at-Risk Methodologies in conformal prediction.",
    "comparison of value at risk var multivariate forecast model": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Comparison of Value at Risk (VaR) Multivariate Forecast Models in conformal prediction.",
    "computing systemic risk measures with graph neural networks": "Applies spatial and temporal Graph Neural Networks to model financial interconnections, supply chains, and asset return co-movements.",
    "conditional coverage diagnostics for conformal prediction": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "conformal prediction algorithms for time series forecasting methods and benchmark": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "conformal prediction assessment a framework for conditional coverage evaluation and selection": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "conformal prediction stat berkeley edu": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "conformal predictive portfolio selection": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "conformal risk control": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "conformal risk control openreview": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "conformal risk training end to end optimization of conformal risk control": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "country default spreads and risk premium": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Country Default Spreads and Risk Premiums in vrp.",
    "covered call strategy one fact and eight myths": "Deconstructs eight common practitioner misconceptions regarding covered call writing, clarifying its true beta reduction and capped upside mechanics.",
    "covered call uncovered": "CFA Institute Research monograph analyzing the risk-return tradeoffs, return asymmetries, and empirical Sharpe ratios of systematic covered call writing.",
    "covered call uncovered cfa institute research and policy center": "CFA Institute Research monograph analyzing the risk-return tradeoffs, return asymmetries, and empirical Sharpe ratios of systematic covered call writing.",
    "credit risk modeling with graph machine learning informs journal on data science": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Credit Risk Modeling with Graph Machine Learning | INFORMS Journal on Data Science in deep learning.",
    "daily short sale volume files": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Daily Short Sale Volume Files in market microstructure.",
    "decoding market regimes machine learning insights into us asset performance over the last 30 years": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Decoding Market Regimes Machine Learning Insights into US Asset Performance Over The Last 30 Years in machine learning.",
    "deep learning enhanced multi day turnover quantitative trading algorithm for chinese a share market": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Deep Learning Enhanced Multi-Day Turnover Quantitative Trading Algorithm for Chinese A-Share Market in machine learning.",
    "deep learning factor alpha acfr aut": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "deep learning in finance a survey of applications and techniques": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Deep Learning in Finance: A Survey of Applications and Techniques in deep learning.",
    "deep learning in quantitative trading cambridge university press": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Deep Learning in Quantitative Trading - Cambridge University Press in machine learning.",
    "deep learning in quantitative trading cambridge university press assessment": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Deep Learning in Quantitative Trading - Cambridge University Press & Assessment in deep learning.",
    "deep reinforcement learning approach to portfolio management": "Surveys deep reinforcement learning algorithms applied to dynamic portfolio optimization, algorithmic execution, and market making.",
    "developing high frequency equities trading model dspace mit": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Developing High-Frequency Equities Trading Models - DSpace@MIT in factor models.",
    "diplomarbeit convergence analysis of the longstaff schwartz algorithm the research unit fam financial and actuarial mathematics": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Diplomarbeit Convergence Analysis of the Longstaff-Schwartz Algorithm - The research unit FAM - Financial and Actuarial Mathematics in measure theory.",
    "discussion of quantitative tightening around the globe what have we learned by wenxin du kristin forbes and matthew luzzetti dallasfed org": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Discussion of 'Quantitative Tightening Around the Globe: What Have We Learned?' by Wenxin Du, Kristin Forbes and Matthew Luzzetti - Dallasfed.org in fixed income.",
    "dispersion trading based on the explanatory power of s p 500 stock returns": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Dispersion Trading Based on the Explanatory Power of S&P 500 Stock Returns in vrp.",
    "do dark pools harm price discovery": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Do Dark Pools Harm Price Discovery? in market microstructure.",
    "dynamic estimation of volatility risk premium and investor risk aversion from option implied and realized volatilities": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "dynamic estimation of volatility risk premium and investor risk aversion from option implied and realized volatilities federal reserve board": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "dynamic estimation of volatility risk premium and investor risk aversion from option implied and realized volatilities scholars duke publication": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "dynamic graph neural networks for enhanced volatility prediction in financial markets": "Applies spatial and temporal Graph Neural Networks to model financial interconnections, supply chains, and asset return co-movements.",
    "ele539a optimization of communication systems lecture 2 convex optimization and lagrange duality": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of ELE539A: Optimization of Communication Systems Lecture 2: Convex Optimization and Lagrange Duality in entropy pooling.",
    "embracing downside risk": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Embracing Downside Risk in vrp.",
    "empirical evidence on the stock bond correlation taylor francis": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Empirical Evidence on the Stock–Bond Correlation - Taylor & Francis in fixed income.",
    "enhanced portfolio optimization": "Examines robust Bayesian and resampled frontier techniques to mitigate input estimation errors in institutional mean-variance portfolio construction.",
    "enhancing model explainability in financial trading using training aid samples a cnn based candlestick pattern recognition approach ieee xplore": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Enhancing Model Explainability in Financial Trading Using Training Aid Samples: A CNN-Based Candlestick Pattern Recognition Approach - IEEE Xplore in deep learning.",
    "enhancing time series product demand forecasting with hybrid attention based deep learning model ieee xplore": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "entropy augmented forecasting and portfolio construction at the industry group level a causal machine learning approach using gradient boosted decision trees": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Entropy-Augmented Forecasting and Portfolio Construction at the Industry-Group Level: A Causal Machine-Learning Approach Using Gradient-Boosted Decision Trees in entropy pooling.",
    "entropy information and the updating of probabilities": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Entropy, Information, and the Updating of Probabilities in entropy pooling.",
    "entropy pooling with discrete weights in a time dependent setting": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Entropy Pooling with Discrete Weights in a Time-Dependent Setting in entropy pooling.",
    "equity volatility term premium": "Decomposes sovereign bond yields into short-rate expectations and duration risk premia using affine term structure models across macroeconomic cycles.",
    "etf arbitrage under liquidity mismatch": "Analyzes ETF creation/redemption mechanics, authorized participant arbitrage dynamics, tax efficiency, and secondary market liquidity.",
    "etf volume leaders": "Analyzes ETF creation/redemption mechanics, authorized participant arbitrage dynamics, tax efficiency, and secondary market liquidity.",
    "etfs and tax efficiency what you need to know": "Analyzes ETF creation/redemption mechanics, authorized participant arbitrage dynamics, tax efficiency, and secondary market liquidity.",
    "etfs arbitrage and contagion financial markets group": "Analyzes ETF creation/redemption mechanics, authorized participant arbitrage dynamics, tax efficiency, and secondary market liquidity.",
    "evaluating the longstaff schwartz method for pricing of american options": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "evaluation of transformer model for financial targeted sentiment analysis in spanish": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "exotic options and fourier transforms the story is far from over": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "expected option returns": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "expected return and risk of covered call strategy": "Empirically decomposes the expected return, volatility reduction, and downside tail skewness of systematic covered call overlays.",
    "explaining the global interest rate decline bates college": "Analyzes the empirical dynamics, factor decomposition, and macroeconomic drivers of the sovereign yield curve.",
    "exploring different dynamics of recurrent neural network methods for stock market prediction a comparative study": "Evaluates Long Short-Term Memory (LSTM) recurrent neural networks for multi-horizon financial asset price and volatility forecasting.",
    "exploring the tips treasury valuation puzzle liberty street economics": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Exploring the TIPS-Treasury Valuation Puzzle - Liberty Street Economics in fixed income.",
    "finance and economics discussion series screen reader version term structure modeling with supply factors and the federal reserve s large scale asset purchase programs": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "financial forecasting with α rnns a time series modeling approach frontiers": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Financial Forecasting With α-RNNs: A Time Series Modeling Approach - Frontiers in machine learning.",
    "financial machine learning the university of chicago": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Financial Machine Learning - The University of Chicago in deep learning.",
    "financial sentiment analysis and classification a comparative study of fine tuned deep learning model": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Financial Sentiment Analysis and Classification: A Comparative Study of Fine-Tuned Deep Learning Models in deep learning.",
    "financial sentiment analysis using finbert with application in predicting stock movement": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Financial Sentiment Analysis Using FinBERT with Application in Predicting Stock Movement in deep learning.",
    "fine tuning bert for sentiment analysis on financial news": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Fine-Tuning BERT for Sentiment Analysis on Financial News in deep learning.",
    "finrobot an open source ai agent platform for financial applications using large language model": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of FinRobot: An Open-Source AI Agent Platform for Financial Applications using Large Language Models in ai agents.",
    "fixed income cross margin opportunities a driver of change": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Fixed-income cross-margin opportunities: A driver of change in vrp.",
    "fixed income etfs bond liquidity and stressed markets": "Analyzes ETF creation/redemption mechanics, authorized participant arbitrage dynamics, tax efficiency, and secondary market liquidity.",
    "forecasting bond risk premium using stationary yield factors european financial management association": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "forecasting of realised volatility with the random forests algorithm": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "forecasting s p 500 using lstm model": "Evaluates Long Short-Term Memory (LSTM) recurrent neural networks for multi-horizon financial asset price and volatility forecasting.",
    "forecasting stock prices with long short term memory neural network based on attention mechanism plos one": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "from attention to profit quantitative trading strategy based on transformer": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "from factor model to deep learning machine learning in reshaping empirical asset pricing": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "from feedback loops to policy updates reinforcement fine tuning for llm based alpha factor discovery": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "fully flexible views in multivariate normal markets": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Fully Flexible Views in Multivariate Normal Markets in entropy pooling.",
    "general covar based on entropy pooling the authors are listed in alphabetical order": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "globalmarkets weekly wrap up syz group": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of #globalmarkets weekly wrap-up - Syz Group in market microstructure.",
    "graph neural networks for financial systemic risk analysis and network effects": "Applies spatial and temporal Graph Neural Networks to model financial interconnections, supply chains, and asset return co-movements.",
    "harvest volatility risk premium using deep reinforcement learning imperial college london": "Surveys deep reinforcement learning algorithms applied to dynamic portfolio optimization, algorithmic execution, and market making.",
    "harvesting volatility risk premium imperial college london": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "hidformer transformer style neural network in stock price forecasting": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "historical returns on stocks bonds and bills 1928 2024": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Historical Returns on Stocks, Bonds and Bills: 1928-2024 in fixed income.",
    "how ai debt financing impacts duration supply and interest rates": "Analyzes the empirical dynamics, factor decomposition, and macroeconomic drivers of the sovereign yield curve.",
    "how to justify your alpha step by step stephen d benning": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "how to trade stock dispersion with options": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "hrft mining high frequency risk factor collections end to end via transformer": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "identifying high frequency trading activity without proprietary data": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Identifying High Frequency Trading activity without Proprietary Data in factor models.",
    "in broad daylight where the smart money shorts stocks smu cox school of business": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of In Broad Daylight: Where the Smart Money Shorts Stocks | SMU Cox School of Business in market microstructure.",
    "index insights may": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Index Insights: May in dspx.",
    "index tracking error optimization of equity and fixed income etfs": "Analyzes ETF creation/redemption mechanics, authorized participant arbitrage dynamics, tax efficiency, and secondary market liquidity.",
    "inflation uncertainty and the term premium imf elibrary": "Decomposes sovereign bond yields into short-rate expectations and duration risk premia using affine term structure models across macroeconomic cycles.",
    "innovations": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of innovations in quantitative finance.",
    "integrated garch gru in financial volatility forecasting": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "integration of lstm networks in random forest algorithms for stock market trading predictions": "Evaluates Long Short-Term Memory (LSTM) recurrent neural networks for multi-horizon financial asset price and volatility forecasting.",
    "interest rate spillovers from the united states expectations term premium and macro financial vulnerabilities": "Decomposes sovereign bond yields into short-rate expectations and duration risk premia using affine term structure models across macroeconomic cycles.",
    "investigating market strength prediction with cnns on candlestick chart images": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Investigating Market Strength Prediction with CNNs on Candlestick Chart Images in deep learning.",
    "is less is more using autoencoders for feature extraction in m a deal outcome prediction": "Applies deep autoencoder architectures to extract compressed latent risk factors and denoise high-dimensional financial feature spaces.",
    "itô taylor expansions for systems of stochastic differential equations with applications to stochastic partial differential equations": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Itô–Taylor Expansions for Systems of Stochastic Differential Equations with Applications to Stochastic Partial Differential Equations in measure theory.",
    "jump and volatility risk and risk premium a new model and lessons from s p 500 options": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "jumping the gates using beta overlay strategy to hedge liquidity constraints mit": "MIT study developing beta-overlay derivative strategies to maintain portfolio exposures while navigating institutional gating and liquidity constraints.",
    "l1 norm quantile regression department of statistics": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of L1-Norm Quantile Regression - Department of Statistics in measure theory.",
    "lecture 16 numerical sdes basics 1 schemes": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Lecture 16 Numerical SDEs: Basics 1 Schemes in measure theory.",
    "lecture 2 the svi arbitrage free volatility surface parameterization": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "lecture 9 patterns of volatility change copyright emanuel derman 2008": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "leverage aversion and risk parity": "Asness, Frazzini, and Pedersen's study demonstrating how investor leverage aversion creates excess risk-adjusted returns for leveraged low-beta risk parity portfolios.",
    "llm enhanced black litterman portfolio optimization": "Integrates Large Language Models to automatically extract structured qualitative sentiment and macroeconomic views for Black-Litterman portfolio optimization.",
    "long short term memory neural network for financial time series": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Long Short-Term Memory Neural Network for Financial Time Series in machine learning.",
    "lstm transformer based robust hybrid deep learning model for financial time series forecasting": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "machine learning enhanced multi factor quantitative": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "machine learning enhanced multi factor quantitative trading a cross sectional portfolio optimization approach with bias correction": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "machine learning for quantitative finance applications a survey": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Machine Learning for Quantitative Finance Applications: A Survey in deep learning.",
    "market making strategy with reinforcement learning": "Surveys deep reinforcement learning algorithms applied to dynamic portfolio optimization, algorithmic execution, and market making.",
    "measuring information decay in financial markets": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Measuring information decay in financial markets in factor models.",
    "minimizing shortfall 1 introduction": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Minimizing Shortfall 1 Introduction in measure theory.",
    "modality aware transformer for financial time series forecasting": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "model portfolios adaptive solutions for advisory growth": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Model Portfolios: Adaptive Solutions for Advisory Growth in portfolio optimization.",
    "mts a deep reinforcement learning portfolio management framework with time awareness and short selling": "Surveys deep reinforcement learning algorithms applied to dynamic portfolio optimization, algorithmic execution, and market making.",
    "multilayer perceptron modeling for social dysfunction prediction based on general health factors in an iranian women sample nih": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "multilayer perceptron neural network model in asset pricing an empirical study on large cap us stocks": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Multilayer Perceptron Neural Network Models in Asset Pricing: An Empirical Study on Large-Cap US Stocks in deep learning.",
    "nber working paper series an empirical decomposition of risk and liquidity in nominal and inflation indexed government bonds car": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of NBER WORKING PAPER SERIES AN EMPIRICAL DECOMPOSITION OF RISK AND LIQUIDITY IN NOMINAL AND INFLATION-INDEXED GOVERNMENT BONDS Car in fixed income.",
    "non stationary transformers exploring the stationarity in time series forecasting": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "on the application of spectral filters in a fourier option pricing technique journal of computational finance": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "on the fundamental theorem of asset pricing lsu scholarly repository": "Delbaen and Schachermayer's seminal mathematical treatise proving NFLVR equivalence to equivalent local martingale measures for unbounded stochastic processes.",
    "optimal execution a review": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Optimal Execution: A Review in quantitative finance.",
    "optimization of conditional value at risk uw math department": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Optimization of Conditional Value-at-Risk - UW Math Department in measure theory.",
    "optimization of covered call strategy": "Formulates mathematical portfolio optimization models incorporating covered call option overlays to maximize utility under asymmetric return distributions.",
    "option implied spreads and option risk premium": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "option pricing by transform methods extensions unification and error control": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "option trading strategy to harvest the volatility risk premium princeton dataspace": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "option valuation using the fast fourier transform": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "option valuation using the fast fourier transform imperial college london": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "orchestration framework for financial agents from algorithmic trading to agentic trading": "Proposes an orchestration architecture transitioning legacy algorithmic execution rules to autonomous LLM multi-agent trading systems.",
    "parametric stress testing in non normal markets via entropy pooling": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Parametric Stress-Testing in Non-Normal Markets via Entropy Pooling in entropy pooling.",
    "portfolio construction under behavioral distortions and narrow framing a machine learning approach": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Portfolio Construction Under Behavioral Distortions and Narrow Framing: A Machine Learning Approach in entropy pooling.",
    "portfolio optimization based stock prediction using long short term memory network in quantitative trading": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Portfolio Optimization-Based Stock Prediction Using Long-Short Term Memory Network in Quantitative Trading in deep learning.",
    "portfolio optimization for binary options based on relative entropy": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "portfolio optimization for binary options based on relative entropy pubmed": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "portfolio optimization with a mean entropy mutual information model": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Portfolio Optimization with a Mean-Entropy-Mutual Information Model in entropy pooling.",
    "portfolio optimization with covered call": "Formulates mathematical portfolio optimization models incorporating covered call option overlays to maximize utility under asymmetric return distributions.",
    "predictive financial and compliance risk modeling using scientific computing": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "pricing the term structure with linear regressions": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Pricing the Term Structure with Linear Regressions in fixed income.",
    "principle of maximum entropy simple form": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Principle of Maximum Entropy: Simple Form in entropy pooling.",
    "proxy reliance control in conformal recalibration of one sided value at risk": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "quantformer from attention to profit with a quantitative transformer trading strategy": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "quantitative easing and quantitative tightening speech by silvana tenreyro": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Quantitative easing and quantitative tightening − speech by Silvana Tenreyro in fixed income.",
    "quantitative trading using deep q learning": "Applies Deep Q-Networks (DQN) with experience replay to optimize discrete buy-sell-hold execution decisions in equity markets.",
    "recurrent neural networks vanishing and exploding gradients are not the end of the story": "Evaluates Long Short-Term Memory (LSTM) recurrent neural networks for multi-horizon financial asset price and volatility forecasting.",
    "recursive partitioning for heterogeneous causal effects stanford": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Recursive Partitioning for Heterogeneous Causal Effects | Stanford in machine learning.",
    "reflexivity and the feedback effect in financial markets": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Reflexivity and the Feedback Effect in Financial Markets in machine learning.",
    "reflexivity in credit markets": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Reflexivity in Credit Markets in machine learning.",
    "reflexivity in credit markets article faculty research harvard business school": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Reflexivity in Credit Markets - Article - Faculty & Research - Harvard Business School in machine learning.",
    "regulatory notice 21 19": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Regulatory Notice 21-19 in market microstructure.",
    "reinforcement learning framework for quantitative trading": "Surveys deep reinforcement learning algorithms applied to dynamic portfolio optimization, algorithmic execution, and market making.",
    "reporting firm 10 second compliance report card": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Reporting Firm 10 Second Compliance Report Card in market microstructure.",
    "rfs skew risk premium with kozhan and schneider pdf city research online": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of RFS Skew Risk Premium with Kozhan and Schneider.pdf - City Research Online in vrp.",
    "risk adjusted performance of random forest model in high frequency trading": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Risk-Adjusted Performance of Random Forest Models in High-Frequency Trading in machine learning.",
    "risk and reward new insights on 0dte option trading": "Empirical study analyzing intraday volume, dealer delta/gamma hedging, and market stability effects of same-day expiration (0DTE) index options.",
    "risk parity and its discontents": "Critical analysis of risk parity assumptions, evaluating sensitivity to rising interest rates, correlation spikes, and bond duration risks.",
    "risk parity risk management and the real world": "Examines real-world institutional implementation hurdles, liquidity constraints, and drawdown management in leveraged risk parity allocations.",
    "risk sensitive deep reinforcement learning for portfolio optimization": "Surveys deep reinforcement learning algorithms applied to dynamic portfolio optimization, algorithmic execution, and market making.",
    "robo advisors a portfolio management perspective jonathan walter lam advised by david f swensen presented to the department of": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Robo-Advisors: A Portfolio Management Perspective Jonathan Walter Lam Advised by David F. Swensen Presented to the Department of in portfolio optimization.",
    "selective conformal risk control": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "short dated term premium and the level of inflation liberty street economics": "Decomposes sovereign bond yields into short-rate expectations and duration risk premia using affine term structure models across macroeconomic cycles.",
    "short paper robo advisor methodologies dukespace": "Surveys quantitative algorithms, risk profiling mechanisms, and automated rebalancing architectures in digital wealth management robo-advisors.",
    "short sale volume": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Short Sale Volume in market microstructure.",
    "shorting in broad daylight short sales and venue choice": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Shorting in Broad Daylight: Short Sales and Venue Choice in market microstructure.",
    "stacked model with autoencoder for financial time series prediction ieee xplore": "Applies deep autoencoder architectures to extract compressed latent risk factors and denoise high-dimensional financial feature spaces.",
    "statistica sinica preprint no ss 2024 0167": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Statistica Sinica Preprint No: SS-2024-0167 in conformal prediction.",
    "stock and market index prediction using informer network": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Stock and market index prediction using Informer network in deep learning.",
    "taming tail risk in financial markets conformal risk control for nonstationary portfolio var": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "tariff and powell risk drive elevated cross asset vrps": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Tariff and Powell Risk Drive Elevated Cross-Asset VRPs in vrp.",
    "temporal conformal prediction tcp a distribution free statistical and machine learning framework for adaptive risk forecasting": "Provides distribution-free, finite-sample prediction intervals and coverage guarantees for quantitative risk management and forecasting.",
    "testing and ranking of asset pricing model using the grs statistic": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Testing and Ranking of Asset Pricing Models Using the GRS Statistic in factor models.",
    "tests of mean variance spanning": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "the 2022 spike in corporate security settlement fails liberty street economics": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of The 2022 Spike in Corporate Security Settlement Fails - Liberty Street Economics in fixed income.",
    "the benefits of tree based model for stock selection": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of The benefits of tree-based models for stock selection in machine learning.",
    "the black litterman approach original model and extensions": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of The Black-Litterman Approach: Original Model and Extensions in portfolio optimization.",
    "the black litterman model active risk targeting and the parameter tau": "Derives mathematical formulas connecting the Black-Litterman scalar tau to active tracking error budgets and subjective view confidence.",
    "the buy write strategy index investment the efficient market hypothesis australian evidence european financial management association": "Empirically evaluates the risk-adjusted returns, alpha generation, and benchmark outperformance of systematic buy-write strategies in equity markets.",
    "the efficiency of the buy write strategy evidence from australia": "Empirically evaluates the risk-adjusted returns, alpha generation, and benchmark outperformance of systematic buy-write strategies in equity markets.",
    "the fed banks backtesting exceptions during the covid 19 crash causes and consequences": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of The Fed - Banks' Backtesting Exceptions during the COVID-19 Crash: Causes and Consequences in conformal prediction.",
    "the fed decomposing hedge funds u s treasury exposures": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of The Fed - Decomposing Hedge Funds' U.S. Treasury Exposures in quantitative finance.",
    "the fed drivers of option implied interest rate volatility": "Analyzes the empirical dynamics, factor decomposition, and macroeconomic drivers of the sovereign yield curve.",
    "the fed robustness of long maturity term premium estimates": "Decomposes sovereign bond yields into short-rate expectations and duration risk premia using affine term structure models across macroeconomic cycles.",
    "the global dash for cash in march 2020 liberty street economics": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of The Global Dash for Cash in March 2020 - Liberty Street Economics in conformal prediction.",
    "the journal of": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of THE JOURNAL OF in conformal prediction.",
    "the rise of short dated options": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "the sec and cftc overhaul form pf": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of The SEC and CFTC Overhaul Form PF in quantitative finance.",
    "the term premium fred blog": "Decomposes sovereign bond yields into short-rate expectations and duration risk premia using affine term structure models across macroeconomic cycles.",
    "the term structure of monetary policy uncertainty": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of The Term Structure of Monetary Policy Uncertainty in fixed income.",
    "towards autonomous formulaic alpha discovery an evolutionary computation perspective": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "trade reporting frequently asked questions": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Trade Reporting Frequently Asked Questions in market microstructure.",
    "trading places my new view from inside the federal reserve": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Trading Places: My New View from Inside the Federal Reserve in quantitative finance.",
    "trading volatility as an asset class": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "transformer based time series forecasting for stock": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "transformer for times series an application to the s p500": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "transformers and large language model in healthcare a review pmc pubmed central": "Analyzes attention-based Transformer architectures and temporal self-attention mechanisms for financial time series forecasting.",
    "understanding short sale volume data on finra s website": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Understanding Short Sale Volume Data on FINRA's Website in market microstructure.",
    "venn pillar series 1 of 4 the practice of understanding portfolio risk with orthogonal factors": "Evaluates cross-sectional factor risk premia, multi-factor portfolio construction, and statistical methods to prevent backtest overfitting.",
    "volatility insights much ado about 0dtes evaluating the market impact of spx 0dte options": "Empirical study analyzing intraday volume, dealer delta/gamma hedging, and market stability effects of same-day expiration (0DTE) index options.",
    "what is the best risk measure in practice a comparison of standard measures": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of What Is the Best Risk Measure in Practice? A Comparison of Standard Measures in conformal prediction.",
    "what is the volatility risk premium": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "white paper shows volatility risk premium facilitated higher risk": "Investigates empirical option pricing dynamics, implied volatility surface kinematics, and systematic variance risk premium harvesting.",
    "why are interest rates so low part 4 term premium": "Decomposes sovereign bond yields into short-rate expectations and duration risk premia using affine term structure models across macroeconomic cycles.",
    "why etf growth is booming": "Analyzes ETF creation/redemption mechanics, authorized participant arbitrage dynamics, tax efficiency, and secondary market liquidity.",
    "why the term premium isn t as boring as it sounds": "Decomposes sovereign bond yields into short-rate expectations and duration risk premia using affine term structure models across macroeconomic cycles.",
    # Batch 4 Curated Research Papers
    "130 30 the new long only": "Andrew Lo's framework evaluating active extension strategies, short-borrow costs, and risk attribution within an integrated portfolio management paradigm.",
    "a census of the factor zoo": "Surveys hundreds of published empirical factor anomalies, evaluating multiple-testing hurdles and shrinkage methodologies to evaluate genuine risk premia.",
    "a comprehensive study of volatility forecasting using transformer based model": "Evaluates self-attention Transformer architectures for capturing long-range temporal dependencies and non-linear volatility regime shifts in financial time series.",
    "a deep reinforcement learning framework for optimal trade execution": "Applies Deep Q-Networks and Policy Gradients to solve multi-period trade execution and minimize implementation shortfall.",
    "a dynamic approach to pairs trading": "Formulates a continuous-time stochastic control and Kalman filtering framework to dynamically track time-varying hedge ratios in pairs trading.",
    "a financial time series denoiser based on diffusion model": "Applies generative diffusion models to financial time series denoising and feature extraction.",
    "a h premium and the shanghai hong kong stock connect": "Analyzes how the opening of Shanghai-Hong Kong Stock Connect altered liquidity dynamics and reduced cross-border price disparities between A-shares and H-shares.",
    "a history of commercially available risk model": "Surveys the historical development of commercial multi-factor risk models from early Barra systems to modern multi-asset risk management platforms.",
    "a machine learning approach to volatility forecasting": "Benchmarks gradient boosting and neural network models against GARCH specifications for predicting equity index realized volatility.",
    "a pairs trading strategy on fractionally cointegrated implied volatility of s p 500 equities": "Develops a statistical arbitrage pairs trading framework exploiting fractional cointegration in implied volatility surfaces of S&P 500 constituent options.",
    "a practitioner s guide to factor model": "CFA Institute foundational monograph detailing macroeconomic, fundamental, and statistical multi-factor risk models for equity portfolio management.",
    "a reality check for data snooping": "Halbert White's seminal Econometrica paper introducing the Bootstrap Reality Check to test for data-mining bias across large universes of trading strategies.",
    "a simple and reliable way to compute option based risk neutral distributions": "New York Fed research paper detailing a robust non-parametric interpolation methodology to extract risk-neutral probability density functions from option smile curves.",
    "a simple approximate long memory model of realized volatility": "Fulvio Corsi's seminal paper introducing the Heterogeneous Autoregressive Realized Volatility (HAR-RV) model based on daily, weekly, and monthly volatility horizons.",
    "a simple approximation of the continuous time garch 1 1 model": "Derives discrete-time convergence properties and analytical diffusion approximations for GARCH(1,1) continuous-time stochastic processes.",
    "a systematic approach to portfolio optimization a comparative study of reinforcement learning agents market signals and investment horizons": "Benchmarks deep reinforcement learning agents (PPO, A2C, DDPG) against classical mean-variance and risk-parity portfolio optimization frameworks.",
    "a test for superior predictive ability": "Peter Hansen's seminal Econometrica paper refining the Reality Check into the Superior Predictive Ability (SPA) test with studentized bootstrap statistics.",
    "a three factor model of the term structure with macroeconomic variables": "Decomposes the Treasury yield curve into level, slope, and curvature components within a macro-finance term structure framework.",
    "a tool kit for factor mimicking portfolios": "Presents an econometrically rigorous framework for constructing factor-mimicking tracking portfolios with minimized tracking error and turnover.",
    "a tool kit for factor mimicking portfolios1": "Presents an econometrically rigorous framework for constructing factor-mimicking tracking portfolios with minimized tracking error and turnover.",
    "a user s guide to sofr the alternative reference rates committee april 2019": "Alternative Reference Rates Committee (ARRC) guide detailing the transaction volume weighting, publication cadence, and compounding conventions of the Secured Overnight Financing Rate (SOFR).",
    "addressing the non stationarity and complexity of time series data for long term forecasts": "Investigates adaptive filtering and stationarity transformations to improve long-horizon econometric time series forecasting.",
    "adr premium its construction around crisis": "Investigates the behavior and breakdown of American Depositary Receipt (ADR) pricing premia relative to home-market underlying shares during financial crises.",
    "advanced statistical arbitrage with reinforcement learning": "Integrates deep Q-learning with statistical arbitrage mean-reversion signals to optimize dynamic entry and exit execution.",
    "affine term structure model theory and evidence": "Duffie and Kan's foundational mathematical framework for multi-factor affine term structure models of the zero-coupon yield curve.",
    "aima strategy paper 130 30 strategy": "AIMA whitepaper detailing the institutional portfolio mechanics, tracking error characteristics, and short-borrow dynamics of 130/30 active extension strategies.",
    "alphagpt human in the loop ai for quantitative investment": "Introduces Alpha-GPT, an interactive human-in-the-loop framework leveraging LLMs to translate investment hypotheses into formulaic alpha expressions.",
    "american options on dividend paying assets": "Broadie and Detemple's seminal paper deriving analytical upper and lower bounds for American options on assets with continuous and discrete dividend yields.",
    "an advanced ensemble deep learning framework for stock price prediction using vae transformer and lstm model": "Constructs an ensemble deep learning architecture combining Variational Autoencoders with Transformers and LSTMs for financial time-series forecasting.",
    "an alternative factor model on the cross section of expected stock return": "Hou, Xue, and Zhang's (HXZ) seminal paper proposing the q-factor model based on investment and profitability to explain empirical asset pricing anomalies.",
    "an analysis of cointegration on the daily spot exchange rate": "Empirically evaluates cointegration and vector error correction models across major foreign exchange spot pairs.",
    "an analysis of the longstaff schwartz algorithm for american option pricing": "Provides theoretical convergence proofs and finite-sample error bounds for the Longstaff-Schwartz Least-Squares Monte Carlo algorithm in high dimensions.",
    "an efficient calibration framework for volatility derivatives under rough volatility with jumps": "Constructs an efficient joint calibration framework for SPX options and VIX derivatives using rough fractional Brownian motion with compound Poisson jumps.",
    "an empirical analysis of 130 30 strategy": "Empirical study benchmarking 130/30 active extension portfolios against long-only and market-neutral implementations across various market regimes.",
    "an empirical examination of the cross section of equity return": "Fama and French's foundational study investigating how size, book-to-market, leverage, and E/P explain the cross-section of expected stock returns.",
    "an empirical investigation of the black scholes option pricing model": "Empirical study documenting systematic Black-Scholes pricing discrepancies across strike moneyness and maturity horizons.",
    "an empirical test of the arbitrage pricing theory": "Roll and Ross's foundational paper empirically testing Ross's Arbitrage Pricing Theory (APT) against cross-sectional equity returns.",
    "arbitrage free svi volatility surfaces": "Jim Gatheral's foundational framework establishing SVI parameter constraints to guarantee absence of static butterfly and calendar spread arbitrage.",
    "arbitrage pricing theory and the term structure of interest rate": "Applies Arbitrage Pricing Theory multi-factor asset pricing to model the equilibrium term structure of Treasury yields.",
    "asset pricing with cross sectional return dispersion": "Demonstrates that market-wide cross-sectional return dispersion is a priced risk factor commanding a significant equity risk premium.",
    "asset pricing with disagreement": "Hong and Stein's theoretical model showing that heterogeneous investor beliefs and short-sale constraints generate asset price bubbles and crash dynamics.",
    "bad beta good beta": "Campbell and Vuolteenaho's seminal paper decomposing equity beta into cash-flow beta (bad beta) and discount-rate beta (good beta).",
    "bakshi kapadia and madan 2003 risk neutral moment estimators": "Bakshi, Kapadia, and Madan's seminal framework deriving model-free analytical formulas to extract risk-neutral skewness and kurtosis from option prices.",
    "barriers to arbitrage and the cross section of expected returns": "Examines how idiosyncratic risk and institutional holding constraints prevent arbitrageurs from correcting equity mispricings.",
    "benchmark risk and the cross section of expected returns": "Investigates how fund manager benchmark tracking error risk distorts equilibrium asset prices and factor risk premia.",
    "beyond the factor zoo a machine learning approach to expected returns": "Applies autoencoders and neural networks to extract non-linear latent factor representations from large empirical asset pricing datasets.",
    "bid ask spreads and the cross section of stock returns": "Amihud and Mendelson's seminal paper demonstrating that expected equity returns are an increasing, concave function of bid-ask spreads.",
    "bootstrapping the early exercise boundary in the least squares monte carlo method": "Introduces a non-parametric bootstrapping technique to refine and stabilize early exercise boundary estimation in Least-Squares Monte Carlo derivatives pricing.",
    "can deep learning beat garch on volatility forecasting": "Empirically compares LSTM and Transformer deep learning models with classical GARCH specifications across multi-day volatility forecasting horizons.",
    "capital market equilibrium with restricted borrowing": "Black's foundational paper deriving the Zero-Beta Capital Asset Pricing Model when riskless borrowing is unavailable.",
    "challenges with using the black scholes model for pricing long maturity options": "Investigates parameter sensitivity and systematic pricing biases of Black-Scholes approximations when applied to long-maturity and discrete dividend equity options.",
    "cointegration and error correction representation estimation and testing": "Engle and Granger's Nobel Prize-winning foundational paper formalizing cointegration and Error Correction Models for non-stationary economic time series.",
    "common risk factors in the returns on stocks and bonds": "Fama and French's landmark 1993 study introducing the 3-factor equity model (Market, SMB, HML) and term structure bond factors.",
    "common stock delisting an empirical analysis of firms performance": "Empirically quantifies post-delisting shareholder recovery rates, bankruptcy outcomes, and financial distress indicators across US equity markets.",
    "convergence and biases of monte carlo estimates of american option prices using a parametric exercise rule": "Quantifies high-biased and low-biased dual Monte Carlo estimators for American option pricing under parametric exercise boundaries.",
    "cross sectional and time series determinants of momentum returns": "Examines how macroeconomic credit conditions and investor attention influence the profitability and crash risk of momentum strategies.",
    "cross sectional variation in stock returns": "Seminal empirical asset pricing study documenting the joint explanatory power of size, value, momentum, and profitability factors.",
    "cross validation for time series and quantitative trading": "Formulates Purged and Embargoed Combinatorial Cross-Validation (CPCV) to prevent information leakage and serial correlation bias in financial machine learning.",
    "data snooping and the cross section of expected returns": "Harvey, Liu, and Zhu's seminal paper demonstrating that hundreds of published factor anomalies are false discoveries due to multiple-testing data snooping without t-statistic hurdle adjustments.",
    "deep direct reinforcement learning for financial trading": "Deng et al.'s influential paper introducing recurrent deep reinforcement learning to directly optimize financial trading positions without separate price forecasting.",
    "deep learning enhanced calibration of the heston model a unified framework": "Constructs deep neural network surrogates to solve the inverse calibration problem of Heston stochastic volatility parameters in sub-millisecond latency.",
    "deep learning for market making": "Applies deep reinforcement learning to high-frequency limit order book market making, optimizing quote inventory dynamics.",
    "deep learning for portfolio optimization": "Surveys deep reinforcement learning and neural network architectures for dynamic multi-asset portfolio optimization.",
    "deep learning for time series forecasting a survey": "Authoritative survey detailing recurrent, convolutional, and attention-based deep learning architectures for time series forecasting.",
    "deep learning for vwap execution in crypto markets beyond the volume curve": "Applies recurrent neural networks and reinforcement learning to dynamic Volume-Weighted Average Price (VWAP) order execution under non-stationary liquidity regimes.",
    "deep reinforcement learning in quantitative finance a survey": "Surveys the mathematical formulations, state-action space designs, and empirical performance of deep RL in portfolio optimization and market making.",
    "deepsupp attention driven correlation pattern analysis for": "Introduces DeepSupp, an attention-based deep learning framework to detect and quantify dynamic support and resistance levels from limit order book data.",
    "delisted firms and momentum profits": "Investigates how excluding delisted firms induces severe survivorship and lookahead biases in empirical tests of cross-sectional momentum strategies.",
    "dense passage retrieval for open domain question answering": "Karpukhin et al.'s foundational paper introducing dual-encoder dense passage retrieval (DPR) for high-precision semantic text search.",
    "discrete time models for pricing financial derivatives": "Cox, Ross, and Rubinstein's seminal paper introducing the binomial option pricing model.",
    "dispersion trading using options": "Analyzes the mechanics, risk-return profile, and correlation monetization of option dispersion trading strategies on equity indices.",
    "do short sale constraints prevent arbitrage an analysis of the china a h share spread": "Examines how short-sale restrictions, capital account controls, and retail trading sentiment sustain persistent valuation premia in Chinese A-shares relative to H-shares.",
    "do stocks outperform treasury bills": "Hendrik Bessembinder's landmark empirical study demonstrating that the majority of individual US common stocks fail to beat Treasury bills due to extreme positive return skewness.",
    "does market microstructure affect stock returns": "Investigates how order flow toxicity, bid-ask spreads, and limit order book depth affect cross-sectional expected stock returns.",
    "dynamic factor model factor augmented vector autoregressions and structural vector autoregressions in macroeconomics": "Stock and Watson's authoritative survey on Dynamic Factor Models and Factor-Augmented Vector Autoregressions (FAVAR) in macroeconomic modeling.",
    "dynamic portfolio selection under regime switching": "Formulates continuous-time stochastic control models for optimal asset allocation under Markov regime-switching market environments.",
    "early exercise decision in american options with dividends stochastic volatility and jumps": "Analyzes optimal early exercise boundaries for American options under stochastic volatility and jump diffusion processes with discrete dividend schedules.",
    "empirical asset pricing via machine learning": "Gu, Kelly, and Xiu's landmark paper demonstrating that machine learning (gradient boosting, neural networks) significantly outperforms linear factor models in empirical asset pricing.",
    "empirical performance of alternative option pricing models": "Bakshi, Cao, and Chen's seminal study benchmarking stochastic volatility, stochastic interest rate, and jump option pricing models against market quotes.",
    "estimating bank trading risk a factor model approach": "NBER study developing a multi-factor risk model to decompose and stress-test commercial and investment bank trading book exposures.",
    "evaluating the performance of garch models": "Hansen and Lunde's influential study evaluating over 300 GARCH-family models against realized volatility benchmarks.",
    "expected returns and idiosyncratic risk": "Ang, Hodrick, Xing, and Zhang's seminal paper documenting the anomalous negative relation between idiosyncratic volatility and expected stock returns.",
    "extreme stock return skewness and the performance of individual stocks": "Empirically documents that aggregate stock market wealth creation is heavily concentrated in a tiny fraction of top-performing compounders while the median stock underperforms.",
    "factor investing and asset allocation a review": "Comprehensive survey reviewing multi-factor equity investing, factor crowding, and institutional portfolio implementation.",
    "factor momentum and cross sectional momentum": "Demonstrates that cross-sectional equity momentum is largely explained by momentum in factor portfolios.",
    "fast reliable pricing and calibration of the rough heston model": "Develops rapid Padé approximations and Adams-Bashforth discretization methods to calibrate rough Heston fractional volatility models.",
    "financial trading with deep reinforcement learning": "Empirically tests Deep Deterministic Policy Gradient (DDPG) and Proximal Policy Optimization (PPO) algorithms for continuous-action portfolio rebalancing.",
    "forecasting realized volatility with deep learning model an empirical study": "Empirically benchmarks LSTM, GRU, and Temporal Convolutional Networks against econometric HAR models for multi-horizon realized volatility forecasting.",
    "forecasting stock return volatility a comparative study": "Empirically benchmarks classical GARCH, Realized GARCH, and deep learning models on intraday and daily volatility forecasting.",
    "forecasting the cboe vix and skew indices using heterogeneous autoregressive model": "Applies Heterogeneous Autoregressive (HAR) models to forecast the joint dynamics and term structure interactions of the Cboe VIX and SKEW indices.",
    "generalized arbitrage free svi volatility surfaces": "Extends the Stochastic Volatility Inspired (SVI) parameterization to guarantee absence of static arbitrage across extreme strike and maturity asymptotes.",
    "generalized autoregressive conditional heteroskedasticity": "Tim Bollerslev's foundational paper introducing the GARCH model to capture volatility clustering and time-varying persistence in financial returns.",
    "hedging risk factors": "Formulates optimal factor-hedging algorithms to construct portfolios orthogonal to systematic style and macroeconomic factor risks.",
    "hedging with stochastic and local volatility": "Compares dynamic delta and vega hedging effectiveness between local volatility and stochastic volatility models under severe smile shifts.",
    "high frequency statistical arbitrage with machine learning": "Integrates deep learning and high-frequency limit order book features into statistical arbitrage models to capture non-linear micro-structure mean reversion.",
    "high frequency trading and price discovery": "Brogaard, Hendershott, and Riordan's seminal study showing that high-frequency trading firms contribute significantly to price discovery and trade in the direction of permanent price changes.",
    "hybrid search combining dense and sparse retrieval for effective search": "Evaluates reciprocal rank fusion algorithms combining sparse lexical BM25 retrieval with dense embedding vector search for high-accuracy information retrieval.",
    "identification of time varying factor model": "Develops econometric estimation and asymptotic inference procedures for high-dimensional factor models with time-varying factor loadings.",
    "implications of dynamic factor model for var analysis": "Stock and Watson's seminal paper introducing Dynamic Factor Models to extract latent macroeconomic drivers from high-dimensional time-series panels.",
    "implied volatility surfaces and volatility smile dynamics": "Gatheral's foundational text analyzing the geometry, asymptotic bounds, and calibration of implied volatility surfaces.",
    "information transmission from pre market to regular market": "Examines lead-lag relationships and cross-market price transmission between index futures, pre-market ETF trading, and cash equity opens.",
    "intertemporal capital asset pricing model": "Robert Merton's foundational continuous-time asset pricing model introducing state-variable hedging demands into the CAPM.",
    "intraday trading volume patterns of equity markets a study of us and european stock markets": "Empirically documents intraday U-shaped volume, volatility, and bid-ask spread distributions across US and European equity exchanges.",
    "is the united states a lucky survivor a hierarchical bayesian approach": "Wachter and van Binsbergen's study utilizing hierarchical Bayesian estimation to demonstrate that the high historical US equity premium reflects survivorship bias.",
    "limits of arbitrage": "Shleifer and Vishny's foundational paper demonstrating that specialized arbitrageurs face performance-based capital constraints that prevent them from eliminating asset mispricings during extreme dislocations.",
    "liquidity and stock return an empirical study": "Yakov Amihud's seminal paper introducing the Amihud Illiquidity measure based on absolute return per dollar trading volume.",
    "liquidity commonality and cross sectional return": "Empirically investigates systematic liquidity risk and co-movement of liquidity across individual equities.",
    "liquidity in the repo market during times of stress": "Examines money market fund collateral allocation, dealer intermediation constraints, and Federal Reserve standing repo facilities during liquidity crunches.",
    "liquidity risk and expected stock return": "Acharya and Pedersen's seminal study developing the Liquidity-Adjusted Capital Asset Pricing Model (LCAPM) and quantifying systemic liquidity risk premia.",
    "local volatility and dupire s equation": "Formulates Dupire's continuous-time partial differential equation to extract unique local volatility surfaces from continuous European option prices.",
    "local volatility dynamic model": "Analyzes the forward PDE dynamics and calibration stability of local volatility models across equity index volatility smile regimes.",
    "loosening the long only leash": "AQR whitepaper quantifying the efficiency gains, factor breadth expansion, and Sharpe ratio improvements of relaxing long-only constraints into 130/30 extension strategies.",
    "machine learning for option pricing an empirical investigation of network architectures": "Empirically evaluates feedforward networks, ResNets, and Physics-Informed Neural Networks (PINNs) for non-parametric option pricing surface estimation.",
    "machine learning for realized volatility forecasting with alternative data": "Integrates alternative data sources and gradient-boosted decision trees with HAR-RV models to improve multi-day realized volatility forecasts.",
    "machine learning in quantitative finance": "Comprehensive survey of machine learning algorithms for asset pricing, volatility forecasting, risk management, and algorithmic execution.",
    "macro factor mimicking portfolios": "Develops a systematic methodology for constructing factor-mimicking equity portfolios to hedge macroeconomic inflation and interest rate risk.",
    "macroeconomic variables and the term structure of interest rate": "Ang and Piazzesi's seminal work constructing a joint no-arbitrage affine term structure model incorporating inflation and macroeconomic growth factors.",
    "market making in electronic markets": "Avellaneda and Stoikov's seminal paper developing optimal high-frequency quoting strategies under inventory constraints and Poisson order arrivals.",
    "measuring liquidity commonality": "Analyzes the covariance of individual stock liquidity with market-wide liquidity using high-frequency intraday order book data.",
    "measuring the term premium in government bond yields": "Adrian, Crump, and Moench's (ACM) seminal New York Fed study constructing an affine dynamic term structure model to estimate high-frequency Treasury term premia.",
    "metadata filtering in vector databases for enterprise rag systems": "Analyzes pre-filtering and post-filtering indexing architectures in vector databases to enforce strict relational constraints during semantic search.",
    "model based reinforcement learning for algorithmic trading": "Develops model-based RL architectures incorporating environment transition dynamics to improve sample efficiency in financial trading strategies.",
    "model calibration in option pricing": "Reviews inverse problem regularization techniques and objective loss functions for stable option pricing model parameter calibration.",
    "model free boundaries of option time value and early exercise premium": "Derives model-free analytical bounds on American option time values and early exercise boundaries using no-arbitrage constraints and discrete cash flow mechanics.",
    "modeling the persistence of conditional variances": "Engle and Bollerslev's foundational work introducing Integrated GARCH (IGARCH) to formalize long-memory persistence in financial market variance.",
    "momentum strategies and risk": "Barroso and Santa-Clara's seminal paper demonstrating that managing the time-varying volatility of momentum strategies virtually eliminates momentum crashes.",
    "monte carlo methods for pricing financial options": "Surveys variance reduction techniques, quasi-Monte Carlo sequences, and path generation algorithms for multi-asset derivatives pricing.",
    "multiple testing and the false discovery rate in finance": "Applies Benjamini-Hochberg and Storey False Discovery Rate (FDR) adjustments to evaluate the statistical authenticity of published financial market anomalies.",
    "numerical solutions of american options with dividends using finite difference methods": "Formulates Crank-Nicolson and implicit finite difference PDE discretization schemes to price American options subject to discrete dividend payouts.",
    "off but not gone a study of nasdaq delistings": "Analyzes the frequency, corporate characteristics, and terminal investor losses associated with involuntary regulatory and distress delistings on Nasdaq.",
    "on multivariate financial time series classification": "Evaluates multivariate time-series classification algorithms for predicting directional market regimes and trend reversal probabilities.",
    "optimal execution of portfolio transactions": "Almgren and Chriss's seminal foundational paper formulating the optimal execution trajectory balancing permanent and temporary market impact against inventory risk.",
    "option pricing when underlying stock returns are discontinuous": "Robert Merton's foundational paper introducing the jump-diffusion option pricing model.",
    "overnight returns and intraday price dynamics": "Documents the persistent structural return disparity and mean-reversion characteristics between overnight market gaps and daytime intraday returns.",
    "pairs trading performance of a relative value arbitrage strategy": "Gatev, Goetzmann, and Rouwenhorst's foundational empirical study documenting the risk-adjusted returns and excess alpha of quantitative pairs trading in US equities.",
    "pairs trading quantitative methods and analysis": "Comprehensive monograph detailing distance, cointegration, and copula methods for quantitative pairs trading strategies.",
    "portfolio constraints and the fundamental law of active management": "Clarke, de Silva, and Thorley's foundational paper introducing the Transfer Coefficient (TC) to formalize the performance drag imposed by portfolio constraints.",
    "portfolio optimization the conditional value at risk as an alternative to the mean variance framework application on the german": "Rockafellar and Uryasev's framework applying Conditional Value at Risk (CVaR) minimization to optimize asset allocations under heavy-tailed return distributions.",
    "portfolio selection": "Harry Markowitz's foundational 1952 paper introducing Modern Portfolio Theory and mean-variance optimization.",
    "practical improvements to mean variance optimization for multi asset class portfolios": "Surveys shrinkage covariance estimation, resampled efficient frontiers, and factor constraints to mitigate error maximization in mean-variance portfolio optimization.",
    "predicting stock returns with machine learning": "Empirically benchmarks penalized regressions, tree ensembles, and deep neural networks for predicting out-of-sample cross-sectional stock returns.",
    "price discovery and trading after hours": "Barclay and Hendershott's seminal study analyzing price discovery efficiency, adverse selection costs, and informed trading dynamics in after-hours electronic trading sessions.",
    "price discovery in financial markets": "Surveys the market microstructure mechanisms, order flow dynamics, and information transmission across electronic financial markets.",
    "price discovery in pre opening periods": "Empirically investigates order book transparency, indicative uncrossing prices, and information revelation during pre-market auction sessions.",
    "pricing options from the point of view of a trader": "Stoikov and Saglam's practitioner paper examining how market maker inventory constraints and bid-ask spreads drive empirical option quote deviations from Black-Scholes.",
    "pseudo mathematics and financial charlatanism the misuse of math in finance": "Bailey, Borwein, López de Prado, and Zhu's influential paper exposing the statistical dangers of backtest overfitting and pseudo-mathematical optimization in quantitative finance.",
    "reinforcement learning for automated financial trading a review": "Comprehensive academic survey detailing Deep Q-Networks, Policy Gradients, and Actor-Critic architectures applied to algorithmic trading and execution.",
    "reinforcement learning in financial markets": "Surveys reinforcement learning applications in market making, algorithmic execution, and systematic portfolio rebalancing.",
    "retrieval augmented generation for knowledge intensive nlp tasks": "Lewis et al.'s seminal paper introducing Retrieval-Augmented Generation (RAG) combining pre-trained parametric language models with non-parametric dense vector index retrieval.",
    "revisiting the u shaped patterns in volatility and price impacts novel results using trade time estimates": "Utilizes trade-time transaction clocks to demonstrate that U-shaped intraday volatility is primarily driven by institutional order arrival clustering rather than calendar time.",
    "reviving the lost art of perturbation for exotic pricing": "Applies asymptotic perturbation theory to derive closed-form analytical approximations for exotic derivatives under complex stochastic volatility dynamics.",
    "risk and long run ipo returns": "Eckbo and Norli's empirical study examining long-run IPO underperformance and demonstrating that risk factor exposures explain post-offering equity returns.",
    "risk parity chartered alternative investment analyst association": "CAIA monograph detailing the equal risk contribution mathematical derivation, leverage implementation, and multi-asset portfolio benefits of Risk Parity.",
    "risk return and equilibrium empirical tests": "Fama and MacBeth's seminal 1973 paper introducing the two-pass cross-sectional regression methodology for testing asset pricing models.",
    "robust portfolio optimization": "Surveys robust optimization methodologies to protect mean-variance portfolios against parameter estimation error and covariance uncertainty.",
    "short dated smile under rough volatility asymptotics and numerics": "Derives small-time asymptotic expansions for implied volatility smiles under rough fractional volatility models with Hurst parameter H < 1/2.",
    "size and book to market factors in earnings and returns": "Fama and French's foundational study linking size and value factor returns to underlying fundamental firm profitability.",
    "skewness and the bubble": "Conrad, Dittmar, and Ghysels' empirical study analyzing risk-neutral skewness extracted from option prices to predict market bubble formations and crash probabilities.",
    "sofr and the transition away from libor": "Analyzes the structural design, transaction-level volume weighting, and market transition mechanics from LIBOR to the Secured Overnight Financing Rate (SOFR).",
    "sparse approximate factor model for high dimensional covariance matrix estimation and portfolio selection": "Develops sparse approximate factor models using L1-regularization to improve large covariance matrix estimation and minimum-variance portfolio selection.",
    "statistical arbitrage in the u s equities market": "Marco Avellaneda and Jeong-Hyun Lee's seminal paper developing a PCA-based statistical arbitrage framework with Ornstein-Uhlenbeck residual spread modeling.",
    "statistical arbitrage with cointegrated pairs": "Formulates state-space Kalman filter models to dynamically estimate cointegrating vectors in statistical arbitrage pairs trading.",
    "stock trading optimization through model based reinforcement": "Applies model-based reinforcement learning with world models to optimize sequential trade execution and risk-adjusted portfolio returns.",
    "support resistance levels towards profitability in intelligent algorithmic trading model": "Formalizes rule-based and clustering algorithms to identify high-probability support and resistance zones for algorithmic trading strategies.",
    "survivorship bias in performance studies": "Brown, Goetzmann, Ibbotson, and Ross's seminal paper quantifying how survivorship bias inflates historical mutual fund and hedge fund performance.",
    "taming tail risk regularized multiple β worst case cvar portfolio": "Develops a regularized multiple-beta robust optimization framework to minimize worst-case CVaR under distributional uncertainty and macro regime shifts.",
    "testing for cointegration with threshold autoregressive and smooth transition autoregressive model": "Develops non-linear threshold cointegration tests to model asymmetric mean reversion and transaction cost bands in statistical arbitrage spreads.",
    "the application of the black litterman model in a multi factor framework": "Extends the Black-Litterman model to express subjective and quantitative active views directly on orthogonal risk factor premia rather than asset classes.",
    "the asymmetric effects of good and bad volatility in the har model": "Patton and Sheppard's foundational study decomposing realized variance into upside and downside semi-variances to enhance HAR-RV volatility forecasting.",
    "the black litterman model extensions and asset allocation": "Comprehensive mathematical formulation of the Black-Litterman portfolio optimization framework incorporating Bayesian view integration and confidence parameterization.",
    "the capital asset pricing model theory and evidence": "Fama and French's classic paper reviewing the theoretical foundations and empirical failures of the single-factor Capital Asset Pricing Model (CAPM).",
    "the cboe skew index investigating the tail risk of s p 500 returns": "Cboe whitepaper detailing the mathematical methodology, cubic option portfolio replication, and tail-risk measurement of the Cboe SKEW Index.",
    "the cross section of expected stock returns": "Fama and French's landmark 1992 paper demonstrating that size and book-to-market equity factors absorb the role of market beta in explaining cross-sectional stock returns.",
    "the cross section of volatility and expected stock returns": "Ang, Hodrick, Xing, and Zhang's seminal study documenting the low-volatility anomaly and pricing of aggregate volatility risk.",
    "the deflated sharpe ratio": "Bailey and López de Prado's foundational paper introducing the Deflated Sharpe Ratio to correct for selection bias, non-normality, and multiple testing in backtests.",
    "the empirical foundations of factor investing": "Asness et al. (AQR) monograph detailing the economic rationale, long-term persistence, and implementation of value, momentum, carry, and defensive factors.",
    "the factor zoo": "Cochrane's Presidential Address highlighting the multidimensional explosion of published empirical asset pricing factor anomalies.",
    "the forward rate anomaly and the term structure of interest rates": "Examines the forward rate bias and the failure of the Uncovered Interest Parity hypothesis in fixed income and currency markets.",
    "the fundamental law of active management time series dynamics and cross sectional properties": "Marco Avellaneda's mathematical treatise extending the Grinold-Kahn Fundamental Law to incorporate dynamic factor decay and time-varying cross-sectional correlation.",
    "the information in the term structure of interest rate": "Mishkin's influential empirical study investigating the term structure's predictive power for future inflation and real economic activity.",
    "the intraday volatility of stock price": "Andersen and Bollerslev's seminal study utilizing high-frequency intraday returns to extract model-free realized volatility and filter diurnal market microstructure noise.",
    "the limits of arbitrage in equity markets": "Empirically tests Shleifer-Vishny limits of arbitrage in cross-sectional equity pricing anomalies.",
    "the long term risk of global stock markets": "Philippe Jorion and William Goetzmann's seminal study examining survivorship bias in global equity markets and documenting the high historical frequency of market breaks and capital wipeouts.",
    "the market for borrowing stock": "D'Avolio's seminal paper documenting short-sale supply constraints, borrow fees, and institutional lending dynamics in US equities.",
    "the mechanics of the treasury basis trade": "Federal Reserve Board study detailing the hedge fund cash-futures Treasury basis trade, repo leverage financing, and structural liquidity risks.",
    "the predictive power of pre market trading": "Analyzes institutional order imbalances and trading volume in pre-market electronic sessions as statistically significant predictors of regular market opening direction.",
    "the pricing of options and corporate liabilities": "Black and Scholes' landmark 1973 paper deriving the closed-form Black-Scholes formula for European option valuation.",
    "the probability of backtest overfitting": "López de Prado et al.'s seminal paper introducing Combinatorial Symmetric Cross-Validation (CSCV) to calculate the exact probability of backtest overfitting (PBO).",
    "the relation between return and market value of common stocks": "Rolf Banz's seminal 1981 paper documenting the empirical size anomaly where small-cap stocks earn higher risk-adjusted returns than large-cap stocks.",
    "the repo market and the financial crisis": "Gary Gorton and Andrew Metrick's foundational study demonstrating that runs on repo collateral haircut increases were the central systemic driver of the 2007-2008 banking crisis.",
    "the rough bergomi model from motivation to implementation": "Details the mathematical architecture, variance curve simulation, and fast Fourier pricing implementation of the rough Bergomi fractional volatility model.",
    "the stock bond correlation a tale of two days in the u s treasury bond market": "Jun Pan's study analyzing the time-varying stock-bond correlation and its regime shifts driven by inflation shocks and flight-to-safety liquidity demands.",
    "the structural plumbing of the dollar funding market": "Analyzes the interaction between domestic repo markets, FX swap funding lines, and central bank liquidity swap facilities.",
    "the svi arbitrage free volatility surface parameterization": "Gatheral and Jacquier's seminal paper formulating necessary and sufficient conditions for arbitrage-free SVI implied volatility surface parameterizations.",
    "the term structure of interest rates": "Surveys modern multi-factor affine and Heath-Jarrow-Morton (HJM) term structure models of interest rates.",
    "the theory of speculation": "Louis Bachelier's pioneering 1900 dissertation modeling asset prices with Brownian motion and formulating the first option pricing model.",
    "the three musketeers relationships between hong kong shanghai and shenzhen before and after shanghai hong kong stock connect": "Evaluates market integration, price discovery efficiency, and arbitrage convergence across Greater China equity exchanges following the launch of Stock Connect.",
    "the three types of factor model a comparison of their explanatory power": "Empirically compares the out-of-sample explanatory power and covariance estimation accuracy of macroeconomic, fundamental, and statistical factor models.",
    "the vanna volga method for derivatives pricing": "Formalizes the Vanna-Volga pricing and hedging methodology, decomposing exotic option prices into Black-Scholes values plus vega, vanna, and volga risk adjustments.",
    "the volatility smile": "Emanuel Derman and Iraj Kani's foundational work introducing implied tree models to capture the empirical volatility smile.",
    "time series momentum": "Moskowitz, Ooi, and Pedersen's seminal study documenting persistent 'trend' or time-series momentum across global equities, commodities, currencies, and bonds.",
    "time varying causalities in prices and volatilities between the cross listed stocks in chinese mainland and hong kong stock markets": "Applies time-varying Granger causality and asymmetric GARCH models to evaluate information flow and volatility transmission between dual-listed A-share and H-share equities.",
    "twin stock pricing puzzle": "Empirically analyzes persistent violations of the Law of One Price in dual-listed Royal Dutch/Shell and Unilever twin share structures.",
    "using monte carlo to value derivatives with early exercise": "Longstaff and Schwartz's foundational paper introducing Least-Squares Monte Carlo (LSM) for pricing American and Bermudan options via cross-sectional regression.",
    "value and momentum in factor momentum": "Demonstrates that factor portfolios exhibit strong time-series and cross-sectional momentum that drives underlying individual stock returns.",
    "valuing american options by simulation a simple least squares approach": "Seminal work establishing least-squares regression on basis functions to estimate continuation values in American option Monte Carlo pricing.",
    "vanna volga and smile consistent implied volatility surface of equity index option": "Analyzes the Vanna-Volga market quotation convention and its heuristic interpolation for constructing smile-consistent implied volatility surfaces in equity indices.",
    "volatility and correlation in quantitative finance": "Reghai's authoritative treatise on pricing and managing volatility and correlation derivatives in equity and multi-asset markets.",
    "volatility forecasting a review of the recent literature": "Comprehensive academic survey evaluating the empirical forecasting performance of GARCH-family, stochastic volatility, and realized volatility models across asset classes.",
    "volatility forecasting with neural networks": "Empirically evaluates recurrent and convolutional neural network architectures for predicting realized volatility from high-frequency intraday data.",
    "volatility model in practice rough path dependent or markovian": "Empirically benchmarks rough fractional volatility, path-dependent volatility, and Markovian stochastic volatility models on out-of-sample smile forecasting.",
    "volatility of the u s stock market return": "Schwert's seminal empirical analysis evaluating the macroeconomic drivers, recession linkages, and long-term historical dynamics of US stock market volatility.",
    "what is beta": "AQR whitepaper detailing the estimation, leverage scaling, and empirical nuances of equity beta in multi-factor investing.",
    "where have all the ipos gone the hard life of the small ipo": "Analyzes the long-term decline and high mortality rate of small-cap initial public offerings under increased regulatory and structural market pressures.",
    "why do companies delist voluntarily from the stock market": "Examines the financial, governance, and cost-benefit rationales behind corporate decisions to voluntarily terminate public stock exchange listings.",
    "zero beta capm": "Fischer Black's foundational paper deriving the equilibrium capital asset pricing model under borrowing restrictions.",

    # === Batch 5 Curated Research Papers ===
    # 1. Option-Implied Distributions, Breeden-Litzenberger & Volatility Smiles
    "how useful are implied distributions evidence from stock index option": "BIS empirical study evaluating the forecasting accuracy and subjective risk aversion adjustments of option-implied risk-neutral probability density functions.",
    "risk neutral densities a review": "Jackwerth's authoritative academic survey detailing parametric, spline, and kernel methodologies for extracting risk-neutral probability density functions from option prices.",
    "implied risk neutral distribution a comparison of estimation methods": "Warwick working paper benchmarking mixture of lognormals, kernel regression, and smoothed implied volatility smile methods for extracting risk-neutral distributions.",
    "some results on extracting and understanding the risk neutral returns distribution for the u s stock market": "Stephen Figlewski's study utilizing Generalized Extreme Value distributions to model the heavy tails and empirical skew of option-implied risk-neutral density functions.",
    "options and the gamma knife": "Ziemba and MacLean's study analyzing extreme negative gamma risk, capital preservation, and tail-loss amplification in short-dated options strategies.",
    "a simple and reliable way to compute option based risk neutral distributions": "New York Fed study developing a robust cubic spline interpolation methodology on implied volatility smiles to stably extract risk-neutral densities.",
    "extracting risk neutral probability distributions from option prices using trading volume as a filter": "IHS study using trade volume filtering and microstructure noise reduction to improve the calibration accuracy of risk-neutral density estimators.",
    "non structural approach to implied moments extraction": "Applies model-free non-structural numerical integration across option strikes to extract implied skewness and kurtosis moments directly from option price strips.",
    "methodology for estimating market probability density functions": "Federal Reserve Bank of Minneapolis methodology for estimating market-implied probability density functions across asset classes.",
    "extracting risk neutral probability densities by fitting implied volatility smiles": "ECB working paper calibrating smoothed implied volatility smile functions to extract risk-neutral densities from interest rate futures options.",
    "option implied probability distributions and currency excess returns": "New York Fed study demonstrating that higher-order risk-neutral moments extracted from currency options predict foreign exchange excess returns.",
    "understanding fx risk premium": "Swiss National Bank research paper analyzing variance risk premia, skewness, and jump risks in foreign exchange derivative markets.",
    "the role of risk neutral moments in forecasting future realised volatility an international perspective": "Demonstrates that higher-order risk-neutral moments (skewness, kurtosis) provide incremental predictive power for forecasting realized volatility across global equity indices.",
    "option implied risk neutral distributions and risk aversion": "CFA Institute Research Foundation monograph detailing how subjective risk aversion functions transform risk-neutral distributions into real-world physical probability forecasts.",
    "the information content of implied volatility from currency options": "BIS study evaluating the empirical forecasting power of currency option implied volatility for realized exchange rate movements.",
    "deriving option implied probability densities for foreign exchange markets": "Bank of England research paper outlining spline interpolation methodologies on option smile quotes to extract risk-neutral distributions.",
    "stochastic calculus for arbitrage free pricing with stochastic volatility": "Derives the Feynman-Kac connection and martingale pricing representation for continuous-time stochastic volatility models.",

    # 2. XGBoost, Tree Ensembles & Machine Learning Trading
    "option pricing using ensemble learning": "Evaluates ensemble gradient boosting and random forest architectures for non-parametric option pricing and implied volatility surface fitting.",
    "machine learning robustness a primer": "Surveys distributional shifts, adversarial robustness, and out-of-distribution generalization in financial machine learning models.",
    "analysis of the application of xgboost in exchange traded funds": "Applies XGBoost decision trees to model cross-sectional ETF return dynamics and constituent factor exposures.",
    "a machine learning based stock prediction system using xgboost and random forests": "Benchmarks gradient boosted decision trees against recurrent neural networks for equity price trend forecasting.",
    "evaluating machine learning classification for financial trading an empirical approach": "Empirically evaluates classification performance metrics, AUC-PR, and backtest profitability of machine learning classifiers in financial trading.",
    "comparing xgboost and lstm model for prediction of stock price direction": "Compares XGBoost gradient boosting against LSTM recurrent networks for predicting directional price movement in individual equities.",
    "comparative analysis of xgboost algorithm and linear regression in predicting the trend of investor overreaction": "Analyzes non-linear investor overreaction and behavioral mean-reversion using XGBoost decision tree architectures.",
    "haelt a hybrid attentive ensemble learning transformer framework for high frequency stock price forecasting": "Proposes a hybrid framework combining Transformer self-attention with gradient boosted ensemble learning for high-frequency limit order book forecasting.",
    "financial distress early warning from a systemic risk perspective based on the adaptive weighted xgboost bagging model": "Develops an adaptive weighted XGBoost-Bagging ensemble model for corporate financial distress early warning and default probability estimation.",
    "advancing financial analytics integrating xgboost lstm and random forest algorithms for precision forecasting of corporate financial distress": "Integrates XGBoost, Random Forests, and LSTM architectures to forecast corporate credit distress and bankruptcy likelihood.",
    "xgboost based multi factor stock selection model for rotational trading": "Develops an XGBoost multi-factor ranking model for sector and equity rotational trading strategies.",
    "a refined methodological approach long term stock market forecasting with xgboost": "Investigates feature engineering and hyperparameter optimization for multi-horizon equity return forecasting using XGBoost.",
    "stock price prediction using a hybrid lstm gnn model": "Combines Graph Neural Networks with LSTM sequence models to capture cross-stock supply chain and industry correlation graphs in equity price prediction.",
    "lstm vs transformers in banking forecasting": "Empirically benchmarks LSTM recurrent models against self-attention Transformers for multi-horizon banking time-series forecasting.",
    "financial time series analysis with transformer model": "Evaluates Transformer sequence architectures for financial time series denoising, volatility modeling, and trend forecasting.",
    "a method for evaluating the interpretability of machine learning model in predicting bond default risk based on lime and shap": "Applies SHAP values and LIME feature attribution to explain non-linear machine learning predictions of corporate bond default risk.",
    "less discriminatory alternative and interpretable xgboost framework for binary classification": "Develops an interpretable tree-regularized XGBoost framework ensuring fair and explainable credit risk classification.",
    "comprehensive analysis of random forest and xgboost performance with smote adasyn and gnus under varying imbalance levels": "Evaluates synthetic oversampling techniques (SMOTE, ADASYN) with tree ensembles for classification under severe class imbalance.",
    "a robust machine learning approach for credit risk analysis of large loan level datasets": "BIS study evaluating XGBoost and deep neural networks on granular loan-level portfolios for macroprudential stress testing.",
    "a kernel based perspective for why transformers fail to generalize on time series forecasting and beyond": "Provides theoretical kernel analysis explaining why standard Transformer self-attention fails on non-stationary, low signal-to-noise financial time series.",
    "transformers versus lstms for electronic trading": "Benchmarks Transformer attention mechanisms against LSTMs for high-frequency limit order book trend forecasting and execution.",
    "mm itransformer a multimodal approach to economic time series forecasting with textual data": "Develops MM-iTransformer to integrate multi-modal textual sentiment embeddings with inverted Transformer variate-attention for macroeconomic time series forecasting.",
    "crypto price prediction using lstm and xgboost": "Evaluates hybrid LSTM and XGBoost models for predicting high-volatility cryptocurrency price trends.",
    "support for stock trend prediction using transformers and sentiment analysis": "Integrates financial news sentiment embeddings with Transformer sequence encoders for directional stock trend prediction.",
    "plutus a well pre trained large unified transformer can unveil financial time series regularities": "Pre-trains a large foundation Transformer model on multi-market financial time series to capture universal price dynamics and cross-asset transferability.",
    "stockformer a swing trading strategy based on stl decomposition and self attention networks": "Combines STL time-series decomposition with self-attention networks to extract swing trading signals across market frequencies.",
    "does self attention need separate weights in transformers": "Investigates weight-sharing mechanisms in Transformer self-attention layers to improve parameter efficiency and reduce overfitting in time series modeling.",
    "a financial time series prediction model based on multiplex attention and linear transformer structure": "Develops multiplex attention mechanisms with linear time complexity for scalable financial time series forecasting.",
    "trading on uncertainty futurequant transformer s distribution based strategy for futures markets": "Formulates FutureQuant Transformer to output full predictive probability distributions for probabilistic risk management in futures trading.",
    "an end to end llm enhanced trading system": "Architects an end-to-end quantitative trading system utilizing LLM reasoning agents for alpha signal generation and execution control.",

    # 3. Transformers in Systematic Trading & Foundation Models
    "transformer based model for stock price prediction a comprehensive review": "Comprehensive academic survey detailing Transformer self-attention architectures and temporal feature extractors for stock price prediction.",
    "temporal fusion transformers for interpretable multi horizon time series forecasting": "Bryan Lim et al.'s seminal paper introducing Temporal Fusion Transformers (TFT) combining self-attention with gating mechanisms for multi-horizon time series forecasting.",
    "informer beyond efficient transformer for long sequence time series forecasting": "Seminal paper introducing the ProbSparse attention mechanism in Informer to reduce time complexity for long sequence time-series forecasting.",
    "a time series is worth 64 words long term forecasting with transformers": "Introduces PatchTST, demonstrating that patching time-series subseries into tokens significantly enhances Transformer forecasting accuracy while reducing compute.",
    "crossformer transformer utilizing cross dimension dependency for multivariate time series forecasting": "Develops Crossformer to explicitly capture cross-time and cross-variable dependencies in multivariate financial time series.",
    "itransformer inverted transformers are effective for time series forecasting": "Introduces the inverted Transformer architecture (iTransformer) applying attention across variates rather than time steps for multivariate forecasting.",
    "autoformer decomposition transformers with auto correlation for long term series forecasting": "Introduces Autoformer with auto-correlation mechanisms and series decomposition blocks for long-term time series forecasting.",
    "time llm time series forecasting by reprogramming large language model": "Proposes reprogramming pre-trained text LLMs with patch reprogramming and domain prompts for zero-shot and few-shot time series forecasting.",
    "are transformers effective for time series forecasting": "Seminal paper demonstrating that simple single-layer linear models (DLinear) often outperform complex Transformer architectures on standard time series benchmarks.",
    "transformers in time series a survey": "Comprehensive survey reviewing architectural adaptations, positional encodings, and attention modifications for time series Transformers.",
    "deep transformer model for time series forecasting": "Surveys deep multi-layer Transformer sequence-to-sequence architectures for multi-horizon forecasting.",
    "tlob a novel transformer model with dual attention for stock price trend prediction with limit order book data": "Develops a dual-attention Transformer model to capture spatial level-depth correlations and temporal order arrival dynamics in limit order books.",
    "deep learning in long short stock portfolio allocation an empirical study": "Empirically benchmarks deep neural network architectures for long-short cross-sectional equity portfolio construction and risk-adjusted alpha.",
    "stockformer a price volume factor stock selection model based on wavelet transform and multi task self attention networks": "Combines wavelet decomposition with multi-task self-attention networks to extract multi-frequency price-volume alpha signals.",
    "economic predictions with big data the illusion of sparsity": "Giannone, Lenza, and Primiceri's seminal paper showing that economic and financial prediction models favor dense shrinkage over sparse feature selection.",
    "a sparsity based model of bounded rationality": "Xavier Gabaix's foundational framework modeling how economic agents optimize decision-making under attention constraints by building sparse mental models.",

    # 4. Formulaic Alphas, Genetic Programming & Alpha Decay
    "alpha mining and enhancing via warm start genetic programming for quantitative investment": "Proposes warm-start genetic programming to accelerate formulaic alpha factor discovery and mitigate premature convergence.",
    "quantfactor reinforce mining steady formulaic alpha factors with variance bounded reinforce": "Applies variance-bounded policy gradient reinforcement learning to discover robust, low-decay formulaic alpha factors.",
    "autoalpha an efficient hierarchical evolutionary algorithm for mining alpha factors in quantitative investment": "Introduces AutoAlpha, a hierarchical evolutionary algorithm for mining formulaic alpha factors in quantitative investment.",
    "synergistic formulaic alpha generation for quantitative trading based on reinforcement learning": "Formulates synergistic multi-agent reinforcement learning to generate mutually orthogonal formulaic alpha signals.",
    "combining factors in multifactor portfolios": "Analyzes portfolio construction tradeoffs between integrated multi-factor scoring versus mixing standalone factor sleeves.",
    "understanding alpha decay": "Quantifies the mathematical relationship between signal turnover, crowding, implementation costs, and the half-life of quantitative alpha.",

    # 5. Futures Market Anomalies, Delivery Options & Basis Trading
    "when benchmarks fail the causes and consequences of negative oil prices": "Wharton study analyzing the structural failure of physical storage capacity and negative price settlement in WTI crude oil futures in April 2020.",
    "on the negative pricing of wti crude oil futures": "Empirically investigates order book microstructure, retail ETF roll dynamics, and negative pricing mechanics in WTI futures.",
    "debunking the roll yield myth in futures markets": "Exposes the economic fallacy of viewing roll yield as a standalone return generator rather than an artifact of spot price mean reversion and storage costs.",
    "deconstructing futures returns the role of roll yield": "CME whitepaper decomposing commodity and financial futures returns into spot price changes, roll yield carry, and collateral yield.",
    "embedded theoretical quality option pricing in treasury bond futures": "Models the theoretical quality option embedded in Treasury bond futures arising from conversion factor deviations.",
    "the pricing of treasury bond futures the quality variation option": "Michael Hemler's seminal study deriving analytical bounds and pricing formulas for the cheapest-to-deliver quality variation option in Treasury bond futures.",
    "treasury futures delivery options basis spreads and delivery tails": "Deconstructs the cheapest-to-deliver switch option, delivery timing option, and basis trading dynamics in US Treasury futures.",
    "financial stability risks from basis trades in the us treasury and euro area government bond markets": "ECB study analyzing hedge fund sovereign bond basis trade leverage, repo financing dependencies, and systemic market liquidity risks.",

    # 6. Autocallable Notes & Structured Products
    "hedging and pricing structured products featuring multiple underlying assets": "Develops deep learning and multi-asset local volatility models for pricing and hedging multi-underlying autocallable structured products.",
    "domain knowledge preservation in financial machine learning": "Investigates incorporating no-arbitrage boundary conditions and financial domain constraints into machine learning pricing architectures.",
    "improving risk management and analysis of structured notes through path dependence greeks and machine learning": "Applies machine learning approximations to evaluate path-dependent barrier Greeks and autocallable redemption probabilities.",
    "are issuer margins fairly stated evidence from the issuer estimated value for retail structured products": "Empirically quantifies hidden embedded issuer fees and secondary market markdown discounts in retail structured products.",

    # 7. Private Credit & Systemic Leverage
    "bank lending to private credit size characteristics and financial stability implications": "Federal Reserve study analyzing bank exposure to private credit funds through subscription lines, NAV loans, and collateralized credit facilities.",
    "could the growth of private credit pose a risk to financial system stability": "Federal Reserve Bank of Boston study evaluating private debt illiquidity, fund leverage, and systemic interconnectedness with the banking sector.",
    "private credit characteristics and risks": "Federal Reserve analysis detailing direct lending borrower characteristics, debt service coverage ratios, and covenant-lite loan terms.",
    "private credit risk management in evergreen funds": "CAIA research paper examining liquidity mismatches, gating mechanisms, and valuation smoothing in perpetual evergreen private credit funds.",
    "private markets public risk financial stability implications of alternative funding sources": "ECB assessment analyzing the macroprudential implications and non-bank financial intermediation risks of private debt expansion.",
    "the global drivers of private credit": "BIS study analyzing the macroeconomic drivers, regulatory capital arbitrage, and institutional asset allocation shifts fueling private debt growth.",
    "markets systemic risk and the subprime mortgage crisis": "Schwarcz's legal and economic analysis examining structural complexity, moral hazard, and systemic liquidity contagion during the 2008 financial crisis.",
    "household leverage before and after the great recession time series versus cross sectional evidence": "Examines the role of credit expansion, collateral constraints, and household debt overhang in macroeconomic recessions.",

    # 8. SAA / TAA Performance Attribution
    "performance measurement and attribution foundations and frameworks": "CFA Institute monograph detailing the mathematics of Brinson-Fachler asset allocation and security selection attribution models.",
    "risk adjusted performance attribution and portfolio optimisations under tracking error constraints": "Develops risk-adjusted active performance attribution frameworks for benchmark-relative portfolios subject to tracking error limits.",
    "performance attribution in private equity a case study of two north american pension funds": "CAIA research study formulating multi-period factor attribution models tailored to illiquid private equity fund investments.",

    # 9. Portfolio Optimization, Robust Estimation & Execution Impact
    "portfolio selection problem using cvar risk measures equipped with metaheuristic optimization": "Applies metaheuristic algorithms and Conditional Value-at-Risk (CVaR) minimization to solve non-convex portfolio selection problems.",
    "portfolio optimization problems with cardinality constraints": "Analyzes mixed-integer quadratic programming algorithms for mean-variance portfolio optimization with cardinality and transaction cost constraints.",
    "an empirical comparison between robust estimation and robust optimization for mean variance portfolios": "Compares robust covariance estimators (Ledoit-Wolf) against robust optimization uncertainty sets for mitigating portfolio estimation risk.",
    "resampled efficient frontier integration for multi objective evolutionary algorithms": "Integrates Michaud's resampled efficient frontier framework into multi-objective evolutionary algorithms to reduce portfolio turnover.",
    "testing strategies based on multiple signals": "Robert Novy-Marx's influential paper detailing multiple testing corrections and false discovery rates when evaluating multi-signal quantitative strategies.",
    "trading volume alpha": "Empirically documents the cross-sectional return predictability of turnover and abnormal trading volume across equity markets.",
    "three models of market impact": "Jim Gatheral's foundational paper analyzing temporary, permanent, and transient market impact models and proving no-dynamic-arbitrage conditions.",
    "multi period portfolio optimization using model predictive control": "Applies model predictive control (MPC) to multi-period mean-variance and risk parity portfolio rebalancing under dynamic transaction costs.",
    "industry grade deep reinforcement learning for portfolio optimization": "Develops an industrial-grade deep reinforcement learning framework incorporating execution slippage and turnover constraints for multi-asset allocation.",
    "esg constraints in portfolio optimization": "Quantifies the efficient frontier tracking error and Sharpe ratio penalty imposed by ESG screening constraints on mean-variance portfolios.",
    "a multi period optimization framework for portfolio selection using interval analysis": "Develops an interval-analysis optimization framework to handle bounded parameter uncertainty in multi-period portfolio selection.",
    "multi objective portfolio optimization via gradient descent": "Formulates multi-objective gradient descent to trace continuous Pareto efficient frontiers balancing return, risk, and transaction costs.",

    # 10. Sell-Side Research Biases & Market Epistemology
    "mifid ii unbundling and sell side analyst research": "NYU Stern study examining how MiFID II research unbundling impacted sell-side analyst coverage, research quality, and market efficiency.",
    "target price accuracy of sell side analysts evidence from india": "Evaluates the forecasting accuracy and optimism bias of sell-side equity analyst target prices across emerging markets.",
    "analysts set price targets using trailing p e ratios": "Demonstrates that sell-side analyst price targets are overwhelmingly derived from heuristic trailing P/E multiples rather than DCF valuation models.",
    "financial analyst characteristics and herding behavior in forecasting": "Analyzes how analyst experience, brokerage reputation, and career concerns drive herding behavior toward consensus earnings forecasts.",
    "determinants of herding behavior among financial analysts": "Investigates macroeconomic uncertainty and institutional incentives as primary drivers of analyst consensus herding.",
    "do sell side analysts say buy while whispering sell": "NBER study demonstrating that sell-side analysts privately convey negative sentiment to institutional clients while issuing public buy recommendations.",
    "institutional investor attention and underreaction to news": "Zhi Da et al.'s study utilizing Bloomberg search volume to measure institutional investor attention and quantify underreaction to corporate news.",
    "disruption in the market for information mifid ii and investor relations": "Examines how MiFID II unbundling reduced small-cap research coverage and increased corporate spending on direct investor relations.",

    # 11. Technical Analysis Formalization & Deep RL Trading
    "foundations of technical analysis computational algorithms statistical inference and empirical implementation": "Andrew Lo, Harry Mamaysky, and Jiang Wang's seminal study developing non-parametric kernel regressions to mathematically formalize and test technical chart patterns.",
    "a comprehensive analysis of machine learning model for algorithmic trading of bitcoin": "Evaluates machine learning classifiers and feature importance metrics for high-volatility cryptocurrency algorithmic trading.",
    "comparative analysis of machine learning techniques in financial risk assessment": "Compares tree-based ensembles, support vector machines, and neural networks for financial credit risk and default probability prediction.",
    "stock market trading via actor critic reinforcement learning and adaptable data structure": "Develops actor-critic deep reinforcement learning agents with dynamic state representations for automated equity trading.",
    "supervised learning approaches for sentiment analysis in stock market predictions": "Evaluates supervised NLP models and financial domain lexicons for extracting predictive market sentiment signals.",
    "portfolio dynamic trading strategy using deep reinforcement learning": "Applies deep deterministic policy gradient (DDPG) agents to optimize continuous-action multi-asset portfolio weights.",
    "reinforcement learning meets technical analysis combining moving average rules for optimal alpha": "Combines reinforcement learning state-action policies with classical moving average crossover rules to optimize trade timing and drawdown control.",
    "machine learning methods to exploit the predictive power of open high low close ohlc data": "University College London study developing machine learning feature transformations on candlestick OHLC price dynamics.",
    "fintsbridge a new evaluation suite for real world financial prediction with advanced time series model": "Introduces a standardized benchmark evaluation suite for testing state-of-the-art deep time-series models on real-world financial data.",
    "machine learning for financial risk management a survey": "Comprehensive survey detailing machine learning applications in market risk, credit risk, operational risk, and systemic stress testing.",
    "towards designing a generic and comprehensive deep reinforcement learning framework for financial trading": "Architects a modular deep reinforcement learning framework incorporating execution delay, transaction friction, and risk penalties.",
    "an improved reinforcement learning model based on sentiment analysis": "Integrates financial news sentiment embeddings into deep Q-learning reward functions for equity trading.",
    "a survey on machine learning model for financial time series forecasting": "Surveys statistical learning, RNNs, CNNs, and Transformer models for financial asset return and volatility forecasting.",

    # 12. Corporate Insider Trading Signals & Transparency
    "the legal implications of insider trading and market manipulation": "Examines corporate governance mechanisms, blackout periods, and compliance frameworks for mitigating illegal insider trading and market manipulation.",
    "the unintended consequences of forcing insider trading transparency": "Duke Fuqua study analyzing how mandatory insider reporting transparency affects informed trading dynamics and corporate disclosure policies.",
    "insider trading and investor sentiment": "Empirically tests how corporate insider buying and selling behavior interacts with market-wide retail sentiment regimes.",
    "inferring bad news from insider sales": "Isolates informational bad news from liquidity-driven insider sales by conditioning on corporate earnings disclosure calendars.",
    "are insiders trades informative": "Josef Lakonishok and Inmoo Lee's seminal NBER study demonstrating that aggregate insider purchases strongly predict future equity market returns, especially in small-cap stocks.",
    "estimating the returns to insider trading": "Leslie Jeng, Andrew Metrick, and Richard Zeckhauser's seminal study quantifying abnormal returns to corporate insider purchase portfolios.",
    "insider sentiment and market returns international evidence": "Documents international cross-country evidence on the predictive power of corporate insider net buying for aggregate stock market returns.",
    "investor attention and insider trading": "Empirically demonstrates how corporate insiders strategically time stock sales during periods of elevated retail investor attention.",
    "insider trading in connected firms during trading bans": "Analyzes shadow insider trading where informed executives trade in economically connected peer companies during firm blackout windows.",
    "flaws in oversight and regulation of corporate insider trading": "University of Michigan study identifying structural enforcement gaps and opportunistic timing in Rule 10b5-1 executive trading plans.",

    # 13. Volume Price Analysis, VWAP & Algorithmic Execution
    "the impact of trading volume on portfolio momentum strategy": "Examines how trading volume interaction modifies the formation and holding period profitability of price momentum strategies.",
    "the effect of trading volume on stock price dynamics": "Empirically investigates the lead-lag relationship and price impact between trading volume spikes and equity price reversals.",
    "vwap execution as an optimal strategy": "Jim Gatheral's study formulating the optimal execution trajectory for Volume-Weighted Average Price (VWAP) tracking under dynamic order flow.",
    "conviction and volume measuring the information content of hedge fund trading": "Harvard study demonstrating that concentrated, high-volume hedge fund institutional positioning conveys significant long-term alpha.",
    "forecasting intraday volume in equity markets with machine learning": "Develops machine learning models to forecast U-shaped intraday volume profiles and volume arrival bursts for algorithmic execution.",
    "a comparative study of machine learning algorithms for stock price prediction using insider trading data": "Benchmarks supervised learning models incorporating Form 4 insider trading volume features for equity return prediction.",
    "hybrid machine learning model for long term stock market prediction": "Combines convolutional feature extractors with recurrent networks to forecast long-term equity trends from volume-price matrices.",
    "a novel ensemble deep learning model for stock prediction based on technical indicators": "Develops an ensemble deep neural architecture integrating price-volume momentum oscillators for directional trend forecasting.",

    # 14. Deep Hedging, Alternative Data & Systematic Quant Architectures
    "empirical deep hedging": "Evaluates the real-world performance of deep neural network hedging policies calibrated to empirical option order flow and transaction costs.",
    "a deep reinforcement learning approach to automated stock trading using xlstm networks": "Applies extended LSTM (xLSTM) architectures within deep reinforcement learning for automated equity portfolio execution.",
    "deep hedging with reinforcement learning a practical framework for option risk management": "Develops a reinforcement learning framework for non-parametric dynamic option hedging under market frictions and discrete liquidity.",
    "is the difference between deep hedging and delta hedging a statistical arbitrage": "HEC Montréal study proving that deep hedging strategies exploit empirical volatility smile mispricings relative to classical Black-Scholes delta hedging.",
    "deep hedging under market frictions a comparison of drl model for options hedging with impact and transaction costs": "Benchmarks Actor-Critic, PPO, and DDPG reinforcement learning architectures for option hedging subject to permanent market impact and spread costs.",
    "mining credit card data for stock returns": "Empirically tests the predictive power and alpha decay of alternative consumer credit card transaction data for estimating firm quarterly sales.",
    "looking under the bonnet short term strategy": "Man AHL quantitative research paper detailing signal construction, turnover management, and execution latency in short-horizon systematic strategies.",
    "advanced methods in portfolio optimization for trading strategy and smart beta": "Imperial College treatise evaluating shrinkage covariance estimation and risk parity allocations across smart beta factor strategies.",
    "quantitative portfolio management review and outlook": "Comprehensive survey detailing the evolution of quantitative portfolio management from factor investing to deep learning and alternative data.",
    "a machine learning approach to regime modeling": "Two Sigma research paper applying unsupervised clustering and hidden Markov models to identify macroeconomic and market volatility regimes.",
    "artificial intelligence textual analysis and hedge fund performance": "Evaluates how quantitative hedge funds deploying NLP textual analysis and machine learning generate superior risk-adjusted alpha.",
    "alpha gpt 2 0 human in the loop ai for quantitative investment": "Introduces Alpha-GPT 2.0, an interactive LLM system enabling human-in-the-loop quantitative alpha mining and factor backtesting.",
    "an explainable deep learning approach for stock market trend prediction": "Develops an attention-based explainable deep learning architecture to interpret feature importance in equity trend prediction.",

    # 15. Strategy Decay, Regime Shifts & The Peso Problem
    "measuring strategy decay risk minimum regime performance and the durability of systematic investing": "Fabozzi and Alexander's study introducing minimum regime performance metrics to quantify alpha decay risk and systematic strategy durability across macro environments.",
    "why static portfolios fail when risk regimes change": "CFA Institute study analyzing how fixed asset allocation weights suffer severe drawdown acceleration during macroeconomic regime transitions.",
    "the peso problem in financial economics": "Martin Evans' treatise defining the peso problem where rational expectations of rare, severe disasters distort empirical asset return distributions.",
    "challenges in macro finance modeling": "Federal Reserve research paper analyzing non-linear structural breaks and term premium dynamics in macro-finance equilibrium models.",
    "hierarchical ai multi agent fundamental investing evidence from china s a share market": "Develops a hierarchical multi-agent LLM framework simulating analyst debates and fundamental valuation in China's A-share market.",

    # 16. Financial RAG Architectures & LLMs
    "rag for finance automating document analysis with llms": "CFA Institute report detailing production patterns, prompt engineering, and document chunking for financial retrieval-augmented generation.",
    "retrieval augmented large language model for financial time series forecasting": "Develops RAG frameworks that retrieve historical similar macroeconomic and volatility market regimes to guide LLM time series forecasting.",
    "retrieval augmented generation for fintech agentic design and evaluation": "Presents an agentic multi-stage RAG architecture incorporating automated self-evaluation guardrails for financial technology systems.",
    "p1gpt a multi agent llm workflow module for multi modal financial information analysis": "Develops a multi-agent LLM system for parsing and cross-referencing multi-modal financial statements, tables, and earnings call audio.",
    "assessing rag system capabilities on financial documents": "ACL FinNLP benchmark evaluating retrieval precision, numerical factual consistency, and hallucination rates of RAG systems on financial 10-K filings.",
    "hierfinrag hierarchical multimodal rag for financial document understanding": "Proposes a hierarchical multimodal RAG framework that preserves tabular structure and document hierarchy in annual corporate reports.",
    "smartfinrag interactive modularized financial rag system": "Develops an interactive modularized RAG architecture featuring adaptive chunking and dynamic query expansion for financial question answering.",
    "evaluating retrieval augmented generation model for financial report question and answering": "Benchmarks dense semantic embeddings, hybrid BM25 retrieval, and re-ranking models on financial statement QA accuracy.",
    "llm output drift cross provider validation and mitigation for financial workflows": "Quantifies stochastic output drift across LLM provider updates and proposes deterministic consensus validation for compliance workflows.",
    "bayesian rag uncertainty aware retrieval for reliable financial question answering": "Formulates a Bayesian retrieval framework to quantify epistemic retrieval uncertainty and prevent hallucinated answers on financial disclosures.",
    "raptor recursive abstractive processing for tree organized retrieval": "Introduces RAPTOR, a tree-organized retrieval method that recursively clusters and summarizes text chunks for multi-level hierarchical retrieval.",
    "long context vs rag for llms an evaluation and revisits": "Empirically benchmarks native long-context window LLMs against retrieval-augmented generation across document retrieval and reasoning tasks.",
    "knowledge graphs and their applications in finance": "Surveys entity extraction, relational link prediction, and enterprise knowledge graph architectures in financial risk management.",
    "trade offs in financial ai explainability in a trilemma with accuracy and compliance": "Analyzes the structural trilemma between predictive accuracy, model explainability, and regulatory compliance in financial AI systems.",
    "explainable ai in finance addressing the needs of diverse stakeholders": "CFA Institute monograph evaluating feature attribution methods (SHAP, IG) and compliance frameworks for AI systems in asset management.",
    "targeting the core a simple and effective method to attack rag based agents via direct llm manipulation": "Investigates prompt injection vulnerabilities, vector database poisoning, and adversarial retrieval manipulation in agentic RAG architectures.",

    # 17. Recommender Systems & Social Sentiment
    "deep learning based recommender system a survey and new perspectives": "Comprehensive survey detailing deep collaborative filtering, autoencoders, and attention mechanisms in modern recommender systems.",
    "quantitative stock selection model using graph learning and a spatial temporal encoder": "Develops spatial-temporal graph neural networks to model inter-firm supply chain relationships and cross-asset momentum spillovers.",
    "stock market prediction using machine learning and deep learning architectures": "Benchmarks convolutional neural networks and recurrent models for predicting equity price direction from high-frequency technical indicators.",
    "new quantitative approaches to asset selection and portfolio construction": "Columbia University dissertation developing non-linear machine learning factor models and robust portfolio optimization algorithms.",
    "investment portfolio optimization based on modern portfolio theory and deep learning model": "Integrates deep learning return forecasts into classical Markowitz mean-variance and Black-Litterman portfolio optimization frameworks.",
    "a portfolio recommendation system based on machine learning and big data analytics": "Develops a hybrid collaborative filtering and multi-factor scoring system for personalized asset allocation recommendations.",
    "regulating ai in financial services legal frameworks and compliance challenges": "Analyzes international regulatory frameworks, algorithmic accountability, and compliance governance for AI models in financial services.",

    # 18. Index Futures & Microstructure
    "the impact of high frequency trading on markets": "CFA Institute survey analyzing market quality, bid-ask spread compression, and adverse selection risks associated with high-frequency market making.",
    "equity market structure literature review high frequency trading": "SEC Division of Trading and Markets comprehensive empirical review evaluating the impact of high-frequency algorithmic trading on market liquidity and volatility.",
    "the impact of high frequency trading on market liquidity a mathematical approach": "Mathematical microstructure model analyzing high-frequency quote placement dynamics, order book depth, and market resiliency.",
    "the ambivalent role of high frequency trading in turbulent market periods": "Empirically investigates HFT liquidity provision versus rapid quote withdrawal during high-volatility market flash crashes.",
    "hedging strategies in futures and forward markets": "University lecture treatise formalizing minimum-variance hedge ratios and cross-hedging effectiveness in equity index futures.",
    "calculating equity index futures fair value": "CME whitepaper deriving the cost-of-carry fair value formula, dividend adjustments, and cash-and-carry basis arbitrage bounds for ES and NQ futures.",

    # Additional Batch 5 exact norm keys
    "stock market trading via actor critic reinforcement learning and adaptable data structure pmc": "Develops actor-critic deep reinforcement learning agents with dynamic state representations for automated equity trading.",
    "stock market trading via actor critic reinforcement learning and adaptable data structure": "Develops actor-critic deep reinforcement learning agents with dynamic state representations for automated equity trading.",
    "towards designing a generic and comprehensive deep reinforcement learning framework": "Architects a modular deep reinforcement learning framework incorporating execution delay, transaction friction, and risk penalties.",
    "a comprehensive survey of recommender systems based on deep learning": "Comprehensive survey detailing deep learning, neural graph networks, and attention-based architectures in modern recommender systems.",
    "stock market prediction using machine learning and deep learning architectures": "Benchmarks convolutional neural networks and recurrent models for predicting equity price direction from high-frequency technical indicators.",
    "chapter 0 machine learning robustness a primer": "Surveys distributional shifts, adversarial robustness, and out-of-distribution generalization in financial machine learning models.",
    "analysis of the application of xgboost in exchange traded funds": "Applies XGBoost decision trees to model cross-sectional ETF return dynamics and constituent factor exposures.",
    "a machine learning based stock prediction system using xgboost and random forests": "Benchmarks gradient boosted decision trees against recurrent neural networks for equity price trend forecasting.",
    "comparing xgboost and lstm model for prediction of microsoft corp s stock price direction": "Compares XGBoost gradient boosting against LSTM recurrent networks for predicting directional price movements in individual equities.",
    "financial distress early warning for chinese enterprises from a systemic risk perspective based on the adaptive weighted xgboost bagging model": "Develops an adaptive weighted XGBoost-Bagging ensemble model for corporate financial distress early warning and default probability estimation.",
    "a robust machine learning approach for credit risk analysis of large loan level datasets using deep learning and extreme gradien": "BIS study evaluating XGBoost and deep neural networks on granular loan-level portfolios for macroprudential stress testing.",
    "interpretability analysis in transformers based on attention visualization": "Investigates multi-head attention weight visualization and layer-wise attribution to interpret financial Transformer representations.",
    "predicting stock price by using attention based hybrid lstm model": "Integrates multi-head self-attention with LSTM recurrent networks to capture long-range temporal dependencies in equity prices.",
    "finbharat stock prediction using transformer": "Applies Transformer sequence models to capture multi-horizon price patterns and volatility dynamics across Indian equities.",
    "attention is all you need": "Vaswani et al.'s seminal paper introducing the multi-head self-attention Transformer architecture, replacing recurrent and convolutional sequence processing.",
    "explainable transformers in financial forecasting philarchive": "Examines attention rollout and Integrated Gradients methods to explain Transformer predictions in financial time series forecasting.",
    "explainable transformers in financial forecasting": "Examines attention rollout and Integrated Gradients methods to explain Transformer predictions in financial time series forecasting.",
    "efficient transformers a survey": "Comprehensive survey detailing linear, sparse, and memory-efficient attention mechanisms in scalable Transformer architectures.",
    "an ai enhanced forecasting framework integrating lstm and transformer based sentiment for stock price prediction": "Integrates news sentiment embeddings from Transformer encoders with LSTM price sequence models for stock trend prediction.",
    "sparse high dimensional model in economics": "Surveys high-dimensional sparse regression, Lasso regularization, and post-selection inference in empirical economics and finance.",
    "hedging with e mini s p 500 future": "CME whitepaper detailing cross-hedging mechanics, basis risk, and hedge ratio optimization using E-mini S&P 500 futures.",
    "hedging strategy in futures and forward markets": "University lecture treatise formalizing minimum-variance hedge ratios and cross-hedging effectiveness in equity index futures.",
    "determinants of herding behavior among financial analysts a study of french listed firms": "Empirically investigates macroeconomic uncertainty and career incentives as primary drivers of sell-side analyst consensus herding.",
    "the legal implications of insider trading and market manipulation how corporate governance can mitigate legal risks and promote fairness": "Examines corporate governance mechanisms, blackout periods, and compliance frameworks for mitigating illegal insider trading and market manipulation.",
    "inferring bad news from insider sales emory university": "Isolates informational bad news from liquidity-driven insider sales by conditioning on corporate earnings disclosure calendars.",
    "inferring bad news from insider sales": "Isolates informational bad news from liquidity-driven insider sales by conditioning on corporate earnings disclosure calendars.",
    "insider trading in connected firms during trading bans the harvard law school forum on corporate governance": "Analyzes shadow insider trading where informed executives trade in economically connected peer companies during firm blackout windows.",
    "insider trading in connected firms during trading bans": "Analyzes shadow insider trading where informed executives trade in economically connected peer companies during firm blackout windows.",
    "the impact of trading volume on portfolios effective time": "Examines how trading volume interaction modifies the formation and holding period profitability of price momentum strategies.",
    "the effect of trading volume on stock price": "Empirically investigates the lead-lag relationship and price impact between trading volume spikes and equity price reversals.",
    "hybrid machine learning model for long term stock market": "Combines convolutional feature extractors with recurrent networks to forecast long-term equity trends from volume-price matrices.",
    "stock prediction using deep learning a comparison": "Benchmarks CNNs, RNNs, and hybrid deep architectures for directional stock price forecasting across market regimes.",
    "a novel ensemble deep learning model for stock prediction based": "Develops an ensemble deep neural architecture integrating price-volume momentum oscillators for directional trend forecasting.",
    "how useful are implied distributions evidence from stock index options": "BIS empirical study evaluating the forecasting accuracy and subjective risk aversion adjustments of option-implied risk-neutral probability density functions.",
    "embedded theoretical quality option pricing in treasury bond futures starting from the definition deviation of conversion factor": "Models the theoretical quality option embedded in Treasury bond futures arising from conversion factor deviations.",
    "private credit risk management in evergreen funds portfolio for the future caia": "CAIA research paper examining liquidity mismatches, gating mechanisms, and valuation smoothing in perpetual evergreen private credit funds.",
    "financial production and the subprime mortgage crisis": "Schwarcz's legal and economic analysis examining structural complexity, moral hazard, and systemic liquidity contagion during the 2008 financial crisis.",
    "the global drivers of private credit bis": "BIS study analyzing the macroeconomic drivers, regulatory capital arbitrage, and institutional asset allocation shifts fueling private debt growth.",
    "stochastic calculus for arbitrage free pricing with stochastic volatility contents 1 probability spaces and random variables 1": "Derives the Feynman-Kac connection and martingale pricing representation for continuous-time stochastic volatility models.",
    "optimal portfolio selection by cvar based sharpe ratio genetic algorithm approach": "Applies genetic algorithms to optimize CVaR-adjusted Sharpe ratios under non-normal asset return distributions.",
    "black litterman exotic beta and varying efficient portfolios an integrated approach": "Integrates Black-Litterman subjective views with alternative risk premia and dynamic efficient frontiers.",
    "enhancing risk parity by including views robeco com": "Robeco research paper formulating a Black-Litterman framework to integrate active tactical views into risk parity portfolios.",
    "portfolio selection problem using cvar risk measures equipped with dea pso and ica algorithms": "Applies DEA, PSO, and ICA metaheuristics to solve portfolio selection problems minimizing Conditional Value-at-Risk.",
    "on esg portfolio construction a multi objective optimization approach": "Develops multi-objective optimization algorithms to evaluate risk-return-sustainability tradeoffs in ESG portfolio construction.",
    "an empirical comparison between robust estimation and robust optimization to mean variance portfolio": "Compares robust covariance estimators against robust optimization uncertainty sets for mitigating portfolio estimation risk.",
    "resampled efficient frontier integration for moeas": "Integrates Michaud's resampled efficient frontier framework into multi-objective evolutionary algorithms to reduce portfolio turnover.",
    "testing strategy based on multiple signals": "Robert Novy-Marx's influential paper detailing multiple testing corrections and false discovery rates when evaluating multi-signal quantitative strategies.",
    "three model of market impact": "Jim Gatheral's foundational paper analyzing temporary, permanent, and transient market impact models and proving no-dynamic-arbitrage conditions.",
    "multi period portfolio optimization using model predictive control with mean variance and risk parity frameworks": "Applies model predictive control (MPC) to multi-period mean-variance and risk parity portfolio rebalancing under dynamic transaction costs.",
    "advancing investment frontiers industry grade deep reinforcement learning for portfolio optimization": "Develops an industrial-grade deep reinforcement learning framework incorporating execution slippage and turnover constraints for multi-asset allocation.",
    "retrieval augmented generation rag for fintech agentic design and evaluation": "Presents an agentic multi-stage RAG architecture incorporating automated self-evaluation guardrails for financial technology systems.",
    "smartfinrag interactive modularized financial rag live demo system": "Develops an interactive modularized RAG architecture featuring adaptive chunking and dynamic query expansion for financial question answering.",
    "llm output drift cross provider validation mitigation for financial workflows": "Quantifies stochastic output drift across LLM provider updates and proposes deterministic consensus validation for compliance workflows.",
    "the future and fintech knowledge graphs and its applications in finance": "Surveys entity extraction, relational link prediction, and enterprise knowledge graph architectures in financial risk management.",
    # --- Batch 6 Curated Research Papers ---
    "a comparison of the kelly criterion and a mean variance model to portfolio selection with kospi 200": "Empirically benchmarks Kelly capital growth optimization against Markowitz mean-variance portfolio construction in Korean equity index markets.",
    "a new interpretation of information rate": "John L. Kelly Jr.'s foundational 1956 paper introducing the Kelly criterion to maximize the asymptotic growth rate of capital in information-theoretic betting and communication channels.",
    "a subordinated stochastic process model with finite variance for speculative prices": "Peter K. Clark's seminal Econometrica paper introducing the Mixture of Distributions Hypothesis (MDH) linking price volatility to stochastic latent information flow.",
    "aggregate confusion the divergence of esg ratings": "Berg, Kölbel, and Rigobon's seminal MIT Sloan study decomposing ESG rating divergence into measurement, scope, and weight discrepancies across major rating agencies.",
    "an empirical analysis of counterparty risk in cds prices": "Empirically isolates counterparty credit risk and joint default probabilities embedded in single-name credit default swap spreads.",
    "artificial intelligence vs efficient markets a critical reassessment of predictive model in the big data era": "MDPI empirical study analyzing the limits of predictability and out-of-sample alpha decay in deep learning models across market regimes.",
    "bloomberggpt a large language model for finance": "Bloomberg quantitative research paper introducing BloombergGPT, a 50-billion parameter decoder-only language model trained on domain-specific financial data and general corpora.",
    "combinatorial information market design": "Robin Hanson's seminal paper introducing Logarithmic Market Scoring Rules (LMSR) for automated market making and combinatorial prediction markets.",
    "computing the ssr": "Quantitative study developing robust numerical estimation algorithms for the Skew Stickiness Ratio (SSR) from discrete option surface observations.",
    "conditional extreme risk black swan hedging and asset prices": "University of Hawaii study modeling tail-risk pricing, black swan hedging mechanics, and extreme value theory distributions in equity asset pricing.",
    "convergence studies on monte carlo methods for pricing mortgage backed securities": "MDPI study evaluating quasi-Monte Carlo Sobol sequences and Brownian bridge path generation for accelerated mortgage-backed security pricing.",
    "credit default swaps": "Federal Reserve Board FEDS study analyzing market liquidity, price discovery, and systemic interconnectedness across sovereign and single-name corporate CDS markets.",
    "credit risk modeling and analysis using copula method and changepoint approach to survival data": "Columbia University doctoral dissertation developing dynamic copula models and structural changepoint survival analysis for multi-name credit portfolio default modeling.",
    "deep limit order book forecasting a microstructural guide": "Comprehensive academic review analyzing spatial-temporal feature engineering, DeepLOB convolutional neural networks, and microstructural order book dynamics.",
    "divergence and aggregation of esg ratings a survey": "Comprehensive academic survey detailing mathematical aggregation methodologies, rating divergence drivers, and portfolio implications of divergent ESG ratings.",
    "esg and financial performance aggregated evidence from more than 2000 empirical studies": "Friede, Busch, and Bassen's comprehensive meta-analysis of over 2,000 empirical studies demonstrating a positive relation between corporate ESG criteria and financial performance.",
    "esg ratings a compass without direction": "Harvard Law study evaluating the lack of standardization and high correlation breakdown across commercial ESG rating methodologies.",
    "essays on market microstructure": "Purdue University doctoral dissertation examining informed trading, high-frequency quoting dynamics, and institutional order execution.",
    "estimating u s cross border securities flows ten years of the tic slt": "Federal Reserve study analyzing a decade of Treasury International Capital (TIC) data to measure foreign investor portfolio shifts across US equities, Treasuries, and corporate bonds.",
    "evaluating trading strategy": "Campbell Harvey and Yan Liu's seminal study deriving multiple testing hurdle rates and haircut Sharpe ratios to adjust for data-mining and backtest overfitting.",
    "explaining credit default swap spreads with equity volatility and jump risks of individual firms": "Cremers, Driessen, and Maenhout (BIS Working Paper 181) seminal empirical study demonstrating that single-stock option-implied volatility and jump risk explain corporate CDS spreads.",
    "factor timing": "Ilmanen, Israel, Lee, Moskowitz, and Thapar (AQR / NBER) empirical study demonstrating that dynamic factor timing offers modest economic benefits and is easily overwhelmed by turnover costs.",
    "factor timing with portfolio characteristics": "EFMA study evaluating dynamic factor timing strategies using macroeconomic state variables, valuation spreads, and momentum characteristics.",
    "financial news analysis using llms": "Benchmarks foundation LLMs against domain-tuned architectures for nuanced financial entity extraction and contextual sentiment scoring.",
    "finding the value at risk for credit default swaps": "DiVA portal study applying copula-based Monte Carlo simulations and historical VaR models to measure market and credit risks in CDS portfolios.",
    "findpo financial sentiment analysis for algorithmic trading through preference optimization of llms": "Develops Direct Preference Optimization (DPO) frameworks for financial LLMs to align sentiment signals with trading execution and downside risk aversion.",
    "fine tuning gemma 7b for enhanced sentiment analysis of financial news headlines": "Benchmarks parameter-efficient fine-tuning (PEFT/LoRA) of open-weights LLMs for domain-specific financial news headline sentiment classification.",
    "fingpt open source financial large language model": "Introduces FinGPT, an open-source financial large language model framework utilizing low-rank adaptation (LoRA) for real-time sentiment analysis and alpha generation.",
    "finllama llm based financial sentiment analysis for algorithmic trading": "Applies instruction-tuned LLaMA architectures to extract high-precision directional sentiment signals from financial news feeds for algorithmic trading.",
    "funding liquidity shocks in a quasi experiment evidence from the cds big bang": "American Economic Association study exploiting the 2009 CDS Big Bang to measure how derivative standardization impacted corporate bond funding liquidity and CDS-bond basis arbitrage.",
    "gamma and vega hedging using deep distributional reinforcement learning": "Frontiers in AI study developing deep distributional reinforcement learning algorithms for multi-period gamma and vega hedging of non-linear option portfolios under transaction friction.",
    "harvesting volatility risk premium": "Imperial College London quantitative thesis analyzing the empirical magnitude, time-series predictability, and delta-hedged harvesting of the equity index variance risk premium.",
    "hft and ghost liquidity": "ESMA quantitative research study analyzing high-frequency quote cancellation rates and fleeting phantom liquidity in electronic limit order books.",
    "historical performance of put writing strategy": "Oleg Bondarenko's seminal Cboe study evaluating the long-term risk-return profile, Sharpe ratios, and drawdown dynamics of systematic SPX cash-secured put writing.",
    "how misunderstanding factor model set unreasonable expectations for smart beta": "Journal of Portfolio Management study examining how benchmark mismatch and factor cyclicality lead to misaligned expectations in systematic factor strategies.",
    "how misunderstanding factor models set unreasonable expectations for smart beta": "Journal of Portfolio Management study examining how benchmark mismatch and factor cyclicality lead to misaligned expectations in systematic factor strategies.",
    "how to properly compute credit default swap returns": "Formulates a mathematically rigorous framework for computing daily Mark-to-Market and cash-flow returns on unfunded single-name credit default swap contracts.",
    "implied volatility volatility smile skew smirk and risk neutral density rnd": "Fordham University quantitative treatise detailing the mathematical extraction of risk-neutral probability density functions (RND) from option implied volatility smiles via Breeden-Litzenberger.",
    "interpretable hypothesis driven trading a rigorous walk forward validation framework for market microstructure signals": "Presents an interpretable hypothesis-driven walk-forward validation architecture for statistical microstructure signals to eliminate backtest overfitting.",
    "interpreting the volatility smile an examination of the information content of option prices": "Federal Reserve Board research paper analyzing the macroeconomic information content, jump risk expectations, and subjective risk aversion embedded in option implied volatility smiles.",
    "investing is compression": "Applies algorithmic information theory and Kolmogorov complexity to demonstrate that quantitative investing is mathematically equivalent to lossy data compression.",
    "is smart beta really so smart": "Burton Malkiel's critical empirical evaluation comparing fundamental, low-volatility, and equal-weighted smart beta indexes against cap-weighted market benchmarks.",
    "jump risk stock returns and slope of implied volatility smile": "Empirically connects equity jump risk intensities to the steepness and term structure of index option implied volatility skews.",
    "kelly criterion from a simple random walk to lévy processes": "USC Dornsife study extending the continuous-time Kelly portfolio selection framework from Brownian motions to jump-diffusion and heavy-tailed Lévy processes.",
    "kelly s criterion for option investment": "Georgia Tech quantitative monograph deriving continuous and discrete Kelly optimal position sizing formulas for multi-leg options strategies.",
    "large language model for financial and investment management applications": "Journal of Portfolio Management study evaluating LLM applications across factor discovery, earnings call analysis, and automated investment committee reporting.",
    "leveraging large language model for sentiment analysis and investment strategy development in financial markets": "MDPI study evaluating prompt engineering and retrieval-augmented LLM sentiment extraction for systematic multi-asset strategy construction.",
    "likelihood based volatility estimators in the presence of market microstructure noise": "Dacheng Xiu's seminal study deriving quasi-maximum likelihood estimators for continuous-time volatility estimation in the presence of high-frequency bid-ask bounce and microstructure noise.",
    "lit limit order book transformer": "Frontiers in AI study introducing LiT, a Transformer architecture designed to capture long-range spatial and temporal dependencies across multi-level limit order books.",
    "long term capital growth the good and bad properties of the kelly and fractional kelly capital growth criteria": "MacLean and Ziemba's authoritative treatise evaluating the asymptotic optimality, finite-horizon drawdown severity, and fractional shrinkage properties of the Kelly criterion.",
    "machine learning for market microstructure and high frequency trading": "Michael Kearns and Yuriy Nevmyvaka's seminal quantitative survey evaluating reinforcement learning and supervised models for optimal execution and high-frequency trade routing.",
    "market impact a systematic study of the high frequency options market": "Bouchaud et al.'s empirical study analyzing square-root market impact laws, order book liquidity consumption, and high-frequency execution dynamics in options markets.",
    "modelling the instability of mortgage backed prepayments": "Federal Reserve Bank of New York study analyzing burnout effects, turnover rates, and non-linear parameter instability in mortgage prepayment functions.",
    "modified kelly criteria": "Simon Fraser University study proposing shrinkage and Bayesian modified Kelly formulas to stabilize portfolio growth under parameter uncertainty.",
    "monte carlo methods for security pricing": "Phelim Boyle, Mark Broadie, and Paul Glasserman's seminal Columbia University treatise on Monte Carlo simulation techniques and variance reduction for pricing path-dependent derivatives.",
    "mortgage backed securities": "Federal Reserve Bank of New York Staff Report detailing the market architecture, agency guarantees, TBA forward market mechanics, and prepayment risks in RMBS.",
    "news sentiment and investment risk management innovative evidence from large language model": "Macquarie University study investigating how LLM-extracted news sentiment improves portfolio risk forecasting and dynamic Value-at-Risk estimates.",
    "on detecting spoofing strategy in high frequency trading": "Applies machine learning classifiers to limit order book order arrival patterns to detect illegal spoofing and quote manipulation.",
    "option portfolio selection with generalized entropic portfolio optimization": "Formulates generalized entropic portfolio optimization algorithms to size multi-strike option portfolios under non-Gaussian return distributions.",
    "option smile volatility and implied probabilities implications of concavity in iv curves": "Quantifies the non-parametric risk-neutral probability densities implied by concave option smile geometries and investigates butterfly arbitrage bounds.",
    "option volatility arbitrage opportunities": "LSU graduate dissertation modeling long-dated LEAP volatility term structure anomalies, calendar spread pricing, and implied vs realized volatility arbitrage.",
    "performance of smart beta etfs in the u s market 2009 2019": "Singapore Management University empirical study analyzing the tracking error, factor tilts, and net-of-fee alpha of US smart beta ETFs from 2009 to 2019.",
    "portfolio optimization for binary options based on relative entropy": "Applies relative entropy minimization and information theory to solve optimal multi-asset binary options portfolio sizing.",
    "positive versus negative esg portfolio screening and investors preferences": "Empirically benchmarks positive best-in-class versus negative exclusionary ESG portfolio screening across risk-adjusted return and tracking error distributions.",
    "practical implementation of the kelly criterion optimal growth rate number of trades and rebalancing frequency for equity portfolios": "Frontiers in Applied Mathematics study evaluating the practical implementation of Kelly growth optimal sizing, trade frequency, and dynamic rebalancing under transaction costs.",
    "prediction markets": "Justin Wolfers and Eric Zitzewitz's seminal survey analyzing information aggregation, contract design, and market efficiency across prediction markets.",
    "prepayment modeling in mortgage backed securities": "DiVA research study formulating stochastic interest rate models (Hull-White) coupled with empirical refinancing incentive functions for RMBS option-adjusted spread valuation.",
    "rise of the machines application of machine learning to mortgage prepayment modeling": "Journal of Fixed Income study applying XGBoost and neural network survival models to forecast path-dependent non-linear mortgage prepayment curves.",
    "risk constrained kelly gambling": "Stephen Boyd et al. (Stanford University) study formulating convex optimization frameworks for risk-constrained Kelly capital allocation with Value-at-Risk and variance constraints.",
    "safe haven cds premium": "American Economic Association study analyzing cross-border safe-haven capital flows and sovereign credit default swap premia during global financial stress.",
    "securitized product investment risk management perspectives": "Bank of Japan quantitative study analyzing tranche subordination, correlation breakdown risk, and loss-given-default modeling in structured credit products.",
    "sentiment and volatility in financial markets a review of bert and garch applications during geopolitical crises": "Surveys hybrid FinBERT and GARCH volatility forecasting architectures during systemic market dislocations and geopolitical stress regimes.",
    "sentiment trading with large language model": "Develops an end-to-end quantitative trading framework leveraging LLM sentiment reasoning to generate cross-sectional equity alpha signals.",
    "simply put the performance of cash secured put writing": "Neuberger Berman and Cboe whitepaper analyzing the structural variance risk premium harvested via systematic cash-secured SPX put writing.",
    "sizing the risk kelly vix and hybrid approaches in put writing on index options": "Develops hybrid Kelly-VIX position sizing algorithms to dynamically scale leverage and collateral reserves in systematic index put-writing strategies.",
    "smart beta made smart synthetic risk factors for institutional and retail investors": "Presents a synthetic factor construction methodology to isolate pure factor risk premia from uncompensated idiosyncratic noise in smart beta portfolios.",
    "smart beta versus smart alpha": "Jacobs and Levy's quantitative study deconstructing smart beta indexing strategies into explicit factor exposures and evaluating capacity constraints.",
    "smile dynamics iv": "Lorenzo Bergomi's seminal quantitative treatise on volatility smile dynamics, multi-factor variance curve models, and the Skew Stickiness Ratio.",
    "stochastic volatility and the volatility smile": "DiVA research monograph deriving the calibration mechanics and smile kinematics of Heston, SABR, and local volatility models.",
    "systematic risk and the price structure of individual equity options": "Rotman School of Management study decomposing single-stock option implied volatilities into systematic market risk and idiosyncratic firm volatility components.",
    "tackling estimation risk in kelly investing using options": "Develops a robust optimization framework using option collars and put overlays to protect Kelly growth portfolios against severe parameter estimation risk.",
    "the black scholes formula and volatility smile": "Examines theoretical model violations of constant volatility in the Black-Scholes framework and surveys parametric smile models.",
    "the central bank balance sheet trilemma": "Federal Reserve research note analyzing the structural policy trade-offs between reserve supply, liquidity safety nets, and central bank balance sheet footprint.",
    "the complex nature of financial market microstructure the case of a stock market crash": "Investigates liquidity collapse, order book asymmetry, and cascade feedback loops during extreme market flash crashes.",
    "the contribution of foreign holdings of u s treasury securities to the u s long term interest rate": "Dallas Fed working paper quantifying the downward term premium pressure exerted by global reserve manager foreign Treasury holdings on US benchmark yields.",
    "the cross border trail of the treasury basis trade": "Federal Reserve Board note mapping foreign institutional leverage, repo financing, and cross-border arbitrage capital flows in the US Treasury cash-futures basis trade.",
    "the derivative payoff bias": "American Economic Association study documenting retail investor cognitive biases and systematic overpayment for lottery-like asymmetric derivative payoffs.",
    "the kelly criterion exploiting favorable bets and the stock market": "David Aldous's mathematical treatise analyzing the asymptotic growth properties, drawdown distributions, and risk of ruin under the Kelly criterion.",
    "the plaza accord 30 years later": "Jeffrey Frankel's Harvard Kennedy School treatise evaluating the macroeconomic effectiveness, currency intervention dynamics, and lasting global imbalances of the 1985 Plaza Accord.",
    "toward esg alpha analyzing esg exposures through a factor lens": "Financial Analysts Journal study demonstrating that ESG ratings primarily load on conventional equity factors (size, quality, momentum) rather than generating standalone alpha.",
    "understanding retail investors dynamic trading behavior in the u s options market": "Cboe Global Markets quantitative research study analyzing retail option order flow, intraday trading patterns, and retail sentiment dynamics across US options exchanges.",
    "using the kelly criterion for investing": "William T. Ziemba's comprehensive chapter on applying full and fractional Kelly betting algorithms across financial asset classes and speculative markets.",
    "vanna volga and smile consistent implied volatility surface of equity index options": "Extends the vanna-volga method to construct arbitrage-free, smile-consistent implied volatility surfaces across equity index option strikes.",
    "vega risk and the smile": "Columbia University quantitative study analyzing unhedged vega risk, volatility-of-volatility exposures, and dynamic smile hedging across strike manifolds.",
    "versatune an efficient data composition framework for training multi capability llms": "EMNLP research paper introducing VersaTune, a multi-stage data selection framework for optimizing fine-tuning data mixtures across diverse domain capabilities.",
    "what can volatility smiles tell us about the too big to fail problem": "Journal of Financial and Quantitative Analysis study using banking sector option volatility smiles to extract market-implied systemic default and bailout probabilities.",
    "will the market fix the market a theory of stock exchange competition and innovation": "Eric Budish et al.'s seminal study analyzing high-frequency trading latency arbitrage, frequent batch auctions, and stock exchange competition.",

}


def load_classified_research_papers(state_path: Path) -> dict[str, dict]:
    """Load slugs classified as research-paper from gdocs/classified_state.json."""
    if not state_path.exists():
        raise FileNotFoundError(f"State file not found: {state_path}")
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)
    return {k: v for k, v in state.items() if v.get("category") == "research-paper"}


def load_article_metadata(articles_dir: Path, target_slugs: set[str]) -> dict[str, dict]:
    """Extract article titles and googleDoc published URLs from TypeScript quarter files."""
    if not articles_dir.exists():
        raise FileNotFoundError(f"Articles directory not found: {articles_dir}")

    files = sorted(articles_dir.glob("*-q*.ts"))
    articles_by_slug: dict[str, dict] = {}
    for filepath in files:
        content = filepath.read_text(encoding="utf-8")
        blocks = re.split(r"\n\s*\{", content)[1:]
        for block in blocks:
            slug_match = re.search(r'\bslug:\s*["\']([^"\']*)["\']', block)
            title_match = re.search(r'\btitle:\s*["\']((?:[^"\'\\]|\\.)*)["\']', block)
            gdoc_match = re.search(r'\bgoogleDoc:\s*["\']([^"\']*)["\']', block)
            if slug_match and slug_match.group(1) in target_slugs:
                slug = slug_match.group(1)
                raw_title = title_match.group(1) if title_match else slug
                title = raw_title.replace('\\"', '"').replace("\\'", "'")
                google_doc = gdoc_match.group(1) if gdoc_match else None
                articles_by_slug[slug] = {
                    "slug": slug,
                    "title": title,
                    "google_doc": google_doc,
                    "source_file": filepath.name,
                }
    return articles_by_slug


def load_doc_ids(matches_path: Path) -> dict[str, str]:
    """Load doc_id mappings for confirmed matches from gdocs/article-exact-matches.md."""
    if not matches_path.exists():
        return {}
    doc_ids: dict[str, str] = {}
    with open(matches_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("| ") and not line.startswith("| Slug") and not line.startswith("| :---"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 5 and parts[3] == "matched":
                    doc_ids[parts[0]] = parts[4]
    return doc_ids


def unwrap_google_url(url: str) -> str:
    """Unwrap Google redirect link (https://www.google.com/url?q=...)."""
    if not url:
        return ""
    if "google.com/url?" in url:
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        if "q" in qs and qs["q"]:
            return qs["q"][0]
    return url


def fetch_published_doc_citations(url: str, timeout: float = 15.0) -> list[dict]:
    """Fetch full published Google Doc HTML and extract items from Works Cited / References."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw_html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [WARN] Failed to fetch {url}: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(raw_html, "html.parser")

    # Locate heading for references section
    ref_heading = None
    for el in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"]):
        text = el.get_text().strip().lower()
        if text in [
            "works cited",
            "works cited:",
            "references",
            "references:",
            "bibliography",
            "bibliography:",
            "citations",
            "citations:",
        ] or re.match(r"^(works cited|references|bibliography)\b", text):
            ref_heading = el
            break

    citations = []
    if ref_heading:
        curr = ref_heading
        while curr:
            curr = curr.find_next_sibling()
            if not curr:
                break
            if curr.name in ["h1", "h2", "h3"]:
                break

            items = []
            if curr.name in ["ol", "ul"]:
                items = curr.find_all("li")
            elif curr.name == "p":
                items = [curr]

            for item in items:
                raw_text = item.get_text().strip()
                if not raw_text:
                    continue
                a_tag = item.find("a")
                href = unwrap_google_url(a_tag.get("href", "")) if a_tag else ""
                citations.append({"raw_text": raw_text, "url": href})
    else:
        # Fallback: check if the document ends with an ordered/unordered list
        lists = soup.find_all(["ol", "ul"])
        if lists:
            last_list = lists[-1]
            for li in last_list.find_all("li"):
                raw_text = li.get_text().strip()
                if not raw_text:
                    continue
                a_tag = li.find("a")
                href = unwrap_google_url(a_tag.get("href", "")) if a_tag else ""
                citations.append({"raw_text": raw_text, "url": href})

    return citations


def is_domain_allowed(url: str) -> tuple[bool, str]:
    if not url:
        return False, "no_url"
    parsed = urllib.parse.urlparse(url)
    netloc = parsed.netloc.lower()
    path = parsed.path.lower()

    for pat in REJECT_DOMAIN_PATTERNS:
        if re.search(pat, netloc):
            return False, f"rejected_domain:{pat}"

    if netloc.startswith("docs.") or netloc.startswith("help.") or netloc.startswith("support.") or netloc.startswith("api."):
        return False, "rejected_docs_subdomain"

    if "formidable" in path or ("wp-content/uploads" in path and "xm global" in path):
        return False, "rejected_spam_upload"

    for pat in GENUINE_RESEARCH_DOMAINS:
        if re.search(pat, netloc):
            return True, f"genuine_domain:{pat}"

    return False, f"unmatched_domain:{netloc}"


def is_url_path_rejected(url: str) -> tuple[bool, str]:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lower()
    netloc = parsed.netloc.lower()

    reject_paths = [
        "/education/courses/",
        "/what-we-do/",
        "/insights/datasets/",
        "/about-us/",
        "/insights/perspectives/",
        "/insights/research/bibliography/",
        "/insights/bibliography/",
        "/insights/research/white-papers",
        "/insights/research/journal-article",
        "/insights/research/working-paper",
        "/files/litigation/",
        "/archives/edgar/",
        "/small-entity-compliance-guide",
        "/notice-amendments-and-commission",
        "/figure/",
        "/scientific-contributions/",
        "/aia-labs",
        "/how-etfs-are-created-and-redeemed",
        "/master-the-mechanics-of-etf-trading",
        "/dimensional-investing-in-an-active-etf-structure",
        "/the-all-weather-story",
        "/the-all-weather-portfolio-built-for-any-forecast",
        "/a-new-era-of-higher-inflation-risks",
        "/from-carrier-pigeons-to-ai-gaining-an-edge-with-alternative-data",
        "/option-selling-has-become-consensus-its-impacts",
        "/new-research-shows-options-based-strategies-can-generate-higher-gross-premiums-with-less-volatility-over-traditional-asset-classes",
        "/refresher-readings/",
        "/ftp/",
        "/class/archive/",
        "/textbook%20solution%20manual/",
        "/insights/2023/02/quant-chart-taming-momentum-crashes",
        "/insights/posts/vix-index-attribution-of-notable-tail-events",
        "/series/",
        "/markets/us/options/market-statistics/",
        "/markets/us/futures/market-statistics/",
        "/tradable-products/vix/",
        "/tradable_products/vix/",
        "/news/news-details/",
        "/investing/investment-products/stocks/day-trading",
        "/research/gdpnow",
        "/complete-issue.pdf",
        "/martin-fund-management-capturing-outsized-commodity-moves",
        "/innovations.htm",
        "/openmarkets/",
        "/rules-regulations/",
        "/resources-small-businesses/",
        "/enforcement-litigation/",
        "/newsroom/press-releases/",
        "/news/press/",
        "/topics/performance-attribution",
        "/blog/2013/08/tactical-asset-allocation-erisa-plans",
        "/our-expertise/insights/2017/sep/mifid-ii-research-unbundling",
        "/tools-information/quikstrike/",
        "/rulebook/",
        "/ideas-made-to-matter/",
        "/news/retail-investors-play-a-losing-game",
        "/duke-fuqua-insights/unintended-consequences",
        "/binaries/documents/center-for-ethical-organizational-cultures/",
        "/context/busi_fac_pubs/",
        "/thenetwork/2011/10/18/the-galleon-insider-trading-case",
        "/businessthink.unsw.edu.au/articles/",
        "/news/2025/05/pamplin-investor-attention-insider-trading",
        "/news/new-study-insider-trading-discovers-flaws",
        "/our-expertise/insights/2024/oct/private-credit",
        "/press-release/2024/citi-and-apollo",
        "/news-and-views/perspective/private-markets-outlook-2026",
        "/leverage/day-2-presentations/Household-Leverage",
        "/blogs/articles/2025/10/14/growth-of-nonbanks",
        "/blogs/cfainstitute.org/investor/2025/06/05/private-credits-surge",
        "/Ec2021_Lecture2r3.pdf",
        "/181.1.03f/Lect14.pdf",
        "/FoundationsFE/BlackScholes.pdf",
        "/FE_Ch02%20Black-Scholes%20Model.pdf",
        "/495lecture28.pdf",
        "/furiproject/",
        "/ahl",
        "/wagnerlawgroup.com/",
        # Batch 6 reject paths
        "/0d1260b891a96241316d883d4f5bfaec_MIT15_450F10_lec02.pdf",
        "/12-1070-eia9-impact-circuit-breakers-on-market-outcomes.pdf",
        "/20200507.pdf",
        "/4700-07-Notes-GBM.pdf",
        "/4701Sum07/lec0813.pdf",
        "/5632/black_scholes.pdf",
        "/7-career-paths-in-quantitative-finance/",
        "/Analysis_of_Securitized_Asset_Liquidity.pdf",
        "/CboeGlobalIndices_PUT-Index.pdf",
        "/Cboe_BuyWrite_Indices_Methodology.pdf",
        "/Class416/Lecture07.pdf",
        "/ESMA36-287652198-2699_Final_Report_on_Greenwashing.pdf",
        "/Good_Bad_Kelly.pdf",
        "/Govert_Verkes_InfCom.pdf",
        "/IRC_Lecture13_2019.pdf",
        "/IRC_Lecture3_2019.pdf",
        "/Kelly_Criterion_Final_Presentation.pdf",
        "/Margin_Requirement_Examples.pdf",
        "/PMC10813872/",
        "/PMC3337209/",
        "/Puente-Slides.pdf",
        "/Risk_Topic_1.pdf",
        "/Sections20_1_2_3.pdf",
        "/Slides2_Class3.pdf",
        "/Updated-Kelly-Criterion-Poster-2023.pdf",
        "/Valuing-weather-and-climate",
        "/XSP_Options_Fact_Sheet.pdf",
        "/a-primer-on-prediction-markets/",
        "/ai-and-big-data-in-investments-Part-III-final.pdf",
        "/bank-japans-seductive-widow-maker-trade",
        "/basel_framework/chapter/MAR/21.htm",
        "/benchmark-indices-series-income-generation-and-smoother-returns-with-cboes-bxm-bxmd-put-and-cmbo-indices/",
        "/capabilities/equities/smart-beta",
        "/docu-2018-02-brochure-fi-challenges-7-things-au.pdf",
        "/dont-get-stuck-paying-the-dividend-on-your-short-trade/",
        "/election-results-show-potential-of-prediction-markets",
        "/fineng1_2008.pdf",
        "/forecast_2024.pdf",
        "/global-economy-shakes-off-tariff-shock-amid-tech-driven-boom",
        "/glossary/quantitative-investing/smart-beta-or-alternative-beta",
        "/gray/it.pdf",
        "/guardrails-market-volatility",
        "/h10/summary/",
        "/henry-schwartzs-zero-day-spx-iron-condor-strategy-a-deep-dive/",
        "/how-to-right-size-hedges-via-beta-weighting-with-xsp-options/",
        "/impact-vs-esg",
        "/insights/is-smart-beta-really-so-smart",
        "/institutional-footprints",
        "/investors-need-to-understand-the-risks-of-smart-beta",
        "/is-esg-investing-more-hype-than-help-for-investment-portfolios",
        "/ln4.pdf",
        "/margin-accounts",
        "/mcbdc_bridge.htm",
        "/portfolio-margin-intraday-trading",
        "/pr/kelly.html",
        "/reverse-convertibles-complex-investments",
        "/revisions-to-the-federal-reserve-dollar-indexes-20190115.html",
        "/seminars/eng/2006/stress/pdf/ms.pdf",
        "/smart-beta-between-active-passive-realms",
        "/spx-fact-sheet.pdf",
        "/state-anti-esg-movement-evolves-to-target-investor-access",
        "/study-machine-learning-can-predict-market-behavior",
        "/the-payment-system-puts-a-floor-on-the-feds-balance-sheet",
        "/tradable_products/index-options-benefits-tax-treatment/",
        "/trade-up-to-market-close-with-xsp",
        "/understanding-smart-beta-strategies-to-boost-investment-portfolio-performance",
        "/uyeda-statement-abs-concept-release-092625",
        "/what-are-etf-expense-ratios-and-why-do-they-matter",
        "/what-is-esg-investing",
        "/what-is-the-best-approach-to-factor-investing",
        "/what-volatility-risk-premium",
        "/why-trade-xsp-vs-spy-a-breakdown-of-the-benefits/",
        "/xsp-options/",
        "/~gray/",
    ]
    for rp in reject_paths:
        if rp in path:
            return True, f"reject_path:{rp}"

    if ("aqr.com" in netloc or "twosigma.com" in netloc) and (path == "/" or path == ""):
        return True, "reject_homepage"

    return False, ""


def clean_paper_title(raw_text: str, url: str) -> str | None:
    # URL-specific canonical titles for known truncations
    # Batch 6 canonical titles
    if "0430.pdf" in url:
        return "The Contribution of Foreign Holdings of U.S. Treasury Securities to the U.S. Long-Term Interest Rate"
    if "0718-1876/20/2/77" in url:
        return "Leveraging Large Language Models for Sentiment Analysis and Investment Strategy Development in Financial Markets"
    if "07_Zhu.pdf" in url:
        return "An Empirical Analysis of Counterparty Risk in CDS Prices"
    if "0895330042162377" in url:
        return "Prediction Markets"
    if "10.1080/1351847X.2025.2585967" in url:
        return "Positive versus Negative ESG Portfolio Screening and Investors' Preferences"
    if "10.3389/frai.2023.1129370" in url:
        return "Gamma and Vega Hedging Using Deep Distributional Reinforcement Learning"
    if "10.7916/D8K361X4" in url:
        return "Credit Risk Modeling and Analysis Using Copula Method and Changepoint Approach to Survival Data"
    if "11EFB91E95DAB3F4FBE243CD390B5F44" in url:
        return "What Can Volatility Smiles Tell Us About the Too Big to Fail Problem?"
    if "1616485/full" in url:
        return "LiT: Limit Order Book Transformer"
    if "172496-K-Huang-Vanna-Volga" in url:
        return "Vanna-Volga and Smile-Consistent Implied Volatility Surface of Equity Index Options"
    if "1902.05418" in url:
        return "Market Impact: A Systematic Study of the High Frequency Options Market"
    if "1914083" in url:
        return "A Subordinated Stochastic Process Model with Finite Variance for Speculative Prices"
    if "2009.14818" in url:
        return "On Detecting Spoofing Strategies in High Frequency Trading"
    if "2022023pap.pdf" in url:
        return "Credit Default Swaps"
    if "2025.emnlp-main.337" in url:
        return "VersaTune: An Efficient Data Composition Framework for Training Multi-Capability LLMs"
    if "2079-9292/14/9/1721" in url:
        return "Artificial Intelligence vs. Efficient Markets: A Critical Reassessment of Predictive Models in the Big Data Era"
    if "222553496" in url:
        return "Jump Risk, Stock Returns, and Slope of Implied Volatility Smile"
    if "2227-7072/3/2/136" in url:
        return "Convergence Studies on Monte Carlo Methods for Pricing Mortgage-Backed Securities"
    if "227623956" in url:
        return "Long-Term Capital Growth: The Good and Bad Properties of the Kelly and Fractional Kelly Capital Growth Criteria"
    if "2303.17564" in url:
        return "BloombergGPT: A Large Language Model for Finance"
    if "2306.06031" in url:
        return "FinGPT: Open-Source Financial Large Language Models"
    if "2307.15718" in url:
        return "Option Smile Volatility and Implied Probabilities: Implications of Concavity in IV Curves"
    if "2403.09267" in url:
        return "Deep Limit Order Book Forecasting: A Microstructural Guide"
    if "2406.16131" in url:
        return "Computing the SSR"
    if "2412.19245" in url:
        return "Sentiment Trading with Large Language Models"
    if "2507.18417" in url:
        return "FinDPO: Financial Sentiment Analysis for Algorithmic Trading through Preference Optimization of LLMs"
    if "2508.16598" in url:
        return "Sizing the Risk: Kelly, VIX, and Hybrid Approaches in Put-Writing on Index Options"
    if "2508.18868" in url:
        return "Tackling Estimation Risk in Kelly Investing Using Options"
    if "2510.16503" in url:
        return "Sentiment and Volatility in Financial Markets: A Review of BERT and GARCH Applications during Geopolitical Crises"
    if "2512.12924" in url:
        return "Interpretable Hypothesis-Driven Trading: A Rigorous Walk-Forward Validation Framework for Market Microstructure Signals"
    if "2604.10758" in url:
        return "Investing is Compression"
    if "28583036/1/files/52947500.pdf" in url:
        return "Aggregate Confusion: The Divergence of ESG Ratings"
    if "31/3/6" in url:
        return "Rise of the Machines: Application of Machine Learning to Mortgage Prepayment Modeling"
    if "320928650" in url:
        return "A Comparison of the Kelly Criterion and a Mean-Variance Model to Portfolio Selection with KOSPI 200"
    if "36437508.pdf" in url:
        return "Essays on Market Microstructure"
    if "369655284" in url:
        return "BloombergGPT: A Large Language Model for Finance"
    if "381579661" in url:
        return "Fine-Tuning Gemma-7B for Enhanced Sentiment Analysis of Financial News Headlines"
    if "393983519" in url:
        return "FinDPO: Financial Sentiment Analysis for Algorithmic Trading through Preference Optimization of LLMs"
    if "396435503" in url:
        return "Financial News Analysis Using LLMs"
    if "400193903.pdf" in url:
        return "News Sentiment and Investment Risk Management: Innovative Evidence from Large Language Models"
    if "51/3/10" in url:
        return "How Misunderstanding Factor Models Set Unreasonable Expectations for Smart Beta"
    if "577050/full" in url:
        return "Practical Implementation of the Kelly Criterion: Optimal Growth Rate, Number of Trades, and Rebalancing Frequency for Equity Portfolios"
    if "5GbbG2Az" in url:
        return "Funding Liquidity Shocks in a Quasi-Experiment: Evidence from the CDS Big Bang"
    if "9804.pdf" in url:
        return "Modelling the Instability of Mortgage-Backed Prepayments"
    if "Budish_paperStock-Exchange-Competition" in url:
        return "Will the Market Fix the Market? A Theory of Stock Exchange Competition and Innovation"
    if "Chap1_KellyZiemba.pdf" in url:
        return "Using the Kelly Criterion for Investing"
    if "Conditional%20Extreme%20Risk" in url:
        return "Conditional Extreme Risk, Black Swan Hedging, and Asset Prices"
    if "EFMA%202022_stage-3032" in url:
        return "Factor Timing with Portfolio Characteristics"
    if "FinLlama" in url:
        return "FinLlama: LLM-Based Financial Sentiment Analysis for Algorithmic Trading"
    if "Is%20Smart%20Beta%20Really%20Smart.pdf" in url:
        return "Is Smart Beta Really So Smart?"
    if "KearnsNevmyvakaHFTRiskBooks.pdf" in url:
        return "Machine Learning for Market Microstructure and High Frequency Trading"
    if "Kelly-Fin-SIFIN-Final.pdf" in url:
        return "Kelly Criterion: From a Simple Random Walk to Lévy Processes"
    if "N7rsBN2N" in url:
        return "The Derivative Payoff Bias"
    if "NYU-RAM_ESG-Paper_2021" in url:
        return "ESG and Financial Performance: Aggregated Evidence from More than 2000 Empirical Studies"
    if "Neuberger_Berman_Simply_PutWriting.pdf" in url:
        return "Simply Put: The Performance of Cash-Secured Put Writing"
    if "PMC12315853" in url:
        return "Deep Limit Order Book Forecasting: A Microstructural Guide"
    if "PMC12398680" in url:
        return "Divergence and Aggregation of ESG Ratings: A Survey"
    if "PMC7517297" in url:
        return "Portfolio Optimization for Binary Options Based on Relative Entropy"
    if "PMC7517377" in url:
        return "Option Portfolio Selection with Generalized Entropic Portfolio Optimization"
    if "PMC8724601" in url:
        return "The Complex Nature of Financial Market Microstructure: The Case of a Stock Market Crash"
    if "PutWriteCBOE19_v14" in url:
        return "Historical Performance of Put-Writing Strategies"
    if "SBFC2025_7D2_P252.pdf" in url:
        return "How to Properly Compute Credit Default Swap Returns"
    if "Shibo_Lu_01210524.pdf" in url:
        return "Harvesting Volatility Risk Premium"
    if "Simply_PutWriting.pdf" in url:
        return "Simply Put: The Performance of Cash-Secured Put Writing"
    if "Smart-Beta-vs-Smart-Alpha.pdf" in url:
        return "Smart Beta versus Smart Alpha"
    if "Sysrisk.pdf" in url:
        return "Systematic Risk and the Price Structure of Individual Equity Options"
    if "Toward_ESG_Alpha" in url:
        return "Toward ESG Alpha: Analyzing ESG Exposures through a Factor Lens"
    if "Understanding-Retail-Investors-Dynamic-Trading-Behavior" in url:
        return "Understanding Retail Investors' Dynamic Trading Behavior in the U.S. Options Market"
    if "Vega%20risk%20and%20the%20smileJoR.pdf" in url:
        return "Vega Risk and the Smile"
    if "aldous/Real_World/kelly.html" in url:
        return "The Kelly Criterion: Exploiting Favorable Bets and the Stock Market"
    if "article=5581&context=gradschool_theses" in url:
        return "Option Volatility & Arbitrage Opportunities"
    if "article=8073&context=lkcsb_research" in url:
        return "Performance of Smart Beta ETFs in the U.S. Market: 2009–2019"
    if "boyd/papers/pdf/kelly.pdf" in url:
        return "Risk-Constrained Kelly Gambling"
    if "corpgov.law.harvard.edu/2022/08/24/esg-ratings-a-compass-without-direction" in url:
        return "ESG Ratings: A Compass Without Direction"
    if "dachxiu.chicagobooth.edu/download/ch14.pdf" in url:
        return "Likelihood-Based Volatility Estimators in the Presence of Market Microstructure Noise"
    if "derivatives/bergomi.pdf" in url:
        return "Smile Dynamics IV"
    if "diva2:1869932" in url:
        return "Prepayment Modeling in Mortgage Backed Securities"
    if "diva2:302710" in url:
        return "Stochastic Volatility and the Volatility Smile"
    if "diva2:532660" in url:
        return "Finding the Value at Risk for Credit Default Swaps"
    if "esma_wp_4_2020_hft_and_ghost_liquidity" in url:
        return "HFT and Ghost Liquidity"
    if "estimating-u-s-cross-border-securities-flows" in url:
        return "Estimating U.S. Cross-Border Securities Flows: Ten Years of the TIC SLT"
    if "etd/188" in url:
        return "The Black-Scholes Formula and Volatility Smile"
    if "faculty.fordham.edu/rchen/iv.pdf" in url:
        return "Implied Volatility, Volatility Smile/Skew/Smirk, and Risk-Neutral Density (RND)"
    if "interpreting-the-volatility-smile" in url:
        return "Interpreting the Volatility Smile: An Examination of the Information Content of Option Prices"
    if "jpm24b.pdf" in url:
        return "Large Language Models for Financial and Investment Management: Applications"
    if "kellyOptionTalk1.pdf" in url:
        return "Kelly's Criterion for Option Investment"
    if "kelly_56.pdf" in url:
        return "A New Interpretation of Information Rate"
    if "mktscore.pdf" in url:
        return "Combinatorial Information Market Design"
    if "monte_carlo_methods_security_pricing.pdf" in url:
        return "Monte Carlo Methods for Security Pricing"
    if "option-smile-volatility-and-implied-probabilities" in url:
        return "Option Smile Volatility and Implied Probabilities: Implications of Concavity in IV Curves"
    if "pdfid=21484" in url:
        return "Safe-Haven CDS Premia"
    if "plaza-accord-30-years-later-0" in url:
        return "The Plaza Accord, 30 Years Later"
    if "ron0803a.pdf" in url:
        return "Securitized-Product Investment: Risk Management Perspectives"
    if "s70420-8669105-235461.pdf" in url:
        return "Smart Beta Made Smart: Synthetic Risk Factors for Institutional and Retail Investors"
    if "sr1001.pdf" in url:
        return "Mortgage-Backed Securities"
    if "the-central-bank-balance-sheet-trilemma" in url:
        return "The Central Bank Balance-Sheet Trilemma"
    if "the-cross-border-trail-of-the-treasury-basis-trade" in url:
        return "The Cross-Border Trail of the Treasury Basis Trade"
    if "tswartz/papers/kelly.pdf" in url:
        return "Modified Kelly Criteria"
    if "w19973.pdf" in url:
        return "Evaluating Trading Strategies"
    if "w26708.pdf" in url:
        return "Factor Timing"
    if "where-large-language-models-and-finance-meet" in url:
        return "BloombergGPT: A Large Language Model for Finance"
    if "work181.pdf" in url:
        return "Explaining Credit Default Swap Spreads with Equity Volatility and Jump Risks of Individual Firms"
    if "OsakaSVI2012.pdf" in url:
        return "Arbitrage-Free SVI Volatility Surfaces"
    if "timevalue.pdf" in url:
        return "Model-Free Boundaries of Option Time Value and Early Exercise Premium"
    if "broadie%20american%20options.pdf" in url.lower():
        return "American Options on Dividend-Paying Assets"
    if "longstaff_schwartz.pdf" in url.lower():
        return "Valuing American Options by Simulation: A Simple Least-Squares Approach"
    if "stoikovvol.pdf" in url.lower():
        return "Pricing Options from the Point of View of a Trader"
    if "172496-k-huang-vanna-volga" in url.lower():
        return "Vanna-Volga and Smile-Consistent Implied Volatility Surface of Equity Index Options"
    if "mpra.ub.uni-muenchen.de/36127" in url:
        return "The Vanna-Volga Method for Derivatives Pricing"
    if "2507.01971" in url:
        return "DeepSupp: Attention-Driven Correlation Pattern Analysis for Support and Resistance Levels"
    if "2403.18839" in url:
        return "Support and Resistance Identification with Gaussian Mixture Models"
    if "2205.15056" in url:
        return "Stock Trading Optimization through Model-Based Reinforcement Learning"
    if "skewwhitepaperjan2011.pdf" in url.lower():
        return "The Cboe SKEW Index: Investigating the Tail Risk of S&P 500 Returns"
    if "2305.04811" in url:
        return "Deep Learning Models for Price Forecasting of Financial Time Series: A Review of Recent Advancements: 2020-2022"
    if "2602.15055" in url:
        return "Beyond Context Sharing: A Unified Agent Communication Protocol (ACP) for Secure, Federated, and Autonomous Agent-to-Agent (A2A) Orchestration"
    if "Man_AHL_Analysis_Trend_Follo" in url:
        return "Trend Following: Equity and Bond Crisis Alpha"
    if "024/2009/002/article-A007" in url:
        return "Yen Carry Trade and the Subprime Crisis"
    if "dupoyetb/implied_convexity" in url:
        return "The Implied Convexity of VIX Futures"
    if "correlation_impact_to_ccp_margin" in url:
        return "Study of Correlation Impact on Credit Default Swap Margin Using a GARCH-DCC-Copula Framework"
    if "10.1287/mnsc.2021.01379" in url:
        return "Tech-Enabled Financial Data Access, Retail Investors, and Market Quality"
    if "2813-0324/7/1/39" in url:
        return "Comparing Machine Learning Methods—SVR, XGBoost, LSTM, and Deep Neural Networks for Stock Price Prediction"
    if "ArbitrageCompleteness.pdf" in url:
        return "A Simple and Intuitive Coverage of The Fundamental Theorems of Asset Pricing"
    if "2201.00350" in url:
        return "FinRL: A Deep Reinforcement Learning Library for Automated Stock Trading in Quantitative Finance"
    if "Neuberger_Berman_Simply_PutWriting.pdf" in url or "Simply_PutWriting.pdf" in url:
        return "Simply Put: The Performance of Cash-Secured Put Writing"
    if "2002.08245" in url:
        return "AutoAlpha: An Efficient Hierarchical Evolutionary Algorithm for Mining Alpha Factors in Quantitative Investment"
    if "2510.21147" in url:
        return "Hierarchical AI Multi-Agent Fundamental Investing: Evidence from China's A-Share Market"
    if "w7613.pdf" in url:
        return "Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation"
    if "2506.22055" in url:
        return "Crypto Price Prediction Using LSTM and XGBoost"
    if "2407.14736" in url:
        return "Is the Difference Between Deep Hedging and Delta Hedging a Statistical Arbitrage?"
    if "2604.08356" in url:
        return "Measuring Strategy-Decay Risk: Minimum Regime Performance and the Durability of Systematic Investing"
    if "2502.15813" in url:
        return "Stock Price Prediction Using a Hybrid LSTM-GNN Model"
    if "2401.06139" in url:
        return "Stockformer: A Price-Volume Factor Stock Selection Model Based on Wavelet Transform and Multi-Task Self-Attention Networks"
    if "sr677.pdf" in url or "681607" in url:
        return "A Simple and Reliable Way to Compute Option-Based Risk-Neutral Distributions"
    if "sr32.pdf" in url:
        return "Option-Implied Probability Distributions and Currency Excess Returns"
    if "ecbwp198.pdf" in url or "2002198.html" in url:
        return "Extracting Risk Neutral Probability Densities by Fitting Implied Volatility Smiles"
    if "bisp06e.pdf" in url:
        return "How Useful Are Implied Distributions? Evidence from Stock-Index Options"
    if "w6656.pdf" in url:
        return "Are Insiders' Trades Informative?"
    if "w30032.pdf" in url or "7645411" in url:
        return "Do Sell-Side Analysts Say “Buy” While Whispering “Sell”?"
    if "feds-notes/bank-lending-to-private-credit" in url:
        return "Bank Lending to Private Credit: Size, Characteristics, and Financial Stability Implications"
    if "feds-notes/private-credit-characteristics" in url:
        return "Private Credit: Characteristics and Risks"
    if "CPP-20250521.pdf" in url:
        return "Could the Growth of Private Credit Pose a Risk to Financial System Stability?"
    if "8412.pdf" in url:
        return "The Pricing of Treasury Bond Futures: The Quality Variation Option"
    if "fairvalue.html" in url:
        return "Calculating Equity Index Futures Fair Value"
    if "fut_hedging.pdf" in url:
        return "Hedging Strategies in Futures and Forward Markets"
    if "hft_lit_review_march_2014.pdf" in url:
        return "Equity Market Structure Literature Review: High Frequency Trading"
    if "NickRoussanov2_29_24-1.pdf" in url:
        return "When Benchmarks Fail: The Causes and Consequences of Negative Oil Prices"
    if "ip-v3-n1-8-debunking-the-roll-yield-myth" in url:
        return "Debunking the Roll Yield Myth in Futures Markets"
    if "deconstructing-futures-returns" in url:
        return "Deconstructing Futures Returns: The Role of Roll Yield"
    if "treasury-futures-basis-spreads.pdf" in url:
        return "Treasury Futures Delivery Options, Basis Spreads, and Delivery Tails"
    if "Chicago2016OptimalExecution.pdf" in url:
        return "Three Models of Market Impact"
    if "MSES.pdf" in url:
        return "Testing Strategies Based on Multiple Signals"
    if "AIA.pdf" in url:
        return "Institutional Investor Attention and Underreaction to News"
    if "Lang%20Pinto%20Sul" in url:
        return "MiFID II Unbundling and Sell-Side Analyst Research"
    if "PesoProblem_Palgrave.pdf" in url:
        return "The Peso Problem in Financial Economics"
    if "AndrewDMannPhDFinal.pdf" in url:
        return "Machine Learning Methods to Exploit the Predictive Power of Open, High, Low, Close (OHLC) Data"
    if "Rhinesmith-JobMarketPaper.pdf" in url:
        return "Conviction and Volume: Measuring the Information Content of Hedge Fund Trading"
    if "DELABORIEDELABATUT" in url:
        return "Advanced Methods in Portfolio Optimization for Trading Strategies and Smart Beta"
    if "2412.04415" in url:
        return "Targeting the Core: A Simple and Effective Method to Attack RAG-Based Agents via Direct LLM Manipulation"
    if "2076-3417/13/20/11378" in url:
        return "A Comprehensive Survey of Recommender Systems Based on Deep Learning"
    if "2673-9909/5/3/76" in url:
        return "Stock Market Prediction Using Machine Learning and Deep Learning Architectures"
    if "379891582" in url:
        return "Analysis of the Application of XGBoost in Exchange-Traded Funds"
    if "diva2:1985833" in url:
        return "A Machine Learning-Based Stock Prediction System Using XGBoost and Random Forests"

    text = raw_text.strip()
    text = re.sub(r"^(?:\[\d+\]|\d+\.)\s*", "", text).strip()
    if not text or text.startswith("http://") or text.startswith("https://") or text.startswith("www."):
        return None

    split_match = re.split(
        r",\s*accessed\b|,\s*https?://|\s+-\s+accessed\b|\s+accessed\s+[A-Z][a-z]+\s+\d+",
        text,
        flags=re.I,
    )
    title_part = split_match[0].strip()

    # Strip prefixes
    title = re.sub(
        r"^(?:Article\s*Title\s*:\s*|Full\s*article\s*:\s*|NOTE\s+|Online\s+Appendix\.\s+|(?:\(?\s*PDF\s*\)?)|\[\s*PDF\s*\]|\[\s*\d{4,5}\.\d{4,5}(?:v\d+)?\s*\])\s*",
        "",
        title_part,
        flags=re.I,
    ).strip()

    # Strip trailing footnote symbols: *, ∗, †, ‡, etc.
    title = re.sub(r"[\*∗†‡]+$", "", title).strip()

    # Strip trailing ellipsis / dots
    title = re.sub(r"\s*\.\.\.\s*$", "", title).strip()

    # Clean source suffixes
    source_suffixes = [
        r"\s*-\s*ResearchGate(?:\s*\(PDF\))?$",
        r"\s*-\s*arXiv(?:\s*\(PDF\))?$",
        r"\s*-\s*arXiv\.org$",
        r"\s*-\s*SSRN(?:\s*Electronic\s*Journal)?$",
        r"\s*-\s*MDPI$",
        r"\s*-\s*ScienceDirect$",
        r"\s*-\s*SpringerLink$",
        r"\s*-\s*Wiley\s*Online\s*Library$",
        r"\s*-\s*JSTOR$",
        r"\s*-\s*IDEAS/RePEc$",
        r"\s*-\s*RePEc$",
        r"\s*-\s*NBER$",
        r"\s*\|\s*NBER$",
        r"\s*-\s*AQR\s*Capital\s*Management$",
        r"\s*\|\s*AQR\s*Capital\s*Management$",
        r"\s*-\s*AQR$",
        r"\s*-\s*Cboe(?:\s*Global\s*Markets)?$",
        r"\s*-\s*CME\s*Group$",
        r"\s*\|\s*CME\s*Group$",
        r"\s*-\s*Bank\s*for\s*International\s*Settlements$",
        r"\s*-\s*Federal\s*Reserve\s*Bank.*$",
        r"\s*-\s*Columbia\s*Business\s*School$",
        r"\s*-\s*NYU\s*Tandon.*$",
        r"\s*-\s*NYU\s*Stern.*$",
        r"\s*-\s*CBS\s*Research\s*Portal$",
        r"\s*-\s*InK@SMU.*$",
        r"\s*-\s*Portfolio\s*Management\s*Research$",
        r"\s*\|\s*Portfolio\s*Management\s*Research$",
        r"\s*-\s*CORE$",
        r"\s*-\s*OpenReview$",
        r"\s*-\s*Alpha\s*Architect$",
        r"\s*-\s*PLOS$",
        r"\s*-\s*Research\s*journals\s*-\s*PLOS$",
        r"\s*-\s*Research\s*journals$",
        r"\s*-\s*American\s*Economic\s*Association$",
        r"\s*\|\s*Request\s*PDF$",
        r"\s*\|\s*Semantic\s*Scholar$",
        r"\s*-\s*Semantic\s*Scholar$",
        r"\s*-\s*Publications\s*-\s*World\s*Economic\s*Forum.*$",
        r"\s*-\s*World\s*Economic\s*Forum.*$",
        r"\s*-\s*Hugging\s*Face$",
        r"\s*-\s*J\.?P\.?\s*Morgan$",
        r"\s*\|\s*J\.?P\.?\s*Morgan.*$",
        r"\s*-\s*Marcos\s*M\.?\s*Lopez\s*de\s*Prado$",
        r"\s*-\s*Federal\s*\.\.\.$",
        r"\s*-\s*Bayes\s*Business\s*School$",
        r"\s*-\s*UC\s*Berkeley\s*EECS$",
        r"\s*-\s*GOV\.UK$",
        r"\s*\|\s*FINRA\.org$",
        r"\s*-\s*Winter\s*Simulation\s*Conference$",
        r"\s*-\s*DiVA\s*portal$",
        r"\s*-\s*Gresham\s*Investment.*$",
        r"\s*-\s*World\s*Economic\s*Forum.*$",
        r"\s*-\s*DoD\s*CIO.*$",
        r"\s*\|\s*ANZ.*$",
        r"\s*-\s*PNC\s*Bank.*$",
        r"\s*-\s*Latham\s*&\s*Watkins.*$",
        r"\s*-\s*Netspar.*$",
        r"\s*-\s*Zenodo.*$",
        r"\s*-\s*Diva-portal\.org.*$",
        r"\s*-\s*KPMG.*$",
        r"\s*-\s*OAPEN\s*Library.*$",
        r"\s*-\s*SciSpace.*$",
        r"\s*-\s*SDM.*$",
        r"\s*-\s*Hillsdale\s*Investment.*$",
        r"\s*-\s*Euronext.*$",
        r"\s*-\s*GCARD.*$",
        r"\s*-\s*Taylor\s*&\s*Francis\s*Online$",
        r"\s*-\s*Kellogg\s*School\s*of\s*Management$",
        r"\s*-\s*Gupea$",
        r"\s*-\s*Arvid\s*Hoffmann$",
        r"\s*-\s*ijrpr$",
        r"\s*-\s*National\s*Bureau\s*of\s*Economic\s*Research$",
        r"\s*\|\s*Annals\s*of\s*Actuarial\s*Science\s*\|\s*Cambridge\s*Core$",
        r"\s*-\s*Princeton\s*Economics\s*Department$",
        r"\s*-\s*University\s*of\s*Toronto$",
        r"\s*-\s*Columbia\s*Math\s*Department$",
        r"\s*-\s*Department\s*of\s*Mathematics$",
        r"\s*-\s*LPSM$",
        r"\s*\|\s*AFME$",
        r"\s*-\s*AFME$",
        r"\s*-\s*David\s*H\s*Bailey$",
        r"\s*-\s*Brookings\s*Institution$",
        r"\s*-\s*The\s*University\s*of\s*Chicago\s*Business\s*Law\s*Review$",
        r"\s*-\s*European\s*Systemic\s*Risk\s*Board$",
        r"\s*-\s*State\s*Street\s*Global\s*Advisors$",
        r"\s*-\s*Fields\s*Institute.*$",
        r"\s*-\s*ACL\s*Anthology$",
        r"\s*\|\s*Stanford\s*Graduate\s*School\s*of\s*Business$",
        r"\s*-\s*mySimon$",
        r"\s*\|\s*International\s*Journal\s*of\s*Theoretical\s*and\s*Applied\s*Finance.*$",
        r"\s*-\s*The\s*Hedge\s*Fund\s*Journal$",
        r"\s*-\s*Columbia\s*Academic\s*Commons$",
        r"\s*-\s*SEC\.gov$",
        r"\s*-\s*PMC$",
        r"\s*-\s*PMC\s*-\s*NIH$",
        r"\s*-\s*Case\s*-\s*Faculty\s*&\s*Research\s*-\s*Harvard\s*Business\s*School$",
        r"\s*\|\s*Citadel\s*Securities$",
        r"\s*\|\s*Portfolio\s*for\s*the\s*Future\s*\|\s*CAIA$",
        r"\s*-\s*Federal\s*Reserve$",
        r"\s*-\s*Risk\.net$",
        r"\s*-\s*CompatibL$",
        r"\s*-\s*Index\s*of\s*/ftp$",
        r"\s*-\s*Ezelman$",
        r"\s*-\s*Toronto\s*Stock\s*Exchange.*$",
        r"\s*-\s*Yale\s*Department\s*of\s*Economics$",
        r"\s*-\s*University\s*of\s*Edinburgh$",
        r"\s*-\s*UiS\s*Brage$",
        r"\s*-\s*Princeton\s*University$",
        r"\s*-\s*Duke\s*Economics$",
        r"\s*-\s*Baruch\s*MFE\s*Program$",
        r"\s*-\s*European\s*Central\s*Bank$",
        r"\s*\|\s*Wellington\s*US\s*Institutional$",
        r"\s*-\s*Wellington\s*Management$",
        r"\s*-\s*International\s*Monetary\s*Fund$",
        r"\s*-\s*FIUnix\s*Faculty\s*Sites\s*\|\s*Florida\s*International\s*University$",
        r"\s*-\s*e-Publications@Marquette$",
        r"\s*\|\s*Robeco\s*Global$",
        r"\s*-\s*Man\s*Group$",
        r"\s*-\s*National\s*Academic\s*Digital\s*Library\s*of\s*Ethiopia$",
        r"\s*-\s*Federal$",
        r"\s*-\s*V-Lab$",
        r"\s*-\s*Portfolio\s*Construction\s*Forum$",
        r"\s*-\s*Imperial\s*Spiral$",
        r"\s*-\s*New\s*York\s*University$",
        r"\s*-\s*CUNY\s*Graduate\s*Center$",
        r"\s*\|\s*SEC\.gov$",
        r"\s*-\s*Department\s*of\s*Econometrics\s*and\s*Statistics$",
        r"\s*-\s*With\s*an\s*Application\s*to\s*Emerging\s*Markets$",
        r"\s*-\s*A\s*Study\s*Across\s*44\s*Countries$",
        r"\s*-\s*A\s*Study\s*Across\s*44\s*Countries.*$",
        r"\s*Maysam\s*Khodayari\s*Gharanchaei.*$",
        r"\s*Kent\s*Daniel\s*Ravi\s*Jagannathan\s*Soohun\s*Kim.*$",
        r"\s*John\s*Hull\s*and\s*Alan\s*White.*$",
        r"\s*PETER\s*CARR\s*-\s*New\s*York\s*University$",
        r"\s*-\s*UC\s*Berkeley\s*Statistics.*$",
        r"\s*-\s*Duke\s*People.*$",
        r"\s*-\s*DukeSpace.*$",
        r"\s*-\s*Christopher\s*Heil.*$",
        r"\s*-\s*Stanford\s*University.*$",
        r"\s*-\s*University\s*of\s*California.*$",
        r"\s*-\s*UCR\s*\|.*$",
        r"\s*\|\s*Bulletin\s*–.*$",
        r"\s*\|\s*FRED\s*\|.*$",
        r"\s*\|\s*Liberty\s*Street\s*Economics.*$",
        r"\s*\|\s*RBA.*$",
        r"\s*\|\s*Man\s*Group.*$",
        r"\s*\|\s*Cboe.*$",
        r"\s*-\s*CFA\s*Institute\s*Research.*$",
        r"\s*-\s*European\s*Financial\s*Management\s*Association.*$",
        r"\s*-\s*MIT.*$",
        r"\s*-\s*NYU\s*Courant.*$",
        r"\s*-\s*kth\s*\.diva.*$",
        r"\s*-\s*Wharton\s*Statistics.*$",
        r"\s*-\s*Federal\s*Reserve\s*Board.*$",
        r"\s*-\s*Computer\s*Science.*$",
        r"\s*-\s*Bank\s*of\s*Canada.*$",
        r"\s*·\s*The\s*Hedge\s*Fund.*$",
        r"\s*-\s*UW\s*Math\s*Department.*$",
        r"\s*-\s*City\s*Research\s*Online.*$",
        r"\s*-\s*LSU\s*Scholarly\s*Repository.*$",
        r"\s*-\s*Princeton\s*DataSpace.*$",
        r"\s*-\s*Imperial\s*College\s*London.*$",
        r"\s*-\s*PubMed.*$",
        r"\s*-\s*IEEE\s*Xplore.*$",
        r"\s*-\s*IMF\s*eLibrary.*$",
        r"\s*-\s*UChicago\s*Math.*$",
        r"\s*-\s*Faculty\s*&\s*Research\s*-\s*Harvard\s*Business\s*School$",
        r"\s*-\s*Research@CBS$",
        r"\s*-\s*Tuck\s*School\s*of\s*Business$",
        r"\s*-\s*UCLA\s*Mathematics$",
        r"\s*-\s*University\s*of\s*Miami$",
        r"\s*-\s*Swarthmore\s*College$",
        r"\s*-\s*IIT\s*Delhi$",
        r"\s*-\s*Mathematical\s*Institute$",
        r"\s*-\s*C\.\s*T\.\s*Bauer\s*College\s*of\s*Business$",
        r"\s*-\s*Cornell\s*eCommons$",
        r"\s*-\s*UC\s*Berkeley\s*Haas$",
        r"\s*-\s*Paul\s*Merage\s*School\s*of\s*Business$",
        r"\s*-\s*The\s*Ohio\s*State\s*University$",
        r"\s*-\s*UConn\s*Finance\s*Department$",
        r"\s*-\s*Rodney\s*L\.\s*White\s*Center.*$",
        r"\s*-\s*ULB\s*:\s*Dok.*$",
        r"\s*-\s*Shanghai\s*Advanced\s*Institute\s*of\s*Finance.*$",
        r"\s*-\s*Chartered\s*Alternative\s*Investment\s*Analyst\s*Association$",
        r"\s*-\s*DiVA$",
        r"\s*-\s*mtu-mujast$",
        r"\s*-\s*Liberty$",
        r"\s*-\s*OpenMarkets$",
        r"\s*-\s*Wharton's\s*Finance\s*Department$",
        r"\s*-\s*The\s*Cupola$",
        r"\s*-\s*Scholars\s*at\s*Harvard$",
        r"\s*-\s*Fulton\s*Forge\s*Student\s*Research\s*Expo$",
        r"\s*-\s*Two\s*Sigma$",
        r"\s*-\s*Law\.Cornell\.Edu$",
        r"\s*-\s*UNSW$",
        r"\s*-\s*Harbert\s*College\s*of\s*Business$",
        r"\s*-\s*Scholars\s*Crossing$",
        r"\s*-\s*Legal\s*Scholarship\s*Repository$",
        r"\s*-\s*UC\s*Berkeley\s*Law$",
        r"\s*-\s*VTechWorks$",
        r"\s*\|\s*Michigan\s*Ross$",
        r"\s*-\s*Duke\s*Law\s*Scholarship\s*Repository$",
        r"\s*-\s*Oliver\s*Wyman$",
        r"\s*-\s*Partners\s*Group$",
        r"\s*-\s*The\s*Wagner\s*Law\s*Group$",
        r"\s*-\s*University\s*of\s*Warwick$",
        r"\s*-\s*LSE$",
        r"\s*-\s*IRIHS$",
        r"\s*-\s*FRASER$",
        r"\s*-\s*SNB$",
        r"\s*-\s*ACFR\s*-\s*AUT$",
        r"\s*-\s*The\s*University\s*of\s*Texas\s*at\s*Dallas$",
        r"\s*\|\s*Research\s*&\s*Policy\s*Center$",
        r"\s*-\s*A&O\s*Shearman$",
        r"\s*-\s*International\s*Transport\s*Forum$",
        r"\s*-\s*Wharton\s*Faculty\s*Platform$",
        r"\s*-\s*World\s*Scientific\s*Publishing$",
        r"\s*-\s*Hester\s*Law\s*Group$",
        r"\s*-\s*University\s*of\s*Notre\s*Dame$",
        r"\s*-\s*Oxford\s*Academic$",
        r"\s*-\s*UCL\s*Discovery\s*-\s*University\s*College\s*London$",
        r"\s*-\s*Cornell\s*Law\s*School$",
        r"\s*-\s*Bank\s*of\s*England$",
        r"\s*-\s*Federal\s*Reserve\s*Bank\s*of\s*Minneapolis$",
        r"\s*-\s*CFA\s*Institute.*$",
        r"\s*-\s*PMC(?:\s*\(PDF\))?$",
        r"\s*-\s*PhilArchive$",
        r"\s*-\s*The\s*Harvard\s*Law\s*School\s*Forum.*$",
        r"\s*Emory\s*University$",
        # Batch 6 source suffixes
        r"\s*-\s*American\s*Economic\s*Association.*$",
        r"\s*-\s*CFA\s*Institute.*$",
        r"\s*-\s*CFA\s*Institute\s*Blogs.*$",
        r"\s*-\s*Climate\s*Law\s*Blog.*$",
        r"\s*-\s*Columbia\s*University.*$",
        r"\s*-\s*Computer\s*and\s*Information\s*Science.*$",
        r"\s*-\s*Dacheng\s*Xiu.*$",
        r"\s*-\s*DiVA.*$",
        r"\s*-\s*DiVA\s*portal.*$",
        r"\s*-\s*Documents\s*&\s*Reports.*$",
        r"\s*-\s*ETF\s*Market\s*Canada.*$",
        r"\s*-\s*European\s*Union.*$",
        r"\s*-\s*Fordham\s*University\s*Faculty.*$",
        r"\s*-\s*Frontiers.*$",
        r"\s*-\s*HKUST\s*Math\s*Department.*$",
        r"\s*-\s*Hillsdale\s*Investment\s*Management.*$",
        r"\s*-\s*Jacobs\s*Levy\s*Center.*$",
        r"\s*-\s*LSU\s*Scholarly\s*Repository.*$",
        r"\s*-\s*Macquarie\s*University.*$",
        r"\s*-\s*Mason\s*Experimental\s*Geometry\s*Lab.*$",
        r"\s*-\s*NYU\s*Stern.*$",
        r"\s*-\s*OSU\s*Math.*$",
        r"\s*-\s*PMC\s*-\s*NIH.*$",
        r"\s*-\s*Phenix\s*Capital.*$",
        r"\s*-\s*PubMed\s*Central.*$",
        r"\s*-\s*Purdue\s*University\s*Graduate\s*School.*$",
        r"\s*-\s*Robeco\.com.*$",
        r"\s*-\s*Robeco\s*USA.*$",
        r"\s*-\s*Shanghai\s*Advanced\s*Institute\s*of\s*Finance.*$",
        r"\s*-\s*Simon\s*Fraser\s*University.*$",
        r"\s*-\s*Stanford\s*University.*$",
        r"\s*-\s*State\s*Street\s*Global\s*Advisors.*$",
        r"\s*-\s*State\s*Street\s*Investment\s*Management.*$",
        r"\s*-\s*Stevens\s*Institute.*$",
        r"\s*-\s*USC\s*Dornsife.*$",
        r"\s*-\s*University\s*of\s*Hawaii.*$",
        r"\s*-\s*University\s*of\s*Notre\s*Dame.*$",
        r"\s*-\s*Web\s*page\s*for\s*Ron\s*Shonkwiler.*$",
        r"\s*-\s*stat\.berkeley\.edu.*$",
        r"\s*-\s*uu\s*\.diva.*$",
        r"\s*\|\s*CFA\s*Institute.*$",
        r"\s*\|\s*Cboe.*$",
        r"\s*\|\s*Harvard\s*Kennedy\s*School.*$",
        r"\s*\|\s*Jacobs\s*Levy\s*Center.*$",
        r"\s*\|\s*Journal\s*of\s*Financial\s*and\s*Quantitative\s*Analysis.*$",
        r"\s*\|\s*Robeco\s*Global.*$",
        r"\s*\|\s*Yale\s*Insights.*$",
    ]
    for pattern in source_suffixes:
        title = re.sub(pattern, "", title, flags=re.I).strip()

    title = title.strip(" -–—,;:\'\"*∗†‡")
    if len(title) < 5 or title.lower().startswith("http") or title.lower().startswith("www."):
        return None

    # Filter out generic non-papers / marketing / table of contents / fragments
    lower_t = title.lower()
    reject_titles = [
        "table of contents", "references", "works cited", "introduction",
        "conclusion", "abstract", "research", "search", "publications",
        "algorithmic trading", "technical article", "options market at a glance",
        "mastering fx arbitrage in 2025", "the book of jargon", "consolidated half-year report",
        "department of defense zero trust reference architecture", "reform of the u.s. capital framework",
        "summer 2021", "financial volatility and the leverage effect",
        "what is a market maker?", "market makers vs. market takers",
        "quants of the year: leif andersen, michael pykhtin and alexander sokol",
        "alexander sokol wins quant of the year", "credit curve bootstrapping",
        "frb: finance and economics discussion series: screen reader version - 201010",
        "crr3 implementation timeline: live since 2025, the final sprint to frtb",
        "reward-dense mdp. the intermediate reward is designed for the legal but",
        "exchange-traded funds: a small entity compliance guide",
        "master the mechanics of etf trading", "how etfs are created and redeemed",
        "notice of amendments and commission approval - market-on-close system and summary of comment letters and tsx responses",
        "united states commodity funds llc and united states oil fund, lp",
        "united states oil fund, lp", "kathrin glau zorana grbac matthias scherer rudi",
        "analyzing code compatibility, equivalence, and similarity to",
        "alpha discovery via grammar-guided learn- ing and",
        "corgi: a tool-agnostic framework for compiling",
        "about the aqr data library", "an academic-quality data library for practitioners",
        "aqr insight award", "clifford s. asness's research works", "factor timing",
        "journal article", "working paper", "aqr capital management", "cliff's perspectives",
        "value investing bibliography", "momentum bibliography", "carry bibliography",
        "bibliography", "defensive equity bibliography", "style bibliography",
        "defensive research bibliography", "carry", "white papers", "aqr momentum indices, monthly",
        "pushing past the boundaries of esg investing: aqr capital management",
        "hedge fund strategies", "what is api design? principles & best practices",
        "the all weather portfolio: built for any forecast", "a new era of higher inflation risks",
        "the all weather story", "from carrier pigeons to ai – gaining an edge with alternative data",
        "aia labs: the future of investment intelligence", "option selling has become consensus: its impacts",
        "new research shows options-based strategies can generate higher gross premiums with less volatility over traditional asset classes",
        "cliff's perspective resisting the siren song of factor timing",
        "dimensional equity investing in an active etf structure",
        "solutions, proofs, data disclaimer 1. cds bootstrapping procedure",
        "cre50 - counterparty credit risk definitions and terminology",
        "mar50 - credit valuation adjustment framework",
        "counterparty credit risk in basel iii - executive summary",
        "chapter 21: option valuation", "foreign exchange in practice",
        "correlation analysis documentation", "data sets",
        "forticode: a benchmark for evaluating the robustness of code",
        "meet allw: the spdr® bridgewater® all weather® etf",
        "treasury term premia", "5-year, 5-year forward inflation expectation rate",
        "vix volatility products", "8 three types of convergence",
        "1 stochastic taylor expansion", "conditional expectation definition 1.",
        "the lagrange function for general optimization and the dual problem",
        "using lstm in stock prediction and quantitative trading - cs230",
        "accessed november 14, 2025", "what are advantages of autoencoder vs cnn",
        "variance futures", "2025 u.s. equities year in review",
        "venn pillar series", "what is the volatility risk premium?",
        "what is the best risk measure in practice?", "alternative data market size",
        "social dysfunction prediction", "lecture ",
        "an introduction to functional analysis contents", "cboe u.s. equities market volume summary",
        "the term premium | fred blog", "why the term premium isn't as boring as it sounds",
        "why etf growth is booming", "index insights: may",
        "cboe to launch new", "white paper shows volatility risk premium facilitated",
        "acm term premium archives", "understanding short sale volume data on finra",
        "regulatory notice 21-19", "reporting firm 10 second compliance report card",
        "statistica sinica preprint no", "short sale volume",
        "principle of maximum entropy: simple form", "minimizing shortfall 1 introduction",
        "nber working paper series an empirical decomposition of risk and liquidity in nominal and inflation-indexed government bonds car",
        "multilayer perceptron modeling for social dysfunction prediction based on general health factors in an iranian women sample",
        "robo-advisors: a portfolio management perspective jonathan walter lam",
        "two sigma", "gdpnow", "day trading", "vix options", "vix futures", "journal",
        "innovations",
        "e-mini s&p 500 product overview", "e-mini s&p 500 futures overview",
        "e-mini s&p select sector futures overview", "e-mini nasdaq-100 futures contract specs",
        "nasdaq-100 futures and options", "e-mini s&p 500 options contract specs",
        "e-mini nasdaq-100 futures overview", "block and btic liquidity providers",
        "cme group fee list 2026", "january-2025-market-data-fee-list.pdf",
        "e-mini s&p 500 futures margins", "26 u.s. code § 1256",
        "26 u.s. code § 1259", "ownership form codes",
        "insider trading arrangements and related disclosures",
        "disclosure of hedging by employees, officers and directors",
        "insider transactions and forms 3, 4, and 5", "edgar full text search",
        "17 cfr § 240.10b5-1", "what factors constitute insider trading?",
        "martha stewart", "sec charges", "the galleon insider trading case",
        "inside this insider trading loophole", "new virginia tech study reveals",
        "new study on insider trading discovers flaws", "private credit's surge has investors excited",
        "private credit — impact on banks", "citi and apollo announce",
        "private markets outlook 2026", "growth of nonbanks is revealing new financial stability risks",
        "tactical asset allocation & erisa plans", "performance measurement & attribution",
        "econ 2021 - financial economics i", "math 181 lecture 14",
        "the black-scholes model", "ch 2. black-scholes model",
        "640:495 mathematical finance", "quant trading vs traditional trading",
        "man ahl", "why the market should watch special u.s. repo",
        "how cme repofunds rate futures enhance bond basis trading",
        "treasury analytics user guide", "chapter 14p hard red spring wheat futures",
        "vomitoxin in spring", "mifid ii: assessing the impact of research unbundling",
        "federal court approves global research analyst settlement",
        "sec announces enforcement results for fiscal year 2024",
        "retail investors lose big in options markets",
        "retail investors play a losing game with complex options",
        "ai: a landmark report to guide financial institutions",
        "key challenges and regulatory considerations",
        "explainable ai in finance | research & policy center",
        "non-commodity agricultural price hedging",
        "balancing efficiency and resilience in multimodal supply chains",
        "hedging strategies in carbon emission price dynamics",
        "understanding the impact of tiktok's recommendation algorithm",
        "combining content-based and collaborative filtering for job recommendation",
        "crypto price prediction using lstm+xgboost identify applicable funding agency",
        "optimizing smart grid load forecasting",
        "a scalable rf-xgboost framework for financial fraud mitigation",
        "high-frequency trading: an innovative solution to address key issues",
        "a study on backtest metrics for financial analysis",
        "arxiv.org", "accessed december 27, 2025", "accessed november 27, 2025",
        "tactical asset allocation: the flexibility advantage",
        "what is strategic asset allocation?",
        "building a tactical asset allocation overlay with derivatives",
        "performance attribution",
        "explainable ai in finance",
    ]
    for rt in reject_titles:
        if lower_t == rt or lower_t.startswith(rt):
            return None

    if "client specifications" in lower_t or "interface specification" in lower_t:
        return None

    return title


def normalize_title(t: str) -> str:
    """Normalize paper title for robust deduplication."""
    s = re.sub(r"\s*\(\d+\)\s*$", "", t)
    s = re.sub(r"[\*∗†‡]", "", s)
    s = re.sub(r"[^\w\s]", " ", s)
    tokens = s.lower().split()
    normalized_tokens = []
    for tok in tokens:
        if tok in ["premiums", "premia"]:
            normalized_tokens.append("premium")
        elif tok in ["calls"]:
            normalized_tokens.append("call")
        elif tok in ["models"]:
            normalized_tokens.append("model")
        elif tok in ["strategies"]:
            normalized_tokens.append("strategy")
        else:
            normalized_tokens.append(tok)
    return " ".join(normalized_tokens)


def format_markdown_cell(s: str) -> str:
    """Escape markdown pipes and strip newlines."""
    return s.replace("|", "\\|").replace("\n", " ").strip()


def build_why_sentence(norm_t: str, title: str, tags: str) -> str | None:
    """Return the curated, specific Why sentence for this citation, or None.

    Returning None means "not individually reviewed" -- the caller must skip
    the citation entirely rather than invent one. This used to also try a
    substring match and a >=70%-token-overlap fuzzy match against WHY_MAP,
    then fall back to a templated sentence ("Investigates the theoretical
    mechanics... of {title} in {tag}") when nothing matched. Both were
    removed: the fuzzy matching could (and did, confirmed live) assign one
    paper's specific description to a different paper with a similar title
    -- e.g. "Understanding the Correlation Risk Premium" and "Understanding
    the Volatility Risk Premium" got identical, and for one of them wrong,
    Why text this way. The template fallback produced a fabricated-looking
    but content-free sentence that inflated to ~22% of all gdocs-sourced
    rows by batch 3, since it silently qualifies as "specific enough" if you
    only skim it. Neither failure mode is acceptable for a research backlog
    -- an exact match or nothing.
    """
    return WHY_MAP.get(norm_t)


def update_candidates_file(
    candidates_file: Path,
    candidates: list[dict],
    dry_run: bool = False,
) -> tuple[int, int]:
    """Update FOLLOWUP-CANDIDATES.md with new and merged candidate rows."""
    if not candidates_file.exists():
        raise FileNotFoundError(f"Candidates file not found: {candidates_file}")

    content = candidates_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Parse existing candidate rows
    existing_by_norm_title: dict[str, dict] = {}
    table_start_idx = -1
    passed_on_idx = -1

    for idx, line in enumerate(lines):
        if line.startswith("| Title (best guess)"):
            table_start_idx = idx
        elif line.startswith("## Passed on"):
            passed_on_idx = idx
        elif table_start_idx != -1 and passed_on_idx == -1 and line.startswith("|") and not line.startswith("| :---") and not line.startswith("| ---"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 6:
                norm_t = normalize_title(parts[0])
                existing_by_norm_title[norm_t] = {
                    "line_idx": idx,
                    "title": parts[0],
                    "authors_year": parts[1],
                    "why": parts[2],
                    "tags": parts[3],
                    "surfaced_by": parts[4],
                    "doc_id": parts[5],
                    "status": parts[6] if len(parts) > 6 else "",
                }

    merged_count = 0
    new_rows_to_insert: list[str] = []

    for cand in candidates:
        norm_t = cand["norm_title"]
        article_links_str = ", ".join(cand["surfaced_by"])
        doc_ids_str = ", ".join(cand["doc_ids"])

        if norm_t in existing_by_norm_title:
            # Merge with existing row
            ex = existing_by_norm_title[norm_t]
            line_idx = ex["line_idx"]

            # Merge surfaced_by
            existing_surfaced = [s.strip() for s in ex["surfaced_by"].split(",") if s.strip()]
            for link in cand["surfaced_by"]:
                if link not in existing_surfaced:
                    existing_surfaced.append(link)
            new_surfaced_str = ", ".join(existing_surfaced)

            # Merge doc_ids
            existing_docs = [d.strip() for d in ex["doc_id"].split(",") if d.strip()]
            for did in cand["doc_ids"]:
                if did and did not in existing_docs:
                    existing_docs.append(did)
            new_docs_str = ", ".join(existing_docs)

            # Update line in lines
            lines[line_idx] = (
                f"| {format_markdown_cell(ex['title'])} "
                f"| {format_markdown_cell(ex['authors_year'])} "
                f"| {format_markdown_cell(ex['why'])} "
                f"| {format_markdown_cell(ex['tags'] or cand['tags'])} "
                f"| {format_markdown_cell(new_surfaced_str)} "
                f"| {format_markdown_cell(new_docs_str)} "
                f"| {format_markdown_cell(ex['status'])} |"
            )
            merged_count += 1
        else:
            why_sentence = cand["why"]
            row_str = (
                f"| {format_markdown_cell(cand['title'])} "
                f"| "
                f"| {format_markdown_cell(why_sentence)} "
                f"| {format_markdown_cell(cand['tags'])} "
                f"| {format_markdown_cell(article_links_str)} "
                f"| {format_markdown_cell(doc_ids_str)} "
                f"| |"
            )
            new_rows_to_insert.append(row_str)

    # Insert new rows before '## Passed on'
    if not dry_run:
        target = "## Passed on"
        current_text = "\n".join(lines)
        if target in current_text:
            parts = current_text.split(target, 1)
            new_content = (
                parts[0].rstrip()
                + "\n"
                + "\n".join(new_rows_to_insert)
                + "\n\n"
                + target
                + parts[1]
            )
        else:
            new_content = current_text.rstrip() + "\n" + "\n".join(new_rows_to_insert) + "\n"

        candidates_file.write_text(new_content, encoding="utf-8")

    return len(new_rows_to_insert), merged_count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--articles-dir",
        type=Path,
        default=DEFAULT_ARTICLES_DIR,
        help=f"Path to article TS directory (default: {DEFAULT_ARTICLES_DIR})",
    )
    parser.add_argument(
        "--matches",
        type=Path,
        default=DEFAULT_MATCHES_PATH,
        help=f"Path to article-exact-matches.md (default: {DEFAULT_MATCHES_PATH})",
    )
    parser.add_argument(
        "--candidates-file",
        type=Path,
        default=DEFAULT_CANDIDATES_PATH,
        help=f"Path to FOLLOWUP-CANDIDATES.md (default: {DEFAULT_CANDIDATES_PATH})",
    )
    parser.add_argument(
        "--state-file",
        type=Path,
        default=DEFAULT_STATE_PATH,
        help=f"Path to classified_state.json (default: {DEFAULT_STATE_PATH})",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.35,
        help="Delay in seconds between fetches (default: 0.35)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Extract and filter without writing to FOLLOWUP-CANDIDATES.md",
    )
    parser.add_argument(
        "--extracted-state-file",
        type=Path,
        default=DEFAULT_EXTRACTED_STATE_PATH,
        help=f"Path to extracted_state.json, tracks slugs already processed (default: {DEFAULT_EXTRACTED_STATE_PATH})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-process slugs already recorded in extracted_state.json (normally skipped)",
    )

    args = parser.parse_args()
    start_time = time.time()

    research_papers_state = load_classified_research_papers(args.state_file)
    print(f"Loaded {len(research_papers_state)} research-paper entries from state.")

    # Skip slugs already extracted in a prior run -- re-fetching and re-deriving
    # the same doc's citations every batch was silently undoing manual fixes
    # (a row deleted by hand as a duplicate would just get re-added as "new"
    # next run, since this script has no memory of what was manually curated).
    extracted_state: dict = {}
    if args.extracted_state_file.exists():
        try:
            with open(args.extracted_state_file, "r", encoding="utf-8") as f:
                extracted_state = json.load(f)
        except Exception:
            extracted_state = {}

    if args.force:
        target_slugs = set(research_papers_state.keys())
    else:
        already = set(extracted_state.keys())
        target_slugs = set(research_papers_state.keys()) - already
        skipped = len(research_papers_state) - len(target_slugs)
        if skipped:
            print(f"Skipping {skipped} slugs already extracted in a prior run "
                  f"(use --force to re-process).")

    articles_meta = load_article_metadata(args.articles_dir, target_slugs)
    doc_ids = load_doc_ids(args.matches)

    print(f"Fetching citations across {len(articles_meta)} published Google Docs...")

    raw_citations: list[dict] = []
    for idx, (slug, art_info) in enumerate(articles_meta.items(), 1):
        url = art_info.get("google_doc")
        if not url:
            print(f"[{idx}/{len(articles_meta)}] {slug}: No published URL, skipping.")
            continue

        print(f"[{idx}/{len(articles_meta)}] Fetching citations for {slug}...")
        extracted = fetch_published_doc_citations(url)
        doc_id = doc_ids.get(slug, "")
        tags = research_papers_state[slug].get("tags", "")

        for item in extracted:
            raw_citations.append(
                {
                    "slug": slug,
                    "article_title": art_info["title"],
                    "doc_id": doc_id,
                    "raw_text": item["raw_text"],
                    "url": item["url"],
                    "tags": tags,
                }
            )

        if args.delay > 0:
            time.sleep(args.delay)

    total_citations = len(raw_citations)
    print(f"\nExtracted {total_citations} total raw citation items.")

    # Filter and deduplicate
    candidates_map: dict[str, dict] = {}
    passed_domain_prefilter_count = 0
    filtered_out_count = 0

    for c in raw_citations:
        url = c.get("url", "")
        raw_text = c.get("raw_text", "")
        ok, domain_reason = is_domain_allowed(url)
        if not ok:
            filtered_out_count += 1
            continue

        passed_domain_prefilter_count += 1

        rej_path, path_reason = is_url_path_rejected(url)
        if rej_path:
            filtered_out_count += 1
            continue

        title = clean_paper_title(raw_text, url)
        if not title:
            filtered_out_count += 1
            continue

        norm_t = normalize_title(title)
        article_link = f"[{c['article_title']}](https://www.sophie-ai-finance.com/articles/{c['slug']})"
        doc_id = c["doc_id"]
        why_text = build_why_sentence(norm_t, title, c.get("tags", ""))
        if why_text is None:
            # No curated WHY_MAP entry -- skip rather than fabricate. Add a
            # real, specific entry to WHY_MAP above (or write one for this
            # citation as you review it) instead of letting this citation
            # silently drop; it's only silent here to keep the loop simple,
            # not a signal that skipping is the desired end state.
            filtered_out_count += 1
            continue

        if norm_t not in candidates_map:
            candidates_map[norm_t] = {
                "title": title,
                "norm_title": norm_t,
                "url": url,
                "why": why_text,
                "tags": c.get("tags", ""),
                "surfaced_by": [article_link],
                "doc_ids": [doc_id] if doc_id else [],
                "slugs": [c["slug"]],
            }
        else:
            if article_link not in candidates_map[norm_t]["surfaced_by"]:
                candidates_map[norm_t]["surfaced_by"].append(article_link)
            if doc_id and doc_id not in candidates_map[norm_t]["doc_ids"]:
                candidates_map[norm_t]["doc_ids"].append(doc_id)
            if c["slug"] not in candidates_map[norm_t]["slugs"]:
                candidates_map[norm_t]["slugs"].append(c["slug"])

    candidates_list = list(candidates_map.values())
    print(f"\n--- Self-Check Summary ---")
    print(f"Total citations found: {total_citations}")
    print(f"Passed domain pre-filter: {passed_domain_prefilter_count}")
    print(f"Passed full quality filter & deduped: {len(candidates_list)} unique candidates")
    print(f"Filtered out: {filtered_out_count}")

    multi_source = [c for c in candidates_list if len(c["surfaced_by"]) > 1]
    print(f"Multi-source candidates (cited across >1 article): {len(multi_source)}")

    print(f"\n--- 5 Example Rows ---")
    for ex_idx, ex_c in enumerate(candidates_list[:5], 1):
        print(f"[{ex_idx}] Title      : {ex_c['title']}")
        print(f"    Why        : {ex_c['why']}")
        print(f"    Tags       : {ex_c['tags']}")
        print(f"    Surfaced by: {', '.join(ex_c['surfaced_by'])}")
        print(f"    Doc ID     : {', '.join(ex_c['doc_ids'])}")
        print()

    if args.dry_run:
        print(f"[Dry Run] Would update {args.candidates_file} with {len(candidates_list)} candidates.")
    else:
        new_added, merged = update_candidates_file(args.candidates_file, candidates_list)
        print(f"Successfully added {new_added} new candidate rows and merged {merged} rows in {args.candidates_file}")

        # Mark these slugs as extracted so a future run doesn't re-fetch and
        # re-derive them from scratch (which silently undoes manual fixes).
        for slug in target_slugs:
            extracted_state[slug] = {"extracted_at": time.strftime("%Y-%m-%d")}
        args.extracted_state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(args.extracted_state_file, "w", encoding="utf-8") as f:
            json.dump(extracted_state, f, indent=2, ensure_ascii=False)

    print(f"Completed in {time.time() - start_time:.2f}s")


if __name__ == "__main__":
    main()
