---
type: system
title: vLLM Semantic Router
sources: [vllmsr2026]
---
# vLLM Semantic Router
github.com/vllm-project/semantic-router (Apache-2.0; v0.2 "Athena" in Mar 2026; paper arXiv:2603.04444). Origin: Red Hat and the vLLM community. Locus: open-source, inference-engine level ([[industry-landscape]]).

- A "signal-driven" router deployed as an **Envoy ext_proc** filter in front of vLLM backends, with Kubernetes/OpenShift support.
- Signals include ModernBERT-style intent/domain classifiers, semantic kNN, PII and jailbreak detection, and a semantic cache. It also decides **reasoning on/off** per request ([[reasoning-effort-routing]]).
- Evaluated on [[routerarena]] (initial board: vLLM-SR 63.8).
- It is notable for bundling *safety* signals into the routing decision ([[router-security]]), which is rarely done in academic routers.
