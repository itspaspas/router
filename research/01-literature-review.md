---
type: index
title: Literature review — LLM routers 2023–2026
---
# LLM routers: a literature review (2023 – Oct 2026)

> The big picture in one paragraph. LLM routing grew out of a simple economic fact: model prices span two to three orders of magnitude while most queries are easy. The field moved through four phases: **cascades** (2023), **learned query routers and benchmarks** (2024), **generalization, RL and new action spaces** (2025), and then **a critical turn** (2026). In that last phase, large benchmarks showed that most routers, commercial ones included, barely beat simple baselines such as kNN. It also showed that much of the advertised "oracle headroom" is label noise, evaluation artifacts, or coarse task-type structure. At the same time the action space exploded: reasoning effort, samples, steps in agent loops, tokens, sessions and serving replicas. The frontier is now about *information* (what the router gets to observe), *honest evaluation*, *non-stationarity*, *agents*, *systems coupling* and *trust*. See [[05-gaps-and-agenda]].

Navigation: concepts hub [[llm-routing]] · taxonomy [[03-taxonomy]] · timeline [[02-timeline]] · systems [[04-projects-landscape]] · full bibliography `sources/catalog.md`.

---

## 1. Problem statement

Given a pool M = {m₁,…,m_k} with per-call costs c_j(x) and latencies, and an input x, a router chooses an action a ∈ A to maximize expected utility

  U(x, a) = E[q(x, a)] − λ·cost(x, a), subject to budget, latency, safety or privacy constraints.

The literature differs in what A is (one model; a sequence of models; model × effort × samples; per-token choices), in what the policy observes (the query only; partial or complete outputs; internal activations; user and session history; serving state), and in how q is supervised (benchmark correctness, pairwise preference, reward models, LLM judges, implicit feedback). See [[design-space]].

The **oracle router**, which picks the cheapest correct model for every query, is the yardstick. On static benchmarks it beats the best single model by a wide margin. For example, LLMRouterBench reports roughly 92% oracle accuracy against roughly 70–72% for top routers ([[llmrouterbench]]). That headroom motivates the field and is also its most contested number ([[oracle-gap]]).

## 2. Intellectual precursors
- **Mixture-of-Experts gating** (Shazeer 2017; Switch 2021) routes *inside* one network and is trained jointly. LLM routing routes *between* independently trained, often closed models ([[routing-vs-moe]]).
- **Ensembles and fusion**: LLM-Blender (pairwise ranking plus generative fusion, 2023) and Mixture-of-Agents (2024) query every model and then combine. They have high ceilings and high cost, and they set the "use everything" upper bound ([[collaborative-routing]]).
- **Speculative decoding** (2023) is lossless small-to-large collaboration at token level, the systems ancestor of [[token-level-routing]].
- **Learning to defer / selective prediction / algorithm selection** supplies the classic ML framing for [[cascades]] and per-instance model selection.

## 3. Phase I (2023): cascades and first routers
- **FrugalGPT** ([[frugalgpt]]) made the cost–quality framing canonical. It is an API cascade with a learned answer scorer, with large reported savings at GPT-4 quality.
- **AutoMix** ([[automix]]) replaced the trained scorer with *self-verification* plus a POMDP meta-verifier.
- **Mixture-of-thought cascades** (Yue et al.) used answer consistency across CoT and PoT samples as the escalation signal.
- **First query routers**: Tryage (predict per-model loss), Shnitzer et al. (learn routers from existing benchmark results, kNN-like), FORC (meta-model plus budgeted assignment), and **Zooter** ([[zooter]], which distils reward-model scores into a router).
- Lesson of the phase: *seeing the answer* (cascades) gives strong signals, but every query pays for the first call.

