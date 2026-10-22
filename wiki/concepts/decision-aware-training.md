---
type: concept
title: Decision-aware router training (and routing collapse)
sources: [lai2026equirouter, tsiourvas2025causal, garg2026unsolvability, dars2026]
---
# Decision-aware training

The standard recipe is *predict-then-optimize*: regress per-model scores, then take an argmax under a cost penalty. Two failure modes follow.

1. **Routing collapse** ([[routing-collapse]], Lai & Ye 2026). As the budget loosens, routers pour traffic into the most expensive model even when a cheaper one ties. Near-ties combined with small regression errors flip the argmax. This was confirmed on EmbedLLM, GraphRouter and IRT-Router. *Fix:* EquiRouter learns rankings directly, cutting cost ≈17% at GPT-4-level quality on RouterBench.
2. **Majority-class collapse** ([[unsolvability-ceiling]]). When the smallest model is optimal for ≈79% of training queries, routers learn to predict that class, which costs 13–17 pp against what is achievable. Random-feature and shuffled-label controls confirm that the router learned no query signal.

**Remedies in the literature.** Ranking/pairwise losses (EquiRouter, SW-ranking in [[routellm]]), end-to-end regret (Causal LLM Routing), cost-sensitive objectives, and modelling stochastic correctness as distributions (DARS, 2026) rather than single 0/1 labels ([[routing-gap-noise]]).

**Open problem.** Nobody yet trains routers with a *calibrated* utility under the *deployment* cost curve (prices change; see [[gap-nonstationary-pools]]), or with guarantees on regret relative to the best fixed model ([[gap-guarantees-under-shift]]).
