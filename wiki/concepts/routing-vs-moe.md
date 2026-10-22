---
type: concept
title: Routing vs Mixture-of-Experts
sources: [shazeer2017moe, fedus2021switch, varangot2025doing]
---
# Inter-model routing vs intra-model MoE gating

| | MoE gating (Shazeer 2017; Switch 2021) | LLM routing |
|---|---|---|
| Unit routed | token → expert FFN inside one network | query/step/token → whole, separately trained models |
| Trained | jointly, end-to-end with experts | post hoc; the models are frozen black boxes (often APIs) |
| Objective | load-balanced LM loss | quality vs. $ cost, latency, SLO, safety |
| Pool | fixed at training | open; models are added and retired weekly |

The survey arXiv:2502.00409 makes this distinction explicit. Some ideas transfer: load balancing ↔ [[serving-aware-routing]], and collapse onto a few experts ↔ routing collapse ([[decision-aware-training]]). [[token-level-routing]] sits in between: it routes per token like MoE but across separate models, like speculative decoding.

Back to [[llm-routing]].
