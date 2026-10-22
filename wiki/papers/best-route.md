---
type: paper
title: BEST-Route (ICML 2025)
sources: [ding2025bestroute]
---
# BEST-Route: Adaptive LLM Routing with Test-Time Optimal Compute
Ding et al., ICML 2025 (openreview tFBIbCVXkG). Category: [[reasoning-effort-routing]].

**Idea.** The action is *(model, n)*: route to a model **and** choose how many best-of-n samples to draw, with a reward model selecting among them. A small model with several samples can beat one large-model sample at lower cost.
**Significance.** The first clear statement that test-time compute is part of the routing action space. It is a building block for [[gap-unified-compute-allocation]].
