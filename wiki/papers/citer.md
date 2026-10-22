---
type: paper
title: CITER (2025)
sources: [zheng2025citer]
---
# CITER: Collaborative Inference for Efficient LLM Decoding with Token-Level Routing
Zheng et al., arXiv:2502.01976 (NeurIPS 2024 WS version). Category: [[token-level-routing]].

**Idea.** A token-level router sends non-critical tokens to a small model and critical ones to the large model. It is trained with RL, with a reward combining prediction quality and inference cost, and optimized via a preference-style objective.
**Evidence (reported).** ~30–42% inference cost reduction at maintained or improved accuracy on reasoning tasks.
**Limits.** Shared tokenizer and white-box models are required, and KV-cache handoff overhead remains ([[gap-serving-coupling]]).
