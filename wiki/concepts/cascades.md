---
type: concept
title: Cascades, deferral and self-assessment
sources: [chen2023frugalgpt, madaan2023automix, yue2023mot, gupta2024cascade, narasimhan2024fastcascade, ramirez2024twotier, chuang2024selfref, su2025cprouter, diSRouter2025, sater2025, ror2026]
---
# Cascades

Call the cheap model first, judge its output, and escalate only if it looks wrong. Unlike pre-generation routing, the decision sees *the answer*, which is a much stronger signal. The price is paying for the cheap call on every query, plus extra latency on escalated ones.

**Escalation signals**
- *Learned scorer* on (query, answer): [[frugalgpt]]
- *Self-verification* by the small model plus a POMDP meta-verifier: [[automix]]
- *Answer consistency* across sampled CoT/PoT (Yue et al., ICLR 2024)
- *Token-level uncertainty quantiles* (Gupta et al., ICLR 2024); two-tier uncertainty (Ramírez et al., COLM 2024)
- *Trained confidence tokens*: Self-REF; SATER trains the small model to refuse
- *Conformal sets*: CP-Router (LLM vs. LRM), Conformal LLM Routing (ACL SRW 2026) ([[gap-guarantees-under-shift]])
- *Decentralized*: DiSRouter, where each model self-assesses and passes along a chain
- *Resample vs. reroute* (RoR, 2026): retry the same model or move to another?

**Systems interaction.** Faster Cascades merges deferral with speculative decoding. RouterWise shows naive cascades *overload the cheapest model's queue* at high request rates ([[routerwise]], [[serving-aware-routing]]).

**Theory.** [[unified-routing-cascading]] gives the optimal cascade and shows that routing and cascading are two special cases of one cascade-routing policy ([[cascade-routing]]). Mahmood (ICLR 2026) shows that once users can re-prompt or abandon, the provider-optimal policy is usually *static routing without cascading* ([[user-choice-stackelberg]]). Whether to cascade is therefore an economic question as well as a technical one ([[economics-and-incentives]]).
