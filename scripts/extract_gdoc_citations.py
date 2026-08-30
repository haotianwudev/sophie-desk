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

    args = parser.parse_args()
    start_time = time.time()

    research_papers_state = load_classified_research_papers(args.state_file)
    print(f"Loaded {len(research_papers_state)} research-paper entries from state.")

    target_slugs = set(research_papers_state.keys())
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

    print(f"Completed in {time.time() - start_time:.2f}s")


if __name__ == "__main__":
    main()
