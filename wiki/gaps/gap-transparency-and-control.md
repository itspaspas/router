---
type: gap
title: G13 Transparency, user control and auditing
sources: [openai2025gpt5, mahmood2026userchoice, routesplain2025, tran2025archrouter, youragent2026, cai2025substitution]
---
# G13: Who does the router serve, and how would anyone know?

**Evidence.** The GPT-5 router backlash ([[gpt5-router]]). Provider incentives to throttle or downgrade ([[user-choice-stackelberg]]). Opaque commercial routers ([[azure-model-router]], [[not-diamond]]). Explainable routing exists but is rare (ROUTESPLAIN). Arch-Router shows that policy-based control is feasible ([[arch-router]]).

**What is missing.** (1) **Auditing**: black-box tests that detect silent downgrades (statistical model fingerprinting of responses). (2) **Controllable routing**: user-stated quality floors and budgets, honoured and reported. (3) **Explanations** that are faithful (why this model). (4) **Disclosure norms**: which model answered, at what effort. (5) Formal analysis of provider–user incentive misalignment and of mechanisms that fix it ([[economics-and-incentives]]).

## Prior art and counter-evidence (iteration 2)
- [[model-substitution-audit]] (NeurIPS 2025) shows software-only detection of model substitution is unreliable (quantization, random substitution, benchmark-aware evasion) and argues for **TEE attestation**. Pure black-box auditing (the original P9) is therefore likely a dead end. The tractable route is attestation plus per-response disclosure.
- *Your Agent Is Mine* (CCS 2026) measured 428 API routers and found 9 injecting malicious code and 17 touching planted credentials. Intermediary routers are an active supply-chain threat, not only a theoretical one ([[router-security]]).
