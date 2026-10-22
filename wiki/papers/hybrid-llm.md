---
type: paper
title: Hybrid LLM (ICLR 2024)
sources: [ding2024hybrid]
---
# Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing
Ding et al., arXiv:2404.14618, ICLR 2024. Category: [[predictive-routers]].

**Idea.** A BERT-style router predicts the *quality gap* between a small and a large model for a query, and sends it to the small one when the predicted gap is small. A test-time threshold trades quality for cost without retraining. A relaxed-label variant handles stochastic generation quality.
**Legacy.** It defined the binary strong/weak routing template that [[routellm]] scaled up with preference data.
**Limits.** Two models only, and a closed pool.
