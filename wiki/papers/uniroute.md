---
type: paper
title: UniRoute — Universal Model Routing (2025)
sources: [jitkrittum2025uniroute]
---
# Universal Model Routing for Efficient LLM Inference
Jitkrittum et al. (Google), arXiv:2502.08773. Category: [[cold-start-and-model-representation]].

**Idea.** Represent each LLM by a *feature vector of its errors on a small set of representative prompts*, for example per-cluster error rates. A router defined over these features applies to **models never seen in training**. The paper gives excess-risk bounds.
**Significance.** The cleanest formulation of dynamic-pool routing. The open follow-up is *which* prompts to use and how few suffice ([[gap-nonstationary-pools]]).
