---
type: paper
title: RouterWise (2026)
sources: [routerwise2026]
---
# RouterWise: Joint Resource Allocation and Routing for Latency-Aware Multi-Model LLM Serving
arXiv:2604.10907 (2026). Category: [[serving-aware-routing]].

**Finding.** With models on dedicated GPUs, FrugalGPT-style cascades overload the cheapest model's queue, because every prompt hits it first. RouteLLM-style routing also ignores load.
**Method.** Jointly optimize GPU allocation per model and the routing policy under a TTFT SLO.
**Evidence (4×A100).** It stays near a 500/800 ms TTFT target at 50–80 RPS, while the baselines overshoot sharply at matched quality.
**Lesson.** Quality routing and serving cannot be designed separately ([[gap-serving-coupling]]).