## 4. Phase II (2024): learned routers, preference data, benchmarks
- **Binary strong/weak routing**: Hybrid LLM ([[hybrid-llm]]) predicted the quality gap with a test-time threshold. **RouteLLM** ([[routellm]]) trained four router types on Chatbot Arena preferences and released a widely used framework, reporting large savings on MT-Bench (>85%) and smaller ones on GSM8K (≈35%).
- **Representation matching**: RouterDC ([[routerdc]], dual contrastive) and EmbedLLM ([[embedllm]], compact model vectors).
- **Graph and memory routers**: GraphRouter ([[graphrouter]], heterogeneous task–query–LLM graph, which handles new LLMs), Eagle (online ELO), Smoothie (label-free).
- **Bandits**: MetaLLM.
- **Better cascade signals**: token-level uncertainty quantiles (Gupta et al.), Self-REF confidence tokens, two-tier uncertainty selection, Cache & Distil.
- **Token-level collaboration**: Co-LLM learns which model emits each token.
- **Benchmarks**: **RouterBench** ([[routerbench]], Martian, 405K pre-generated outcomes and the AIQ metric). Model-GLUE compares routing with merging and mixing.
- **Early warning**: Srivatsa et al. ("Harnessing the Power of Multiple Minds") found routers struggled to beat the best single model on reasoning. In hindsight this foreshadowed the 2026 critique.

## 5. Phase III (2025): scale, generalization, theory, RL, new action spaces
**Scale and generalization.**
- **RouterEval** ([[routereval]]) assembled 200M+ records over 8,500+ LLMs and found *model-level scaling-up* (more candidates help, given a good router).
- **UniRoute** ([[uniroute]]) represents models by their error vectors on a probe set, which handles unseen models.
- **P2L** ([[p2l]]) learns prompt-specific Bradley–Terry leaderboards.
- **IRT-Router** ([[irt-router]]) applies psychometrics to routing.
- **CARROT** ([[carrot]]) gives a rate-optimal cost and accuracy estimator.
- **Capability instruction tuning** (Model-SAT) adds an aptitude-test model representation.

**Theory.** Dekoninck et al. ([[unified-routing-cascading]], ICML 2025) proved the optimal routing and cascading strategies and unified them as *cascade routing*. The key finding was that **quality estimators are the bottleneck**.

**Budgeted and online routing.** MixLLM (a contextual bandit with latency constraints), PILOT (preference-prior bandit plus budget policy), OmniRouter (a global budget), Causal LLM Routing (regret minimization from observational logs), and streaming-model deployment (ICLR 2026). See [[budgeted-online-routing]].

**RL and LLM-as-router.** Router-R1 ([[router-r1]], NeurIPS 2025) is an LLM that interleaves think and route actions over multiple rounds, with a cost reward, and generalizes via model descriptors. xRouter and MasRouter route inside multi-agent systems.

**Preference-aligned routing.** Arch-Router ([[arch-router]]) is a 1.5B model mapping queries to operator-written `(domain, action)` policies, so new models are added by editing the table. PersonalizedRouter ([[personalizedrouter]]) and GMTRouter model individual users with graphs ([[personalized-routing]]).

**New action spaces.**
- *Test-time compute*: BEST-Route ([[best-route]]) routes over model × best-of-n. CP-Router uses conformal sets to choose between an LLM and a reasoning model. RADAR treats (model, budget) pairs as IRT respondents. See [[reasoning-effort-routing]].
- *Token level*: CITER ([[citer]], an RL token router) and R2R ([[r2r]], which routes only path-divergent tokens).

**Security.** "Rerouting LLM Routers" ([[rerouting-llm-routers]]) showed query-independent *confounder gadgets* that force strong-model routing, and framed the router as a control plane. DSC ([[dsc-robustness]]) found category-driven routing that sends jailbreaks to weaker models.

**The first crack.** "When simple kNN beats complex learned routers" ([[knn-router]]).

**Industry goes mainstream.** OpenAI shipped GPT-5 as a *routed system* ([[gpt5-router]]), and the user backlash showed that routing is a product and trust issue. AWS made Bedrock Intelligent Prompt Routing generally available ([[bedrock-intelligent-prompt-routing]]), Azure shipped Model Router ([[azure-model-router]]), and vLLM Semantic Router ([[vllm-semantic-router]]) and Arch brought routing into open infrastructure.

