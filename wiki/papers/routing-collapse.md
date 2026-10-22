---
type: paper
title: When Routing Collapses / EquiRouter (2026)
sources: [lai2026equirouter]
---
# When Routing Collapses: On the Degenerate Convergence of LLM Routers
Lai & Ye, arXiv:2602.03478 (Feb 2026); a NeurIPS 2026 version is titled "When LLM Routers Overpay: Strong-Model Over-Selection under Loose Budgets". Code: AIGNLAI/EquiRouter. Category: [[decision-aware-training]].

**Phenomenon.** As the cost budget grows, routers converge to always calling the strongest model, even when cheaper models tie. Small models are under-used. This was confirmed on EmbedLLM, GraphRouter and IRT-Router.
**Cause.** Training predicts scalar scores, while the decision is a discrete comparison among near-tied candidates. Small regression errors flip the argmax.
**Fix.** EquiRouter learns *rankings* directly (decision-aware). Reported ≈17% cost reduction at GPT-4-level performance on RouterBench, roughly half the strongest-model call rate, and holds on out-of-domain benchmarks.
