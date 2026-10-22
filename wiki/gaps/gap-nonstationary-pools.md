---
type: gap
title: G3 Non-stationary model pools
sources: [jitkrittum2025uniroute, zerorouter2026, routeprofile2026, streaming2025, zhuang2024embedllm]
---
# G3: Pools, prices and models change faster than routers retrain

**Evidence.** Representation methods exist ([[uniroute]], [[embedllm]], [[zerorouter]], [[graphrouter]], RouteProfile), and online deployment of streaming models has been studied (ICLR 2026). But:
- **Probe budgets are ad hoc.** How few, and *which*, anchor queries characterise a new model? This is an *optimal experimental design / active learning* question (IRT computerized adaptive testing is a natural tool; see [[irt-router]]).
- **Silent drift.** API models change behind a stable name. Routers need drift detection and re-profiling triggers.
- **Price shocks.** Utility-trained routers ([[decision-aware-training]]) embed a cost curve, and a 5× price cut should re-route traffic without retraining. Cost should be an *input*, not a constant.
- **Qualitatively new capabilities** (new reasoning modes, tools, context lengths) break similarity-based transfer.
- **Deprecation and lifecycle.** Graceful removal of a model without degrading neighbours in embedding space.

**Proposal.** P7 in [[06-research-proposals]].
