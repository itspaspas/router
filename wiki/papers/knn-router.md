---
type: paper
title: kNN beats complex routers (2025)
sources: [li2025knn]
---
# Rethinking Predictive Modeling for LLM Routing: When Simple kNN Beats Complex Learned Routers
Yang Li, arXiv:2505.12601 (May 2025). Category: [[nonparametric-routers]], [[oracle-gap]].

**Claim.** A well-tuned kNN router matches and often beats state-of-the-art learned routers on instruction-following, QA and reasoning benchmarks, plus a new multimodal routing set.
**Explanation offered.** Model performance is *local* in embedding space, so non-parametric methods are sample-efficient. Index build takes ~0.2–4 s and inference ~0.3 ms per query.
**Impact.** It made kNN a *mandatory baseline*. [[routing-plateau]] later confirmed kNN is among the leaders everywhere, and ContextualRouter found the same.
