---
type: paper
title: Pandora's AI Model Routing Box (NeurIPS 2026)
sources: [fisch2026pandora]
---
# Pandora's AI Model Routing Box: Efficient Allocation with Costly Value Estimation
Fisch, Trivedi, Huot, Cohen, Kaisers, Lapata, Larson, Eisenstein, arXiv:2608.20316 (Aug 2026), NeurIPS 2026. Category: [[cascade-routing]], [[quality-estimation]].

**Idea.** Estimating each specialist's value is itself costly. Cheap estimators (embeddings) are noisy, while expensive ones (fine-tuned estimators with retrieval results or partial reasoning traces) are accurate. The paper casts routing as **Pandora's Box**, the classic optimal search with costly inspection. Under a Gaussian signal model, closed-form *value-of-information* indices decide, per specialist and input, whether refining the estimate is worth its cost.
**Variants.** *Pandora's Router* is centralized. *Pandora's Bidder* is decentralized: specialists decide whether to invest in self-assessment before accepting a price.
**Evidence (authors).** Across a multi-LLM benchmark, RAG specialists and variable-reasoning LLMs, it matches exhaustive estimation while calling the expensive estimator far less. Decentralized results are mixed: VOI reasoning helps when estimates are accurate, but with noisy estimates a strategic specialist can gain at others' expense ([[economics-and-incentives]]).
**Impact on our agenda.** This is the closest prior art to proposal P2 ([[gap-query-only-signal-ceiling]]). It establishes VOI routing with a *two-level* estimator (cheap vs expensive) under a Gaussian model. Still open: many *heterogeneous* observation types (activations, k-token drafts, full answers), non-Gaussian and correlated signals across models, multi-step acquisition, and cross-model transfer of a single observation.
