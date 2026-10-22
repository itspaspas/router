---
type: concept
title: Representation-matching routers
sources: [chen2024routerdc, zhuang2024embedllm, tran2025archrouter, cscr2025, tagrouter2025, avengers2025, vllmsr2026]
---
# Representation-matching routers

Embed queries and models (or intents/policies) in a shared space and route by similarity.

- **Contrastive query↔LLM alignment**: [[routerdc]] (dual contrastive loss); CSCR (cost-aware contrastive routing, NeurIPS 2025).
- **Model embeddings**: [[embedllm]] learns a compact vector per LLM from correctness data. This is the key enabler for [[cold-start-and-model-representation]].
- **Policy/intent matching**: [[arch-router]] maps a query to user-written `(domain, action)` policies, each bound to a model. Adding a model just means editing the policy table. TagRouter matches tags and the Avengers cluster queries. The production equivalents are semantic routers ([[vllm-semantic-router]], [[gateways-and-semantic-router-libs]]).

**Trade-off.** Matching routers generalize and are fast, but they encode *topic*, not *difficulty*. A coding query lands on the coding model whether it is trivial or hard. DSC showed exactly this category-driven behaviour ([[dsc-robustness]]), and the [[task-type-gap]] analysis suggests task type is still where most of the recoverable headroom lies.
