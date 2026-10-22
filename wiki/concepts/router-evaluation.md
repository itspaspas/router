---
type: concept
title: Router evaluation and benchmarks
sources: [hu2024routerbench, huang2025routereval, lu2025routerarena, li2026llmrouterbench, llmrouterlib2026, modelglue2024, routerxbench2026, vlrouterbench2025, mmrbench2026, kassem2025robust, yuan2025whoroutes, routejudge2026, twinrouterbench2026]
---
# Router evaluation

**Benchmarks (offline, pre-generated outcomes)**
| Benchmark | Scale | Distinctive |
|---|---|---|
| [[routerbench]] (2024) | 405K outcomes, 11 models, 8 datasets | cost–quality frontier and AIQ metric; first standard |
| [[routereval]] (EMNLP-F 2025) | 200M+ records, 8,500+ LLMs, 12 evals | model-level scaling-up with candidate count |
| [[llmrouterbench]] (ACL-F 2026) | 400K instances, 21 datasets, 33 models, 10 baselines | most routers (incl. commercial) ≈ simple baseline; recall failures |
| [[routerarena]] (ICLR 2026) | live leaderboard | includes commercial routers (Azure, GPT-5) |
| xRouteBench in [[llmrouter-library]] | 5 scenarios | long-context, vision, time-series, personalization |
| DSC ([[dsc-robustness]]) | categorized | safety, privacy and jailbreak routing |
| VL-RouterBench, MMR-Bench | multimodal | [[multimodal-routing]] |

**Metrics.** Accuracy at a fixed cost; area under the cost–quality curve (AIQ); call-rate to the strong model; *gap recovered* = (router − best single) / (oracle − best single); latency and SLO attainment ([[serving-aware-routing]]).

**The validity crisis (2025–2026).** See [[oracle-gap]]: single-draw labels inflate the oracle, artifacts create fake unsolvables, routers converge to a plateau, and kNN ties everything. A credible 2027 router paper needs multi-sample labels, strong simple baselines (kNN, best-single, task-type oracle), real prices, and significance tests ([[gap-evaluation-validity]]).
