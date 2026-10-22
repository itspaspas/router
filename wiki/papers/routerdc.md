---
type: paper
title: RouterDC (NeurIPS 2024)
sources: [chen2024routerdc]
---
# RouterDC: Query-Based Router by Dual Contrastive Learning
Chen et al., arXiv:2409.19886, NeurIPS 2024. Category: [[representation-matching-routers]].

**Idea.** A small encoder plus learnable LLM embeddings, trained with two contrastive losses: sample–LLM (pull the query toward the best-performing LLMs) and sample–sample (keep similar queries close). Routes by similarity.
**Evidence.** Beat the best single model and prior routers on in- and out-of-distribution reasoning and coding suites at the time.
**Limits.** Closed pool (LLM embeddings learned per model). Later benchmarks find it within the routing plateau band ([[routing-plateau]]).
