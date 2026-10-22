---
type: system
title: HyDRA in GitHub Copilot auto-mode (2026)
sources: [hydra2026]
---
# HyDRA: Hybrid Dynamic Routing Architecture (GitHub Copilot auto-mode)
Garg, Singha Roy, Jang, Brancasi, Fu, arXiv:2605.17106 (May 2026). Locus: provider-internal, deployed ([[industry-landscape]]).

- **Method.** A ModernBERT encoder with four independent sigmoid heads scores each query's *requirements* (reasoning, code generation, debugging, tool use). *Shortfall matching* then picks the cheapest model whose capability profile covers them. Model identities are decoupled from learned parameters, so adding or removing a model is a **config change, not retraining** ([[cold-start-and-model-representation]]). Median latency is 86 ms on CPU.
- **Results (authors).** SWE-Bench Verified, five-model pool: 75.4% vs 74.2% for always-Claude-Sonnet-4.6 at 12.9% savings; iso-quality at **54.1% savings**; 72.5% savings for a 3.2-point drop. Reported to transfer to LiveCodeBench, BigCodeBench and τ-bench, and claimed to route consistently across languages and scripts ([[gap-coverage]]).
- **Deployment.** The paper reports HyDRA is deployed to all users in GitHub Copilot's VS Code Chat auto-mode. That makes it a rare *published* learned router in large-scale production ([[gap-learning-from-logs]]).
- **Reading.** It is a *requirements-vs-capabilities* design, close to task-type routing ([[task-type-gap]]) with a cost-minimizing matcher. That is consistent with the evidence that coarse capability structure carries most of the recoverable value. The evaluation is still offline benchmarks, and no live-traffic outcome data is published.
