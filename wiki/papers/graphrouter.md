---
type: paper
title: GraphRouter (ICLR 2025)
sources: [feng2024graphrouter]
---
# GraphRouter: A Graph-based Router for LLM Selections
Feng, Shen, You (UIUC), arXiv:2410.03834, ICLR 2025. Category: [[nonparametric-routers]].

**Idea.** Build a heterogeneous graph of task, query and LLM nodes, with edges carrying performance and cost. Routing is *edge prediction* with a GNN. New LLMs are attached through a few edges, without retraining from scratch.
**Lineage.** The same group's later work includes [[router-r1]], GMTRouter, [[personalizedrouter]] and [[llmrouter-library]].
**Critique.** Shown to exhibit routing collapse ([[routing-collapse]]).
