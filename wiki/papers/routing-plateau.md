---
type: paper
title: The Routing Plateau (2026)
sources: [lu2026plateau]
---
# The Routing Plateau: Understanding and Breaking the Accuracy Limits of LLM Routers
Lu et al. (Rice, Amazon), arXiv:2606.07587 (Jun 2026). Category: [[oracle-gap]].

**Finding.** 21 routing methods × 5 benchmarks converge to a *narrow accuracy band* well below the oracle, with kNN among the leaders everywhere. Diagnosis: routers learn **average model-performance trends**, not query-specific signals, and fail where instance-specific decisions matter.
**Interventions tried.** A 300K-query benchmark (Nine-by-300k), more data, larger encoders and end-to-end fine-tuning lift eight routers by only ~1.24 pp. The plateau persists.
**Proposed way out.** Inputs *beyond the query*, e.g. partial output trajectories, which is where [[cascade-routing]] and [[gap-query-only-signal-ceiling]] point.
