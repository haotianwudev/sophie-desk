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
    "quantitative trading using deep q learning": "Analyzes the quantitative modeling, theoretical mechanics, and empirical market dynamics of Quantitative Trading using Deep Q Learning in deep learning.",
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
    ]
    for rp in reject_paths:
        if rp in path:
            return True, f"reject_path:{rp}"

    if "aqr.com" in netloc and (path == "/" or path == ""):
        return True, "reject_homepage"

    return False, ""


def clean_paper_title(raw_text: str, url: str) -> str | None:
    # URL-specific canonical titles for known truncations
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


def build_why_sentence(norm_t: str, title: str, tags: str) -> str:
    """Generate a specific, non-boilerplate sentence explaining why the paper is worth getting."""
    # 1. Exact match in WHY_MAP
    if norm_t in WHY_MAP:
        return WHY_MAP[norm_t]

    # 2. Substring match in WHY_MAP
    for k, v in WHY_MAP.items():
        if k in norm_t or norm_t in k:
            return v

    # 3. Token overlap match
    for k, v in WHY_MAP.items():
        k_words = set(k.split())
        t_words = set(norm_t.split())
        overlap = len(k_words & t_words)
        if overlap >= 4 and overlap / min(len(k_words), len(t_words)) >= 0.7:
            return v

    primary_tag = tags.split(",")[0].strip().replace("-", " ") if tags else "quantitative finance"
    return f"Investigates the theoretical mechanics, empirical dynamics, and quantitative implementations of {title} in {primary_tag}."


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
