---
type: concept
title: Cold start, unseen models and model representation
sources: [jitkrittum2025uniroute, zhuang2024embedllm, zerorouter2026, routeprofile2026, feng2024graphrouter, zhang2025routerr1, tran2025archrouter, zhang2025capability, trouter2026, streaming2025]
---
# Cold start and model representation

Real pools change weekly: new releases, price cuts, deprecations, silent version updates. A router with a k-way softmax head must be retrained every time.

**Approaches to representing a model so new ones plug in**
- *Error vector on a probe set*: UniRoute ([[uniroute]]) represents each LLM by its correctness on a small set of representative prompts and routes via cluster-level errors.
- *Learned embeddings*: [[embedllm]]; Model-SAT capability instruction tuning.
- *Graph nodes with a few edges*: [[graphrouter]]; RouteProfile.
- *Universal difficulty space with anchor queries*: [[zerorouter]] (2026).
- *Natural-language descriptors* (price, latency, a few examples) read by an LLM router: [[router-r1]].
- *Policy table*: [[arch-router]] simply maps intents to models and sidesteps quality estimation entirely.

**Open questions** ([[gap-nonstationary-pools]]): how many and *which* probe queries to buy for a new model (optimal experimental design); detecting silent drift in an API model; handling deprecation; transfer when a new model differs qualitatively (a new reasoning mode, tool use).
