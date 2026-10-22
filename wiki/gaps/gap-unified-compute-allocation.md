---
type: gap
title: G7 Unified test-time compute allocation
sources: [ding2025bestroute, radar2025, dart2026, su2025cprouter, dmr2026, openai2025gpt5]
---
# G7: No router allocates all test-time compute jointly

**Evidence.** Separate threads route over model ([[predictive-routers]]), reasoning effort ([[reasoning-effort-routing]], [[dart]]), number of samples ([[best-route]]), precision (DMR), granularity ([[token-level-routing]]), and collaboration ([[collaborative-routing]]).

**What is missing.** One policy over the product space *(model, effort/budget, n samples, aggregation, retrieval on/off, tool use)*, with a shared quality estimator and a single budget. Real providers already expose all these knobs. Questions: Do quality estimators transfer across knobs? Is the utility surface smooth enough for gradient-free search per query? What is the scaling law of "compute-optimal routing" (cf. test-time-compute scaling laws)?
