# Source catalog

199 works. Generated from `sources/catalog.csv` by `scripts/build_graph.py`; edit the CSV, not this file.

Verification column: **V** = verified this session (abstract-level web check); **K** = well-known prior knowledge, not re-checked this session; **I** = indexed from the curated Awesome-Routing-LLMs list only.

## Surveys and indexes (5)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| varangot2025doing | Doing More with Less: Implementing Routing Strategies in LLM-Based Systems (survey; defines router vs MoE gating) | 2025 | arXiv | [arXiv:2502.00409](https://arxiv.org/abs/2502.00409) | V | Defines router as external component selecting among a candidate pool under budget |
| hkustgz2026quals | A Survey on LLM Routing: Objectives Methods and Evaluation (PhD qualifying exam talk) | 2026 | talk | [link](https://dsa.hkust-gz.edu.cn/blog/2026/05/28/a-survey-on-llm-routing-objectivesmethods-and-evaluation/) | V | Not a paper; useful objectives/methods/evaluation framing |
| adaptivecomp2026 | Adaptive Computation in the LLM Era: A Unified Survey of Routing, Cascades, and Test-Time Scaling | 2026 | Cambridge Open Engage preprint | [link](https://www.cambridge.org/engage/coe/article-details/6a2fa5614770e67d92f5bb0c) | V | Routing/cascades/TTS as budgeted sequential decisions; audits 15 systems; savings often not comparable (router/verifier/queue costs miscounted) |
| awesome-routing-llms | Awesome-Routing-LLMs (curated list) | 2026 | GitHub | [link](https://github.com/MilkThink-Lab/Awesome-Routing-LLMs) | V | Index used to seed this catalog (~160 entries) |
| moslem2026survey | Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey | 2026 | arXiv | [arXiv:2603.04445](https://arxiv.org/abs/2603.04445) | V | Moslem & Kelleher; most direct survey of routing + cascading |

## Background and adjacent ideas (4)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| shazeer2017moe | Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer | 2017 | ICLR | [arXiv:1701.06538](https://arxiv.org/abs/1701.06538) | K | Intra-model routing ancestor; contrast with inter-model routing |
| fedus2021switch | Switch Transformers | 2021 | JMLR | [arXiv:2101.03961](https://arxiv.org/abs/2101.03961) | K | Top-1 expert routing inside one model |
| leviathan2023spec | Fast Inference from Transformers via Speculative Decoding | 2023 | ICML | [arXiv:2211.17192](https://arxiv.org/abs/2211.17192) | K | Small-large collaboration at token level without quality loss |
| routingllm2026 | RoutingLLM: Boosting LLM Performance for Network Routing | 2026 | ICASSP | ieee:11461033 | I | Name clash: network routing not model routing |

## Pre-generation routers: predictive scoring (30)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| lu2023zooter | Routing to the Expert: Efficient Reward-guided Ensemble of LLMs (Zooter) | 2023 | NAACL 2024 | [arXiv:2311.08692](https://arxiv.org/abs/2311.08692) | K | Distills reward-model scores into a query router |
| hari2023tryage | Tryage: Real-time Intelligent Routing of User Prompts to LLMs | 2023 | arXiv | [arXiv:2308.11601](https://arxiv.org/abs/2308.11601) | I | Perceptive router predicting downstream loss per expert model |
| srivatsa2024multipleminds | Harnessing the Power of Multiple Minds: Lessons Learned from LLM Routing | 2024 | NAACL WS | [arXiv:2405.00467](https://arxiv.org/abs/2405.00467) | V | Early negative-ish result: routers struggle to beat best single model on reasoning |
| ding2024hybrid | Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing | 2024 | ICLR | [arXiv:2404.14618](https://arxiv.org/abs/2404.14618) | K | BERT router predicts quality gap small vs large; tunable threshold at test time |
| ong2024routellm | RouteLLM: Learning to Route LLMs with Preference Data | 2024 | ICLR 2025 | [arXiv:2406.18665](https://arxiv.org/abs/2406.18665) | V | Strong/weak binary routers from Chatbot Arena preferences (MF; BERT; causal LLM; SW-ranking) |
| stripelis2024tensoropera | TensorOpera Router: A Multi-Model Router for Efficient LLM Inference | 2024 | EMNLP Industry | [arXiv:2408.12320](https://arxiv.org/abs/2408.12320) | I |  |
| universal2024correctness | Universal LLM Routing with Correctness-Based Representation | 2024 | ICLR WS | openreview:86eGohKPyy | I |  |
| agentrouter2025 | AgentRouter (knowledge-graph-guided routing) | 2025 | arXiv | [arXiv:2510.05445](https://arxiv.org/abs/2510.05445) | I |  |
| ding2025bestroute | BEST-Route: Adaptive LLM Routing with Test-Time Optimal Compute | 2025 | ICML | [arXiv:2506.22716](https://arxiv.org/abs/2506.22716) | V | Microsoft; routes to (model, n samples); up to 60% cost cut with <1% quality drop (authors) |
| zhang2025capability | Capability Instruction Tuning (Model-SAT) | 2025 | AAAI | [arXiv:2502.17282](https://arxiv.org/abs/2502.17282) | I | Model capability representation + aptitude test for routing |
| iclrouter2025 | ICL-Router: In-Context Learned Model Representations for LLM Routing | 2025 | AAAI | [arXiv:2510.09719](https://arxiv.org/abs/2510.09719) | I |  |
| song2025irtrouter | IRT-Router: Effective and Interpretable Multi-LLM Routing via Item Response Theory | 2025 | ACL | [arXiv:2506.01048](https://arxiv.org/abs/2506.01048) | V | Psychometric IRT; 20 LLMs x 12 datasets; online warm-up for cold start; interpretable ability/difficulty |
| uncert2025route | Leveraging Uncertainty Estimation for Efficient LLM Routing | 2025 | ICML WS | [arXiv:2502.11021](https://arxiv.org/abs/2502.11021) | I |  |
| metarouter2025 | Meta-Router | 2025 | ICLR 2026 | [arXiv:2509.25535](https://arxiv.org/abs/2509.25535) | I |  |
| onehead2025 | One Head, Many Models | 2025 | arXiv | [arXiv:2509.09782](https://arxiv.org/abs/2509.09782) | I |  |
| frick2025p2l | Prompt-to-Leaderboard (P2L) | 2025 | ICML | [arXiv:2502.14855](https://arxiv.org/abs/2502.14855) | V | Prompt-specific Bradley-Terry leaderboard; used as a router |
| jitkrittum2025uniroute | Universal Model Routing for Efficient LLM Inference (UniRoute) | 2025 | arXiv/ICLR WS | [arXiv:2502.08773](https://arxiv.org/abs/2502.08773) | V | Represent each LLM by its error vector on a small set of prompts -> handles unseen models |
| zerorouter2026 | Breaking Model Lock-in: Cost-Efficient Zero-Shot LLM Routing via a Universal Latent Space (ZeroRouter) | 2026 | arXiv | [arXiv:2601.06220](https://arxiv.org/abs/2601.06220) | V | Model-agnostic difficulty latent space; onboard new models with anchor queries |
| consroute2026 | ConsRoute | 2026 | arXiv | [arXiv:2603.21237](https://arxiv.org/abs/2603.21237) | I |  |
| dars2026 | DARS: From Sampled Outcomes to Capability Distributions | 2026 | arXiv | [arXiv:2606.06924](https://arxiv.org/abs/2606.06924) | I | Models stochastic correctness as distributions rather than single labels |
| dmr2026 | DMR: Dynamic Mix Precision Routing | 2026 | arXiv | [arXiv:2602.02711](https://arxiv.org/abs/2602.02711) | I | Routes across quantization levels of same model |
| haps2026 | HAPS | 2026 | arXiv | [arXiv:2601.05903](https://arxiv.org/abs/2601.05903) | I |  |
| ir3de2026 | IR3DE | 2026 | ICML WS | [arXiv:2606.06098](https://arxiv.org/abs/2606.06098) | I |  |
| nvidia2026prefill | LLM Router: Rethinking Routing with Prefill Activations | 2026 | arXiv | [arXiv:2603.20895](https://arxiv.org/abs/2603.20895) | V | Uses internal prefill activations instead of semantic embeddings as routing signal |
| lugoloobi2026encode | LLMs Encode Their Failures: Predicting Success from Pre-Generation Activations | 2026 | ICLR | [arXiv:2602.09924](https://arxiv.org/abs/2602.09924) | V | Linear probes on pre-generation activations predict success; model-specific difficulty differs from human; routing beats best single model, up to 70% cost cut on MATH |
| logrouter2026 | LogRouter | 2026 | arXiv | [arXiv:2605.18015](https://arxiv.org/abs/2605.18015) | I |  |
| odar2026 | ODAR | 2026 | arXiv | [arXiv:2602.23681](https://arxiv.org/abs/2602.23681) | I |  |
| routerhgc2026 | ROUTERHGC | 2026 | ACL Findings | aclanthology:2026.findings-acl.1589 | I |  |
| switchcraft2026 | Switchcraft | 2026 | arXiv | [arXiv:2605.07112](https://arxiv.org/abs/2605.07112) | I |  |
| trouter2026 | TRouter: Task-Aware LLM Routing (cold start) | 2026 | ACL | aclanthology:2026.acl-long.1007 | I |  |

## Pre-generation routers: representation matching (15)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| zhuang2024embedllm | EmbedLLM: Learning Compact Representations of LLMs | 2024 | ICLR 2025 | [arXiv:2410.02223](https://arxiv.org/abs/2410.02223) | K | Learned model embeddings reused for routing and accuracy prediction |
| chen2024routerdc | RouterDC: Query-Based Router by Dual Contrastive Learning | 2024 | NeurIPS | [arXiv:2409.19886](https://arxiv.org/abs/2409.19886) | K | Contrastive alignment of query and LLM embeddings |
| tran2025archrouter | Arch-Router: Aligning LLM Routing with Human Preferences | 2025 | arXiv | [arXiv:2506.16655](https://arxiv.org/abs/2506.16655) | V | 1.5B generative router mapping queries to user-defined (domain action) policies; add models without retraining |
| cscr2025 | CSCR: Cost-Aware Contrastive Routing for LLMs | 2025 | NeurIPS | [arXiv:2508.12491](https://arxiv.org/abs/2508.12491) | I |  |
| radialrouter2025 | RadialRouter | 2025 | EMNLP | [arXiv:2506.03880](https://arxiv.org/abs/2506.03880) | I |  |
| tagrouter2025 | TagRouter | 2025 | ACL Findings | aclanthology:2025.findings-acl.1110 | I | Tag-based training-free routing for open-domain generation |
| specialists2025 | Talk to Right Specialists: Routing and Planning in Multi-agent System | 2025 | arXiv | [arXiv:2501.07813](https://arxiv.org/abs/2501.07813) | I |  |
| avengers2025 | The Avengers: A Simple Recipe for Uniting Smaller LMs | 2025 | AAAI | [arXiv:2505.19797](https://arxiv.org/abs/2505.19797) | I | Cluster-based routing + ensembling of small open models rivaling GPT-4-class |
| superagent2025 | Toward Super Agent System with Hybrid AI Routers | 2025 | arXiv | [arXiv:2504.10519](https://arxiv.org/abs/2504.10519) | I |  |
| brick2026 | Brick: Spatial Capability Routing for Mixture-of-Models | 2026 | arXiv | [arXiv:2606.13241](https://arxiv.org/abs/2606.13241) | I |  |
| detectrouter2026 | DetectRouter: Prototype-Based Routing for Zero-shot Text Detection | 2026 | ICML | [arXiv:2602.01240](https://arxiv.org/abs/2602.01240) | I |  |
| genrouting2026 | Routing with Generated Data | 2026 | arXiv | [arXiv:2601.09692](https://arxiv.org/abs/2601.09692) | I | Synthetic data for router training |
| tcandon2026 | TCAndon-Router | 2026 | arXiv | [arXiv:2601.04544](https://arxiv.org/abs/2601.04544) | I |  |
| nmusketeers2026 | n-Musketeers | 2026 | arXiv | [arXiv:2602.09173](https://arxiv.org/abs/2602.09173) | I |  |
| vllmsr2026 | vLLM Semantic Router (paper) | 2026 | arXiv | [arXiv:2603.04444](https://arxiv.org/abs/2603.04444) | V | Signal-driven router deployed as Envoy ext_proc; see systems note |

## Pre-generation routers: retrieval, kNN and graph memory (15)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| shnitzer2023benchmark | Large Language Model Routing with Benchmark Datasets | 2023 | COLM | [arXiv:2309.15789](https://arxiv.org/abs/2309.15789) | K | Learn routers from existing benchmark results; kNN-style correctness predictors |
| zhao2024eagle | Eagle: Efficient Training-Free Router for Multi-LLM Inference | 2024 | NeurIPS WS | [arXiv:2409.15518](https://arxiv.org/abs/2409.15518) | I | Global + local ELO from feedback; fast updates |
| feng2024graphrouter | GraphRouter: A Graph-based Router for LLM Selections | 2024 | ICLR 2025 | [arXiv:2410.03834](https://arxiv.org/abs/2410.03834) | K | Heterogeneous task-query-LLM graph; edge prediction; generalizes to new LLMs |
| smoothie2024 | Smoothie: Label Free Language Model Routing | 2024 | NeurIPS |  | K | Weak-supervision (embedding agreement) to route with no labels |
| port2025 | PORT | 2025 | NeurIPS WS | [arXiv:2509.02718](https://arxiv.org/abs/2509.02718) | I |  |
| proxrouter2025 | ProxRouter | 2025 | arXiv | [arXiv:2510.09852](https://arxiv.org/abs/2510.09852) | I |  |
| rar2025 | RAR: Real-Time Adapting Routing | 2025 | ICSE-SEIP | ieee:11121685 | I |  |
| li2025knn | Rethinking Predictive Modeling for LLM Routing: When Simple kNN Beats Complex Learned Routers | 2025 | arXiv | [arXiv:2505.12601](https://arxiv.org/abs/2505.12601) | V | Well-tuned kNN matches/beats learned routers; ~0.3ms/query |
| seqmmr2025 | SeqMMR | 2025 | ACL Findings | aclanthology:2025.findings-acl.870 | I |  |
| acrouter2026 | ACRouter: Agent-as-a-Router | 2026 | arXiv | [arXiv:2606.22902](https://arxiv.org/abs/2606.22902) | I |  |
| contextualrouter2026 | ContextualRouter (retrieval + attention reweighting) | 2026 | EACL SRW | aclanthology:2026.eacl-srw.22 | V | Generalizes with 1% history; plain kNN averaging about as good |
| evoroute2026 | EvoRoute | 2026 | arXiv | [arXiv:2601.02695](https://arxiv.org/abs/2601.02695) | I |  |
| scope2026 | Models Under SCOPE | 2026 | ICML | [arXiv:2601.22323](https://arxiv.org/abs/2601.22323) | I |  |
| routeprofile2026 | RouteProfile: graph-based profiling for cold-start routing | 2026 | arXiv | [arXiv:2605.00180](https://arxiv.org/abs/2605.00180) | V | New models lack interaction data; graph profiling |
| vdar2026 | VDAR-Router | 2026 | arXiv | [arXiv:2607.18098](https://arxiv.org/abs/2607.18098) | I |  |

## Constrained, budgeted and online (bandit) routing (24)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| sakota2023forc | Fly-swat or Cannon? Cost-Effective Language Model Choice via Meta-Modeling (FORC) | 2023 | WSDM 2024 | [arXiv:2308.06077](https://arxiv.org/abs/2308.06077) | I | Meta-model predicts per-model performance then solves assignment under budget |
| metallm2024 | MetaLLM: A High-performant and Cost-efficient Dynamic Framework for Wrapping LLMs | 2024 | arXiv | [arXiv:2407.10834](https://arxiv.org/abs/2407.10834) | I | Multi-armed bandit formulation |
| optllm2024 | OptLLM: Optimal Assignment of Queries to LLMs | 2024 | ICWS | [arXiv:2405.15130](https://arxiv.org/abs/2405.15130) | I | Multi-objective assignment |
| mohammadshahi2024routoo | Routoo: Learning to Route to LLMs Effectively | 2024 | arXiv | [arXiv:2401.13979](https://arxiv.org/abs/2401.13979) | I |  |
| panda2025pilot | Adaptive LLM Routing under Budget Constraints (PILOT) | 2025 | EMNLP Findings | [arXiv:2508.21141](https://arxiv.org/abs/2508.21141) | V | Preference-prior LinUCB (PILOT) + online multi-choice-knapsack budget policy; ~93% of GPT-4 at 25% cost (secondary summary) |
| beyondgpt5_2025 | Beyond GPT-5: Making LLMs Cheaper and Better via Performance-Efficiency Optimized Routing (Avengers-Pro) | 2025 | DAI | [arXiv:2508.12631](https://arxiv.org/abs/2508.12631) | I |  |
| somerstep2025carrot | CARROT: A Cost Aware Rate Optimal Router | 2025 | ICLR WS | [arXiv:2502.03261](https://arxiv.org/abs/2502.03261) | V | Minimax analysis: predicting cost+accuracy per query is rate-optimal; SPROUT dataset (~44K queries, priced models); top-3 on RouterArena initial board |
| tsiourvas2025causal | Causal LLM Routing: End-to-End Regret Minimization from Observational Data | 2025 | NeurIPS | [arXiv:2505.16037](https://arxiv.org/abs/2505.16037) | V | Tsiourvas/Sun/Perakis (MIT, IBM); learns from logs where only deployed model observed; surrogate regret losses; interval-conditioned cost preferences |
| ipr2025 | IPR: Intelligent Prompt Routing with User-Controlled Quality-Cost Trade-offs | 2025 | EMNLP Industry | aclanthology:2025.emnlp-industry.170 | I |  |
| llmrank2025 | LLMRank | 2025 | arXiv | [arXiv:2510.01234](https://arxiv.org/abs/2510.01234) | I |  |
| barp2025 | Learning to Route LLMs from Bandit Feedback: One Policy, Many Trade-offs (BaRP) | 2025 | arXiv | [arXiv:2510.07429](https://arxiv.org/abs/2510.07429) | V | Trains router under bandit feedback (only chosen model observed); preference-conditioned trade-offs |
| wang2025mixllm | MixLLM: Dynamic Routing in Mixed Large Language Models | 2025 | NAACL | [arXiv:2502.18482](https://arxiv.org/abs/2502.18482) | V | Contextual bandit; quality+cost predictors + meta-decision maker incl. latency; 97.25% of GPT-4 quality at 24.18% cost under time constraint |
| streaming2025 | Near-Optimal Online Deployment and Routing for Streaming LLMs | 2025 | ICLR 2026 | [arXiv:2506.17254](https://arxiv.org/abs/2506.17254) | I | Online model deployment + routing as models stream in |
| omnirouter2025 | OmniRouter: Budget and Performance Controllable Multi-LLM Routing | 2025 | KDD | [arXiv:2502.20576](https://arxiv.org/abs/2502.20576) | I | Constrained optimization with global budget |
| sparellm2025 | SpareLLM | 2025 | SIGMOD | doi:10.1145/3725356 | I |  |
| generalized2025 | Towards Generalized Routing: Model and Agent Orchestration | 2025 | arXiv | [arXiv:2509.07571](https://arxiv.org/abs/2509.07571) | I |  |
| boute2026 | BOUTE | 2026 | arXiv | [arXiv:2602.10729](https://arxiv.org/abs/2602.10729) | I |  |
| bicsrouter2026 | BiCSRouter | 2026 | ACL Findings | aclanthology:2026.findings-acl.947 | I |  |
| tryageaco2026 | Efficient and Interpretable Multi-Agent LLM Routing via Ant Colony Optimization | 2026 | arXiv | [arXiv:2603.12933](https://arxiv.org/abs/2603.12933) | I |  |
| flexrouter2026 | FlexRouter: Learning Complementary Model Sets for Flexible LLM Routing | 2026 | COLM | [link](https://research.adobe.com/publication/flexrouter-learning-complementary-model-sets-for-flexible-llm-routing/) | V | DPP subset selection balancing competence and redundancy; maximizes P(at least one correct); adaptive set size |
| hydra2026 | HyDRA | 2026 | arXiv | [arXiv:2605.17106](https://arxiv.org/abs/2605.17106) | I |  |
| oats2026 | OATS | 2026 | arXiv | [arXiv:2603.13426](https://arxiv.org/abs/2603.13426) | I |  |
| r2router2026 | R2-ROUTER | 2026 | ICML | [arXiv:2602.02823](https://arxiv.org/abs/2602.02823) | I |  |
| seqroute2026 | SeqRoute | 2026 | arXiv | [arXiv:2605.25424](https://arxiv.org/abs/2605.25424) | V | Multi-turn routing as finite-horizon MDP, offline RL under global budget |

## Cascades, deferral and self-assessment (17)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| madaan2023automix | AutoMix: Automatically Mixing Language Models | 2023 | NeurIPS 2024 | [arXiv:2310.12963](https://arxiv.org/abs/2310.12963) | K | Few-shot self-verification + POMDP meta-verifier to decide escalation |
| chen2023frugalgpt | FrugalGPT: How to Use LLMs While Reducing Cost and Improving Performance | 2023 | TMLR | [arXiv:2305.05176](https://arxiv.org/abs/2305.05176) | K | Canonical LLM cascade with learned scorer; prompt adaptation + approximation + cascade |
| yue2023mot | Large Language Model Cascades with Mixture of Thought Representations for Cost-Efficient Reasoning | 2023 | ICLR 2024 | [arXiv:2310.03094](https://arxiv.org/abs/2310.03094) | K | Answer consistency across CoT/PoT samples as escalation signal |
| ramirez2024cachedistil | Cache & Distil: Optimising API Calls to LLMs | 2024 | ACL Findings | aclanthology:2024.findings-acl.704 | I | Online student distillation decides when to call the teacher API |
| narasimhan2024fastcascade | Faster Cascades via Speculative Decoding | 2024 | ICLR 2025 | [arXiv:2405.19261](https://arxiv.org/abs/2405.19261) | K | Combines cascade deferral rules with speculative execution |
| gupta2024cascade | Language Model Cascades: Token-Level Uncertainty and Beyond | 2024 | ICLR | [arXiv:2404.10136](https://arxiv.org/abs/2404.10136) | K | Learned deferral using token-level uncertainty quantiles |
| chuang2024selfref | Learning to Route LLMs with Confidence Tokens (Self-REF) | 2024 | ICML 2025 | [arXiv:2410.13284](https://arxiv.org/abs/2410.13284) | I | Fine-tune model to emit confidence tokens used for routing/rejection |
| ramirez2024twotier | Optimising Calls to LLMs with Uncertainty-Based Two-Tier Selection | 2024 | COLM | [arXiv:2405.02134](https://arxiv.org/abs/2405.02134) | I | Small model uncertainty alone is a strong routing/cascade signal |
| su2025cprouter | CP-Router: An Uncertainty-Aware Router Between LLM and LRM | 2025 | AAAI 2026 | [arXiv:2505.19970](https://arxiv.org/abs/2505.19970) | V | Training-free; CP prediction-set size on LLM logits decides LLM vs LRM; FBE picks error rate; needs LLM forward pass first; marginal coverage only |
| chen2025confident | Confident or Seek Stronger: Exploring Uncertainty-Based On-Device LLM Routing | 2025 | NeurIPS 2025 WS | [arXiv:2502.04428](https://arxiv.org/abs/2502.04428) | I | On-device to cloud escalation with uncertainty |
| diSRouter2025 | DiSRouter: Distributed Self-Routing for LLM Selections | 2025 | ICLR 2026 | [arXiv:2510.19208](https://arxiv.org/abs/2510.19208) | V | No central router: each LLM self-assesses (two-stage self-awareness training) and answers or passes on; generalizes OOD and to pool changes |
| sater2025 | SATER: Self-Aware and Token-Efficient Approach to Routing and Cascading | 2025 | EMNLP | aclanthology:2025.emnlp-main.531 | I | Trains small model to refuse when unsure; reduces cascade waste |
| acar2026 | ACAR (adaptive cascade routing) | 2026 | arXiv | [arXiv:2602.21231](https://arxiv.org/abs/2602.21231) | I |  |
| r2vagent2026 | R2V Agent | 2026 | arXiv | [arXiv:2605.16604](https://arxiv.org/abs/2605.16604) | I |  |
| raser2026 | RASER | 2026 | arXiv | [arXiv:2606.02488](https://arxiv.org/abs/2606.02488) | I |  |
| ror2026 | Resample or Reroute (RoR) | 2026 | arXiv | [arXiv:2607.08665](https://arxiv.org/abs/2607.08665) | I | When to resample same model vs reroute to another |
| xrouter2026acl | X-Router | 2026 | ACL Findings | aclanthology:2026.findings-acl.994 | I |  |

## Reasoning-effort and test-time-compute routing (6)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| difficulty2025 | Optimizing Reasoning Efficiency through Prompt Difficulty Prediction | 2025 | arXiv | [arXiv:2511.03808](https://arxiv.org/abs/2511.03808) | I |  |
| radar2025 | RADAR: Reasoning-Ability and Difficulty-Aware Routing | 2025 | NeurIPS WS | [arXiv:2509.25426](https://arxiv.org/abs/2509.25426) | I | IRT-style routing over (model x reasoning budget) configurations |
| pan2025rtr | Route to Reason: Adaptive Routing for LLM and Reasoning Strategy Selection | 2025 | arXiv | [arXiv:2505.19435](https://arxiv.org/abs/2505.19435) | V | Jointly routes (model, reasoning strategy) under budget; >60% token cut with higher accuracy than best single model |
| routereason2025 | Route-and-Reason: Scaling LLM Reasoning with Reinforced Model Router | 2025 | arXiv | [arXiv:2506.05901](https://arxiv.org/abs/2506.05901) | I |  |
| dart2026 | DART: Draft-Agreement Routing for Training-Free Adaptive Thinking Budgets | 2026 | arXiv | [arXiv:2606.23181](https://arxiv.org/abs/2606.23181) | V | Two cheap no-think drafts; agreement -> answer; else thinking budget from entropy |
| thinkwhenneeded2026 | Think When Needed: Model-Aware Reasoning Routing | 2026 | arXiv (SIGIR 2026) | [arXiv:2601.18146](https://arxiv.org/abs/2601.18146) | V | Per-instance decide whether an LLM should reason |

## Multi-round, token-level, agentic and fusion routing (25)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| jiang2023blender | LLM-Blender: Ensembling LLMs with Pairwise Ranking and Generative Fusion | 2023 | ACL | [arXiv:2306.02561](https://arxiv.org/abs/2306.02561) | K | Generate-all then rank+fuse; upper-bound style ensemble (expensive) |
| shen2024coll | Learning to Decode Collaboratively with Multiple Language Models (Co-LLM) | 2024 | ACL | [arXiv:2403.03870](https://arxiv.org/abs/2403.03870) | K | Latent variable decides which model emits each token |
| wang2024moa | Mixture-of-Agents Enhances Large Language Model Capabilities | 2024 | ICLR 2025 | [arXiv:2406.04692](https://arxiv.org/abs/2406.04692) | K | Layered multi-LLM aggregation; quality not cost focus |
| zheng2025citer | CITER: Collaborative Inference for Efficient LLM Decoding with Token-Level Routing | 2025 | arXiv (NeurIPS 2024 WS) | [arXiv:2502.01976](https://arxiv.org/abs/2502.01976) | V | RL-trained token router between SLM and LLM |
| centralmas2025 | Controlling Performance and Budget of a Centralized Multi-Agent LLM System | 2025 | arXiv | [arXiv:2511.02755](https://arxiv.org/abs/2511.02755) | I |  |
| feng2025swarms | Heterogeneous Swarms: Jointly Optimizing Model Roles and Weights for Multi-LLM Systems | 2025 | NeurIPS | [arXiv:2502.04510](https://arxiv.org/abs/2502.04510) | I |  |
| lightrouter2025 | LightRouter | 2025 | arXiv | [arXiv:2505.16221](https://arxiv.org/abs/2505.16221) | I |  |
| masrouter2025 | MasRouter: Learning to Route LLMs for Multi-Agent Systems | 2025 | ACL | [arXiv:2502.11133](https://arxiv.org/abs/2502.11133) | V | Cascaded controller: collaboration mode -> roles -> LLM per role; up to 52% cost cut on HumanEval; 17-28% when plugged into MAS frameworks |
| mot2025 | Mixture of Thoughts: Learning to Aggregate What Experts Think | 2025 | ICLR 2026 | [arXiv:2509.21164](https://arxiv.org/abs/2509.21164) | I | Latent-level collaboration among experts |
| fu2025r2r | R2R: Efficiently Navigating Divergent Reasoning Paths with Small-Large Model Token Routing | 2025 | NeurIPS | [arXiv:2505.21600](https://arxiv.org/abs/2505.21600) | K | Route only path-divergent tokens to the large reasoning model |
| rema2025 | ReMA: Learning to Meta-think for LLMs with Multi-agent RL | 2025 | NeurIPS | [arXiv:2503.09501](https://arxiv.org/abs/2503.09501) | I |  |
| zhang2025routerr1 | Router-R1: Teaching LLMs Multi-Round Routing and Aggregation via RL | 2025 | NeurIPS | [arXiv:2506.09033](https://arxiv.org/abs/2506.09033) | V | LLM router interleaves think/route; format+outcome+cost rewards; conditions on model descriptors |
| xrouter2025 | xRouter: Training Cost-Aware LLMs Orchestration System via Reinforcement Learning | 2025 | arXiv | [arXiv:2510.08439](https://arxiv.org/abs/2510.08439) | V | Salesforce; RL-trained router answers or calls 20+ models as tools; cost-penalized reward; small open models struggle to learn orchestration; CC-BY-NC weights |
| agentrouter2026icml | AgentRouter: Heterogeneous Model Routing for Cost-Optimal Multi-Step Agentic Workflows | 2026 | ICML WS (AdaptFM) | [link](https://icml.cc/virtual/2026/68040) | V | 12M classifier per step; reported 72% cost cut <3% task drop vs frontier-only |
| agenticrouting2026 | Agentic Routing: The Harness-Native Data Flywheel | 2026 | arXiv | [arXiv:2607.11399](https://arxiv.org/abs/2607.11399) | V | Step-level routing from harness state; routing logs become training data |
| atlas2026 | Atlas | 2026 | arXiv | [arXiv:2601.03872](https://arxiv.org/abs/2601.03872) | I |  |
| budgetagentic2026 | Budget-Aware Agentic Routing via Boundary-Guided Training | 2026 | arXiv | [arXiv:2602.21227](https://arxiv.org/abs/2602.21227) | I |  |
| budgetmem2026 | BudgetMem | 2026 | ICML | [arXiv:2602.06025](https://arxiv.org/abs/2602.06025) | I |  |
| fusionroute2026 | FusionRoute | 2026 | ICML | [arXiv:2601.05106](https://arxiv.org/abs/2601.05106) | I | Token-level routing + fusion |
| ncots2026 | NCoTs: Neural Chain-of-Thought Search | 2026 | arXiv | [arXiv:2601.11340](https://arxiv.org/abs/2601.11340) | I |  |
| relayllm2026 | RelayLLM | 2026 | arXiv | [arXiv:2601.05167](https://arxiv.org/abs/2601.05167) | I |  |
| scmas2026 | SC-MAS | 2026 | arXiv | [arXiv:2601.09434](https://arxiv.org/abs/2601.09434) | I |  |
| steer2026 | STEER: Confidence-Guided Stepwise Model Routing | 2026 | AAAI | [link](https://github.com/helmsman12/STEER) | I | Step-level routing within a reasoning chain |
| skillorch2026 | SkillOrchestra | 2026 | arXiv | [arXiv:2602.19672](https://arxiv.org/abs/2602.19672) | I |  |
| taro2026 | TARo | 2026 | arXiv | [arXiv:2603.18411](https://arxiv.org/abs/2603.18411) | I |  |

## Personalized and preference-aligned routing (5)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| gmtrouter2025 | GMTRouter: Personalized LLM Router over Multi-turn User Interactions | 2025 | arXiv | [arXiv:2511.08590](https://arxiv.org/abs/2511.08590) | V | Heterogeneous user-LLM-query-response graph |
| dai2025personalized | PersonalizedRouter: Personalized LLM Routing via Graph-based User Preference Modeling | 2025 | TMLR | [arXiv:2511.16883](https://arxiv.org/abs/2511.16883) | V | PersonaRoute-Bench (1000 users) |
| zhang2026dialrouter | From Myopic Selection to Long-Horizon Awareness: Sequential LLM Routing for Multi-Turn Dialogue (DialRouter) | 2026 | arXiv | [arXiv:2604.12385](https://arxiv.org/abs/2604.12385) | V | MCTS over dialogue branches -> distilled lightweight policy; cost-aware reward; beats single LLMs and per-turn routers |
| mtrouter2026 | MTRouter: Cost-Aware Multi-Turn LLM Routing with History-Model Joint Embeddings | 2026 | arXiv | [arXiv:2604.23530](https://arxiv.org/abs/2604.23530) | V | Joint history-model embeddings; notes switching breaks prompt caching |
| swrouter2026 | SWRouter: Similarity-Contractive Window Routing for Multi-Turn LLM Conversations | 2026 | arXiv | [arXiv:2609.11414](https://arxiv.org/abs/2609.11414) | I |  |

## Multimodal routing (5)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| costt2i2025 | Cost-Aware Routing for Efficient Text-To-Image Generation | 2025 | arXiv | [arXiv:2506.14753](https://arxiv.org/abs/2506.14753) | I |  |
| routet2i2025 | RouteT2I: Adaptive Routing of Text-to-Image Requests | 2025 | ICCV |  | I |  |
| vlrouterbench2025 | VL-RouterBench | 2025 | CVPR 2026 | [arXiv:2512.23562](https://arxiv.org/abs/2512.23562) | V | 14 datasets 30.5K samples 17 VLMs (519K pairs); 10 routers; big gain from routing but far from oracle; single-image only |
| mmrbench2026 | MMR-Bench (multimodal routing) | 2026 | arXiv | [arXiv:2601.17814](https://arxiv.org/abs/2601.17814) | I |  |
| relope2026 | ReLope: KL-Regularized LoRA Probes for Multimodal LLM Routing | 2026 | arXiv | [arXiv:2603.24787](https://arxiv.org/abs/2603.24787) | V | Probe-based routing degrades on image queries; LoRA probes to fix |

## Multilingual and other coverage (1)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| nofits2026 | No One Fits All: From Fixed Prompting to Learned Routing in Multilingual LLMs | 2026 | ACL Findings | [arXiv:2604.16937](https://arxiv.org/abs/2604.16937) | V | Routes prompting strategy (native vs translate) per instance, not models; translation helps low-resource languages |

## Serving systems, edge and energy (11)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| cloudedge2025 | Efficient Routing of Inference Requests across LLM Instances in Cloud-Edge Computing | 2025 | arXiv | [arXiv:2507.15553](https://arxiv.org/abs/2507.15553) | I |  |
| ipw2025 | Intelligence per Watt | 2025 | arXiv | [arXiv:2511.07885](https://arxiv.org/abs/2511.07885) | V | Stanford; IPW=accuracy/power; local models answer 88.7% of queries; oracle local/cloud routing cuts energy 80%, cost 74%; 80%-accurate router captures 80% of gains |
| netgpt2025 | Optimizing NetGPT via Routing-Based Synergy and RL | 2025 | arXiv | [arXiv:2511.22217](https://arxiv.org/abs/2511.22217) | I |  |
| federate2026 | Federate the Router: Learning Language Model Routers with Sparse and Decentralized Evaluations | 2026 | arXiv | [arXiv:2601.22318](https://arxiv.org/abs/2601.22318) | V | CMU; federated MLP and k-means routers beat any single-client router; suboptimality theory |
| greenserv2026 | GreenServ | 2026 | arXiv | [arXiv:2601.17551](https://arxiv.org/abs/2601.17551) | I | Energy-aware routing |
| hwrouter2026 | HW-Router: Hardware-Aware Routing for Scalable Multi-LLM Serving | 2026 | arXiv | [arXiv:2608.14575](https://arxiv.org/abs/2608.14575) | V | 3.4-3.9x lower e2e latency under overload vs static routing |
| lqm2026 | LQM-CONTEXTROUTE: Latency-Quality Routing for Tools | 2026 | arXiv | [arXiv:2605.14241](https://arxiv.org/abs/2605.14241) | I |  |
| lodestar2026 | Lodestar: learning-based request router for GPU clusters | 2026 | arXiv | [arXiv:2606.00946](https://arxiv.org/abs/2606.00946) | V | Instance-level (same model) request routing; batching/KV-reuse aware |
| proteus2026 | PROTEUS: SLA-Aware Routing via Lagrangian RL for Multi-LLM Serving Systems | 2026 | arXiv | [arXiv:2601.19402](https://arxiv.org/abs/2601.19402) | V | Constrained RL (Lagrangian) for SLA-aware routing |
| robatch2026 | RoBatch: Towards Cost-effective LLMs Routing with Batch Prompting | 2026 | arXiv | [arXiv:2605.28268](https://arxiv.org/abs/2605.28268) | I | Routing aware of batch prompting economics |
| routerwise2026 | RouterWise: Joint Resource Allocation and Routing for Latency-Aware Multi-Model LLM Serving | 2026 | arXiv | [arXiv:2604.10907](https://arxiv.org/abs/2604.10907) | V | FrugalGPT cascade overloads cheapest model queue; joint placement+routing meets TTFT SLO |

## Benchmarks, evaluation platforms and libraries (14)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| modelglue2024 | Model-GLUE: Democratized LLM Scaling for A Large Model Zoo in the Wild | 2024 | NeurIPS | [arXiv:2410.05357](https://arxiv.org/abs/2410.05357) | I | Compares merging / mixture / stacking / routing for model zoos |
| hu2024routerbench | RouterBench: A Benchmark for Multi-LLM Routing System | 2024 | ICML WS | [arXiv:2403.12031](https://arxiv.org/abs/2403.12031) | V | 405K pre-generated outcomes; cost-quality frontier (AIQ); Martian |
| medrec2025 | Multi-LLM Collaboration for Medication Recommendation | 2025 | arXiv | [arXiv:2512.05066](https://arxiv.org/abs/2512.05066) | I |  |
| lu2025routerarena | RouterArena: An Open Platform for Comprehensive Comparison of LLM Routers | 2025 | ICLR 2026 | [arXiv:2510.00202](https://arxiv.org/abs/2510.00202) | V | Live leaderboard incl. commercial routers (Azure GPT-5 router) at routeworks.github.io |
| huang2025routereval | RouterEval: A Comprehensive Benchmark for Routing LLMs to Explore Model-level Scaling Up | 2025 | EMNLP Findings | [arXiv:2503.10657](https://arxiv.org/abs/2503.10657) | V | 200M+ records 8500+ LLMs 12 evals; model-level scaling-up with candidate count |
| yuan2025whoroutes | Who Routes the Router? Rethinking the Evaluation of LLM Routing Systems | 2025 | NeurIPS WS | openreview:EEPostHMtF | I |  |
| agentselect2026 | AgentSelect | 2026 | arXiv | [arXiv:2603.03761](https://arxiv.org/abs/2603.03761) | I |  |
| amongus2026 | AmongUs (agent deception benchmark used for routing) | 2026 | ICML | [arXiv:2602.05176](https://arxiv.org/abs/2602.05176) | I |  |
| llmrouterlib2026 | LLMRouter: Unified Infrastructure for Developing Evaluating and Deploying LLM Routers (+ xRouteBench) | 2026 | arXiv | [arXiv:2608.06867](https://arxiv.org/abs/2608.06867) | V | 16+ routers in one library; 5 scenarios incl. long-context memory vision time-series personalization; +14.6% rel. over best fixed model; no single winner |
| li2026llmrouterbench | LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing | 2026 | ACL Findings | [arXiv:2601.07206](https://arxiv.org/abs/2601.07206) | V | 400K instances 21 datasets 33 models 10 baselines; many routers incl. commercial fail to beat simple baseline; model-recall failures |
| routejudge2026 | RouteJudge & ORBIT | 2026 | arXiv | [arXiv:2606.18774](https://arxiv.org/abs/2606.18774) | I | LLM-judge based router evaluation |
| routerxbench2026 | RouterXBench | 2026 | arXiv | [arXiv:2602.11877](https://arxiv.org/abs/2602.11877) | I |  |
| gonuguntla2026replay | The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World | 2026 | arXiv | [arXiv:2608.08239](https://arxiv.org/abs/2608.08239) | V | Live forked re-execution on SWE-bench Verified: swaps change 61-94% of later actions; log-stitching replay mispredicts every success-relevant outcome; thoroughness tax |
| twinrouterbench2026 | TwinRouterBench | 2026 | CAIS WS | [arXiv:2605.18859](https://arxiv.org/abs/2605.18859) | I |  |

## Theory and critical analyses (15)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| dekoninck2024unified | A Unified Approach to Routing and Cascading for LLMs (cascade routing) | 2024 | ICML 2025 | [arXiv:2410.10347](https://arxiv.org/abs/2410.10347) | V | Proves optimal routing + new optimal cascade; quality estimators are the critical factor |
| pricellm2025 | PriLLM: Stackelberg routing game | 2025 | AAAI | [arXiv:2511.09062](https://arxiv.org/abs/2511.09062) | I |  |
| routesplain2025 | ROUTESPLAIN: Faithful and Intervenable Routing | 2025 | arXiv | [arXiv:2511.09373](https://arxiv.org/abs/2511.09373) | I | Explainable routing via concepts |
| feng2025onellm | When One LLM Drools Multi-LLM Collaboration Rules | 2025 | arXiv | [arXiv:2502.04506](https://arxiv.org/abs/2502.04506) | I | Position paper on multi-LLM collaboration incl. routing |
| conformal2026 | Conformal LLM Routing with Distribution-Free Safety Guarantees | 2026 | ACL SRW | aclanthology:2026.acl-srw.70 | I |  |
| chen2026gapreal | How Much of the Routing Gap Is Real? Decomposing the Router-to-Oracle Gap | 2026 | arXiv | [arXiv:2607.03436](https://arxiv.org/abs/2607.03436) | V | 12-36% of router-oracle gap is single-draw label noise; multi-sample oracle protocol |
| bae2026retrials | Learning to Route and Schedule LLMs from User Retrials via Contextual Queueing Bandits | 2026 | arXiv | [arXiv:2602.02061](https://arxiv.org/abs/2602.02061) | V | Implicit feedback (retrials) + scheduling jointly |
| lee2026tasktype | Most of the LLM Routing Gap Is Task Type | 2026 | arXiv | [arXiv:2608.23023](https://arxiv.org/abs/2608.23023) | V | Asks what the residual gap is made of; hardest 11-35% queries carry 70-91% of gap (cited prior work) |
| fisch2026pandora | Pandora's AI Model Routing Box: Efficient Allocation with Costly Value Estimation | 2026 | NeurIPS | [arXiv:2608.20316](https://arxiv.org/abs/2608.20316) | V | Costly value estimation as Pandora box; closed-form VOI decides when to call expensive estimator; matches exhaustive estimation at far fewer expensive calls; decentralized bidder variant |
| hao2026racer | RACER: Risk-Aware Calibrated Efficient Routing for Large Language Models | 2026 | ICML | [arXiv:2603.06616](https://arxiv.org/abs/2603.06616) | V | Set-valued routing with distribution-free misrouting-risk control (alpha-VOR); post-hoc, model-agnostic; needs all base-router scores |
| mahmood2026userchoice | Routing, Cascades, and User Choice for LLMs | 2026 | ICLR | [arXiv:2602.09902](https://arxiv.org/abs/2602.09902) | V | Stackelberg provider-user game; optimal policy usually static w/o cascading; incentive to throttle latency |
| lu2026plateau | The Routing Plateau: Understanding and Breaking the Accuracy Limits of LLM Routers | 2026 | arXiv | [arXiv:2606.07587](https://arxiv.org/abs/2606.07587) | V | 21 methods x 5 benchmarks converge to narrow band; routers learn average trends; suggests using partial trajectories |
| auction2026 | Truthful Reverse Auctions for Adaptive Selection | 2026 | AAMAS | [arXiv:2602.14476](https://arxiv.org/abs/2602.14476) | I | Mechanism design: providers bid; router as auctioneer |
| garg2026unsolvability | Unsolvability Ceiling in Multi-LLM Routing: An Empirical Study of Evaluation Artifacts | 2026 | arXiv | [arXiv:2605.07395](https://arxiv.org/abs/2605.07395) | V | Truncation/judge/format artifacts inflate 'unsolvable'; routers collapse to majority class |
| lai2026equirouter | When Routing Collapses: On the Degenerate Convergence of LLM Routers (EquiRouter) | 2026 | arXiv (NeurIPS 2026 as 'When LLM Routers Overpay') | [arXiv:2602.03478](https://arxiv.org/abs/2602.03478) | V | Routers over-select strongest model as budget grows; fix by learning rankings; ~17% cost cut at GPT-4 level on RouterBench |

## Security and robustness (6)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| cai2025substitution | Are You Getting What You Pay For? Auditing Model Substitution in LLM APIs | 2025 | NeurIPS | [arXiv:2504.04715](https://arxiv.org/abs/2504.04715) | V | Software-only detection (output stats, benchmarks, logprobs) unreliable vs quantization/random substitution; argues for TEE attestation |
| kassem2025robust | How Robust Are Router-LLMs? Analysis of the Fragility of LLM Routing Capabilities (DSC) | 2025 | EACL 2026 | [arXiv:2504.07113](https://arxiv.org/abs/2504.07113) | V | Category-driven routing; jailbreaks routed to weak models; privacy/safety checks |
| shafran2025rerouting | Rerouting LLM Routers | 2025 | COLM | [arXiv:2501.01818](https://arxiv.org/abs/2501.01818) | V | Query-independent confounder gadgets force strong-model routing; 'LLM control plane integrity' |
| r2a2026 | R2A: Route to Rome Attack | 2026 | ACL | [arXiv:2604.15022](https://arxiv.org/abs/2604.15022) | I |  |
| rerouteguard2026 | RerouteGuard: Understanding and Mitigating Adversarial Risks for LLM Routing | 2026 | arXiv | [arXiv:2601.21380](https://arxiv.org/abs/2601.21380) | V | Real routing systems vulnerable (cost escalation); embedding-based detector >99% |
| youragent2026 | Your Agent Is Mine: Measuring Malicious Intermediary Attacks on the LLM Supply Chain | 2026 | ACM CCS | [arXiv:2604.08407](https://arxiv.org/abs/2604.08407) | V | Measured 28 paid + 400 free API routers: 9 injected malicious code, 17 touched planted credentials; defenses: fail-closed gating, anomaly screening, transparency logs |

## Industry disclosures (1)

| id | Title | Year | Venue | Link | V | Note |
|---|---|---|---|---|---|---|
| openai2025gpt5 | GPT-5 System Card (real-time router across main/thinking models) | 2025 | system card | [link](https://openai.com/index/gpt-5-system-card/) | V | Router trained on model switches / preference / correctness signals; user backlash over control |

