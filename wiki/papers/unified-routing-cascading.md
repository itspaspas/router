---
type: paper
title: Unified routing and cascading (ICML 2025)
sources: [dekoninck2024unified]
---
# A Unified Approach to Routing and Cascading for LLMs
Dekoninck, Baader, Vechev (ETH Zurich), arXiv:2410.10347, ICML 2025. Category: [[cascade-routing]].

**Contributions.** (1) Proves the optimality of a standard routing strategy. (2) Derives a *new optimal cascading* strategy. (3) Proposes **cascade routing**, which at each step chooses the next model from all remaining ones given the answers so far, with routing and cascading as special cases. (4) Shows that *quality estimators* are the decisive factor.
**Evidence.** Cascade routing beats both routing and cascading consistently across benchmarks, by a large margin when estimators are good.
**Why central.** It is the theoretical frame that later "use partial trajectories" proposals ([[routing-plateau]]) and our value-of-information agenda ([[gap-query-only-signal-ceiling]]) build on.
