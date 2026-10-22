---
type: paper
title: LLMRouterBench (ACL Findings 2026)
sources: [li2026llmrouterbench]
---
# LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing
Li et al., arXiv:2601.07206, Findings of ACL 2026. Code: ynulihao/LLMRouterBench. Category: [[router-evaluation]], [[oracle-gap]].

**Scale.** 400K+ instances, 21 datasets, 33 models, 10 routing baselines in one framework, with latency-aware analysis.
**Findings.** (1) Many recent routers, **including commercial ones, fail to reliably beat a simple baseline**. (2) A large oracle gap persists, driven by *model-recall* failures: when only 1–3 models solve a query, routers rarely find them (secondary summary: top routers ≈70–72% vs oracle ≈92%). (3) The backbone embedding model matters little. (4) Larger pools give diminishing returns compared with *careful model curation* ([[gap-pool-design]]).
