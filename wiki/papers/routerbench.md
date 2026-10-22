---
type: paper
title: RouterBench (2024)
sources: [hu2024routerbench]
---
# RouterBench: A Benchmark for Multi-LLM Routing System
Hu et al. (Martian), arXiv:2403.12031, ICML 2024 WS. Code: withmartian/routerbench. Category: [[router-evaluation]].

**Contribution.** 405K+ pre-generated inference outcomes (11 models, 8 datasets) so routers can be trained and evaluated *without running inference*. It introduced a cost–quality plane and the AIQ (average improvement in quality) metric, and it covers cascades and non-predictive baselines.
**Limits (seen later).** Single sampled outputs ([[routing-gap-noise]]), a 2023-era model pool, and static prices.
