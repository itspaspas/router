---
type: gap
title: G7 Unified test-time compute allocation
sources: [ding2025bestroute, radar2025, dart2026, su2025cprouter, dmr2026, openai2025gpt5, pan2025rtr, odar2026, adaptivecomp2026, r2router2026]
---
# G7: No router allocates all test-time compute jointly

**Evidence.** Separate threads route over model ([[predictive-routers]]), reasoning effort ([[reasoning-effort-routing]], [[dart]]), number of samples ([[best-route]]), precision (DMR), granularity ([[token-level-routing]]), and collaboration ([[collaborative-routing]]).

**What is missing.** One policy over the product space *(model, effort/budget, n samples, aggregation, retrieval on/off, tool use)*, with a shared quality estimator and a single budget. Real providers already expose all these knobs. Questions: Do quality estimators transfer across knobs? Is the utility surface smooth enough for gradient-free search per query? What is the scaling law of "compute-optimal routing" (cf. test-time-compute scaling laws)?

## Prior art and counter-evidence (iteration 2)
Two-knob joint routing exists: [[route-to-reason]] (model × reasoning strategy, >60% token cut), [[best-route]] (model × n samples, up to 60% cost cut at <1% drop), RADAR (model × budget), ODAR (adaptive compute via active inference). The 2026 adaptive-computation survey lists "routing over models *and* inference configurations" as an open problem, which confirms the gap remains for the *full* product space with one shared estimator. It also notes that reported savings are often incomparable, because router, verifier and queueing costs are counted inconsistently. A unified router must use a unified cost accounting.

**Iteration 4 addition.** R2-Router (ICML 2026) adds *output-length budget* as a routing knob, jointly selecting (LLM, length budget) and reporting ~4–5× lower cost (authors). Output length is therefore one more dimension a unified compute router must cover.