## 6. Phase IV (2026): the critical turn and the frontier
**Evaluation reckoning** ([[oracle-gap]]):
- **LLMRouterBench** ([[llmrouterbench]]; 400K instances, 33 models, 10 baselines): many routers, *including commercial ones*, fail to reliably beat a simple baseline. The persistent gap comes from model-recall failures. Curation beats pool size.
- **RouterArena** ([[routerarena]]) is a live leaderboard mixing academic and commercial routers, where an IRT-style router edged out Azure's.
- **The Routing Plateau** ([[routing-plateau]]): 21 methods converge to a narrow band. Routers learn average trends, and more data or larger encoders add only about 1 pp.
- **How much of the gap is real?** ([[routing-gap-noise]]): 12–36% of the router-to-oracle gap is single-draw label noise.
- **Unsolvability ceiling** ([[unsolvability-ceiling]]): truncation, judge and format artifacts. Routers collapse to the majority class.
- **Task type** ([[task-type-gap]]): the remaining recoverable gap lines up mostly with task type.
- **Routing collapse** ([[routing-collapse]]): decision-misaligned training over-selects the strongest model. EquiRouter's ranking loss fixes part of it.

**Frontier expansions:**
- *Richer signals*: routing on **prefill activations** ([[prefill-activation-router]]), **pre-generation probes** ([[llms-encode-failures]], ICLR 2026), and **draft agreement** for thinking budgets ([[dart]]). **Pandora's Router** ([[pandora-router]], NeurIPS 2026) decides *when* paying for an expensive value estimate is worth it.
- *Guarantees*: **RACER** ([[racer]], ICML 2026) gives set-valued routing with distribution-free misrouting-risk control.
- *Sessions*: sequential multi-turn routers ([[dialrouter]], SeqRoute, MTRouter).
- *Evaluation of agent routing*: **The Replay Gap** ([[replay-gap]]) shows log-replay evaluation of per-step model switching is unsound.
- *Agents*: per-step routing (AgentRouter, [[agentrouter-agentic]]) and harness-native data flywheels ([[agentic-routing]]).
- *Serving*: joint placement and routing under TTFT SLOs ([[routerwise]]), hardware-aware routing (HW-Router), batch-prompt-aware routing (RoBatch), energy (GreenServ). See [[serving-aware-routing]].
- *Cold start*: ZeroRouter ([[zerorouter]]) and RouteProfile.
- *Economics*: Stackelberg provider–user games ([[user-choice-stackelberg]]), learning from user retrials ([[user-retrials]]), truthful auctions.
- *Security*: RerouteGuard ([[rerouteguard]]), R2A, and malicious intermediaries: of 428 measured API routers, 9 injected code and 17 touched planted credentials. Software-only detection of model substitution is unreliable ([[model-substitution-audit]]).
- *Infrastructure*: the LLMRouter library and xRouteBench ([[llmrouter-library]]) put 16+ routers behind one interface. Its conclusion is that no single router wins everywhere.
- *Surveys*: Moslem & Kelleher's routing-and-cascading survey (Feb 2026), and a unified survey of routing, cascades and test-time scaling as adaptive computation (Jun 2026). The latter finds reported savings often incomparable because router, verifier and queue costs are counted inconsistently.

## 7. What we know with reasonable confidence
1. **Routing pays in practice when the pool is cost-heterogeneous and traffic is easy-skewed.** Most savings come from sending easy queries to cheap models, which simple classifiers already capture.
2. **Query-only routers are saturated.** Architecture choice matters little (plateau, kNN parity, embedding backbone irrelevance).
3. **The reported oracle gap is inflated.** Noise and artifacts make up a large minority, and much of the rest is task-type structure.
4. **Seeing (part of) the output helps.** Cascades, self-verification, draft agreement and activations are stronger signals, at a cost ([[quality-estimation]]).
5. **Training objective matters more than architecture at the decision boundary** (routing collapse; ranking and regret losses).
6. **The action space is bigger than "which model"**: effort, samples, steps and tokens all trade off.
7. **Routers are attack surfaces and economic actors**, not neutral classifiers.

## 8. Live debates
- *Is learned routing worth it over rules plus task classifiers?* Industry practice ([[gateways-and-semantic-router-libs]], [[nvidia-llm-router]]) suggests rules are good enough. Learned routers have not been shown to win on real traffic.
- *Routing vs. one strong reasoning model with adaptive effort.* If frontier models self-route internally (effort knobs), does external routing shrink to cross-provider price arbitrage?
- *Cascade or not?* The theory says cascade routing is optimal given estimators, while the user-choice game says static routing is usually optimal for providers.
- *Bigger pools or curated pools?* RouterEval and LLMRouterBench point in partly opposite directions ([[gap-pool-design]]).

→ Gaps and agenda: [[05-gaps-and-agenda]] · Concrete projects: [[06-research-proposals]]
