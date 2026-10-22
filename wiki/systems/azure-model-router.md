---
type: system
title: Azure AI Foundry Model Router
---
# Azure AI Foundry Model Router (Microsoft)
Locus: provider-internal ([[industry-landscape]]).

- Deployed as a single "model" endpoint. A trained router picks, per prompt, among Azure-hosted OpenAI models (the GPT-4.1 family and o-series reasoning models at launch in 2025, with GPT-5-family models later).
- According to third-party descriptions, routing modes (Balanced / Cost / Quality) and automatic failover were added later.
- On [[routerarena]]'s initial board, "Azure-Router" scored 66.4, second only to an IRT-style academic router.
- It is opaque: users see which model answered but not why ([[gap-transparency-and-control]]).
