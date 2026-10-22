---
type: concept
title: Non-parametric and memory-based routers (kNN, graph)
sources: [shnitzer2023benchmark, li2025knn, zhao2024eagle, feng2024graphrouter, contextualrouter2026, routeprofile2026, smoothie2024, gmtrouter2025]
---
# Non-parametric and memory-based routers

**kNN / retrieval.** To route a new query, look up similar past queries and use the models' observed correctness on them. Shnitzer et al. (2023) learned routers from benchmark results this way. Li (2025) showed that a *well-tuned kNN matches or beats complex learned routers* at ≈0.3 ms per query ([[knn-router]]), and later work confirmed kNN sits among the leaders on every benchmark ([[routing-plateau]]). ContextualRouter (EACL SRW 2026) found plain kNN averaging about as good as its attention re-weighting. Eagle keeps global and local ELO scores that update online without retraining.

**Graph memory.** [[graphrouter]] builds a task–query–LLM heterogeneous graph and frames routing as edge prediction; it generalizes to new LLMs given a few edges. GMTRouter and PersonalizedRouter add *user* nodes ([[personalized-routing]]). RouteProfile uses graph profiling for cold-start models ([[cold-start-and-model-representation]]).

**Label-free.** Smoothie (NeurIPS 2024) routes with weak supervision from cross-model agreement and no labels.

**Why kNN keeps winning (hypothesis).** Model performance is locally smooth in embedding space, and the available labels are noisy single draws ([[routing-gap-noise]]). Parametric routers therefore have little signal to exploit beyond local averages. This argues for *changing the inputs* rather than the model class ([[gap-query-only-signal-ceiling]]).
