---
type: paper
title: Router-R1 (NeurIPS 2025)
sources: [zhang2025routerr1]
---
# Router-R1: Teaching LLMs Multi-Round Routing and Aggregation via Reinforcement Learning
Zhang, Feng, You (UIUC), arXiv:2506.09033, NeurIPS 2025. Code: ulab-uiuc/Router-R1. Category: [[collaborative-routing]].

**Idea.** The router is itself an LLM policy that interleaves `<think>` and `<route>` actions, calls pool models as tools, and integrates their responses into its context over multiple rounds. It is trained with RL using rule-based rewards: format, final-outcome correctness, and a **cost reward**.
**Generalization.** It conditions only on simple *model descriptors* (price, latency, example performance), so it can route to unseen models ([[cold-start-and-model-representation]]).
**Evidence.** Beats several strong baselines on seven general and multi-hop QA benchmarks while managing cost.
**Open.** Router inference cost (it is an LLM), credit assignment over rounds ([[gap-agentic-credit-assignment]]), and robustness of the cost reward to price changes.
