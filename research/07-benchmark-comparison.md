---
type: index
title: Benchmark and results comparison
---
# Benchmarks and headline results side by side

All figures come from sources checked this session (flag V in `sources/catalog.csv`). Most are *author-reported*, measured on different pools, prices and metrics, so **numbers in different rows are not comparable with each other**. The 2026 adaptive-computation survey makes the same point: router, verifier and queueing costs are counted inconsistently across papers ([[gap-evaluation-validity]]).

## 1. Router benchmarks

| Benchmark | Year / venue | Scale | Unit routed | Labels | Distinctive finding |
|---|---|---|---|---|---|
| [[routerbench]] | 2024, ICML WS | 405K outcomes, 11 models, 8 datasets | query | single draw | cost–quality plane, AIQ metric |
| [[routereval]] | 2025, EMNLP-F | 200M+ records, 8,500+ LLMs, 12 evals | query | single draw | model-level scaling-up with pool size |
| CARROT's SPROUT ([[carrot]]) | 2025 | ~44K queries, priced frontier models | query | single draw | price-aware routing data |
| [[llmrouterbench]] | 2026, ACL-F | 400K+ instances, 21 datasets, 33 models, 10 baselines | query | single draw | most routers ≈ simple baseline; curation > pool size |
| [[routerarena]] | 2026, ICLR | live leaderboard | query | single draw | commercial vs academic routers head to head |
| VL-RouterBench | 2026, CVPR | 30.5K samples, 17 VLMs, 519K pairs | image+text query | single draw, binary | large gains, far from oracle |
| MMR-Bench | 2026 | OCR / VQA / multimodal math | image+text query | precomputed utility | beats best single MLLM at ~⅓ cost |
| xRouteBench ([[llmrouter-library]]) | 2026 | 5 scenarios (QA, long-context memory, vision, time-series, personalization) | query | — | no single router wins everywhere |
| DSC ([[dsc-robustness]]) | 2026, EACL | categorized incl. jailbreak, privacy | query | — | jailbreaks routed to weak models |
| TwinRouterBench | 2026, NeurIPS | 970 verified prefixes (static) + live SWE-bench Verified | agent step | execution-verified tier | judge-free static track plus live spend |
| RouteJudge | 2026 | online platform | routing decision | pairwise user preference | preference-based router evaluation |
| AgentSelect | 2026, ICML | 111K queries, 108K agent configs | query → agent config | interaction records | CF/GNN fragile on long tail |

**What none of them do yet:** multi-sample (noise-aware) labels at evaluation time, an artifact audit, a task-type-oracle baseline, real and changing prices, or confidence intervals. All of these are combined in P1 ([[06-research-proposals]]).

## 2. Headline results reported by router papers

| Method | Action space | Reported result (authors unless noted) | Note |
|---|---|---|---|
| [[routellm]] | strong/weak | >85% cost cut on MT-Bench, ~35% on GSM8K vs GPT-4-only | Arena preferences |
| FORC | 1 of 4 LMs | matches largest LM at 63% lower cost (14 datasets) | meta-model |
| MixLLM | 1 of k + latency | 97.25% of GPT-4 quality at 24.18% cost | contextual bandit |
| PILOT | 1 of k under budget | ~93% of GPT-4 at 25% cost (secondary summary) | bandit + knapsack |
| [[best-route]] | model × n samples | up to 60% cost cut, <1% drop | Microsoft |
| [[route-to-reason]] | model × reasoning strategy | >60% fewer tokens, above best single model | |
| R2-Router | model × output-length budget | ~4–5× lower cost than prior routers | ICML 2026 |
| [[routing-collapse]] (EquiRouter) | 1 of k | ~17% cost cut at GPT-4-level on RouterBench | fixes collapse |
| [[llms-encode-failures]] | 1 of k via probes | beats best single model; up to 70% cost cut on MATH | pre-generation activations |
| SATER | route or cascade | >50% cost and >80% cascade-latency reduction | confidence-aware rejection |
| ConsRoute | device/edge/cloud | ≥95% of cloud quality at ~40% lower latency and cost | prefill features |
| ACAR | 1/2/3-model ensembles | 55.6% vs 54.4% two-model baseline, skipping full ensemble on ~54% of tasks | training-free |
| CSCR | 1 of k | up to 25% better accuracy–cost trade-off | FAISS kNN |
| TagRouter | 1 of k | +6.15% accept rate, −17.2% cost vs 13 baselines | training-free |
| OmniRouter | global budget | +6.3% accuracy, ≥10% cost cut | Lagrangian |
| MasRouter | MAS mode/roles/LLMs | up to 52% cost cut on HumanEval | |
| [[agentrouter-agentic]] | per agent step, 4 tiers | −72% cost, <3% completion drop | workshop paper |
| RelayLLM | token-level, small model controls | large model writes ~1.07% of tokens; 42.5 → 49.5% on math | GRPO |
| STEER | per reasoning step | up to +20% over large model on AIME at 48% fewer FLOPs | logit confidence |
| [[dart]] | think budget | thinking tokens −15–69% (math), −51–63% (code) | training-free |
| GreenServ | 1 of 16 open models | +22% accuracy, −31% energy vs random | bandit |
| Avengers | cluster routing + voting | 10 ~7B models beat GPT-4.1 on 9 of 15 datasets | |
| [[hydra-copilot-auto]] | requirement-matching | iso-quality with Claude Sonnet 4.6 at 54% savings on SWE-Bench Verified | deployed in Copilot |

## 3. Critical / meta results (the yardstick problem)

| Study | Result |
|---|---|
| [[knn-router]] | tuned kNN matches or beats learned routers |
| [[routing-plateau]] | 21 methods in a narrow band; +1.24 pp from more data, encoders and fine-tuning |
| [[routing-gap-noise]] | 12–36% of router–oracle gap is single-draw noise |
| [[unsolvability-ceiling]] | truncation artifacts (65% MMLU, 57% MedQA); routers collapse to majority class (13–17 pp cost) |
| [[task-type-gap]] | hardest 11–35% of queries hold 70–91% of the gap (cited prior work); residual ≈ task type |
| [[llmrouterbench]] | top routers ≈70–72% vs oracle ≈92% (secondary summary); recall failures dominate |
| Intelligence per Watt | oracle local/cloud routing: −80% energy, −74% cost; an 80%-accurate router gets ~80% of that |
| [[replay-gap]] | log-replay evaluation of agent model switching mispredicts every success-relevant outcome |

**How to read this.** Headline savings of 50–85% mostly measure the gap between *always-frontier* and *mostly-cheap*. Coarse difficulty or task routing captures much of that. The critical studies show that *instance-level* gains beyond that are small and fragile under honest evaluation. That is the case for P1 (measure honestly) and P2 (new information sources) in [[05-gaps-and-agenda]].
