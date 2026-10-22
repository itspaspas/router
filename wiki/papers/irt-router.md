---
type: paper
title: IRT-Router (ACL 2025)
sources: [song2025irtrouter, radar2025]
---
# IRT-Router: Effective and Interpretable Multi-LLM Routing via Item Response Theory
ACL 2025 (aclanthology 2025.acl-long.761). Category: [[predictive-routers]].

**Idea.** Borrow psychometrics: each LLM has latent *ability* vectors, and each query has *difficulty* and *discrimination* parameters predicted from its embedding. P(correct) follows an IRT link. This gives interpretable routing and a warm-up for cold-start queries.
**Follow-ons.** RADAR (NeurIPS 2025 WS) treats (model, reasoning budget) pairs as respondents ([[reasoning-effort-routing]]). The top entry on RouterArena's initial board was an IRT-style (MIRT-BERT) router ([[routerarena]]).
**Critique.** Shown to exhibit routing collapse ([[routing-collapse]]).
