---
type: concept
title: Serving-aware routing (latency, load, energy, edge)
sources: [routerwise2026, hwrouter2026, lodestar2026, robatch2026, greenserv2026, ipw2025, cloudedge2025, federate2026, lqm2026, wang2025mixllm]
---
# Serving-aware routing

Most quality/cost routers assume each model is an infinitely elastic API. In self-hosted serving, queues, batching and KV-cache reuse dominate latency.

- **Joint placement and routing**: [[routerwise]] (2026). Naive cascades overload the cheapest model's queue; joint resource allocation keeps TTFT near the SLO.
- **Hardware-aware**: HW-Router reports 3.4–3.9× lower e2e latency under overload vs. static routing.
- **Instance-level** (the same model on many replicas): Lodestar, a learned router aware of batching and KV reuse.
- **Batch prompting**: RoBatch makes routing aware of batched-prompt economics.
- **Energy**: GreenServ. Intelligence-per-Watt (Stanford) finds local models answer 88.7% of queries. Oracle local/cloud routing would cut energy ~80% and cost ~74%, and an 80%-accurate router captures ~80% of those gains.
- **SLA-constrained RL**: PROTEUS (2026) uses Lagrangian RL for SLA-aware multi-LLM serving.
- **Edge/cloud and federated**: cloud-edge routing; *Federate the Router* trains routers across clients without sharing data. On-device→cloud escalation is covered under [[cascades]].

**Gap** ([[gap-serving-coupling]]): a router whose utility includes *current* queue state, prompt-cache hits and switch costs, co-designed with the scheduler. Today quality routers and load balancers are separate layers that optimize conflicting objectives.
