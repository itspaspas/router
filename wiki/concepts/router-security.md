---
type: concept
title: Router security and robustness
sources: [shafran2025rerouting, rerouteguard2026, kassem2025robust, r2a2026, youragent2026]
---
# Router security

The router is a *control plane*. Whoever manipulates it controls cost, quality and safety.

- **Rerouting attacks** ([[rerouting-llm-routers]], COLM 2025): query-independent *confounder gadgets* force routing to the strong (expensive) model. The paper frames this as an "LLM control-plane integrity" problem.
- **Measurement and defense** ([[rerouteguard]], 2026): real routing systems are vulnerable, especially to *cost escalation*. An embedding-based detector with adaptive thresholds reports >99% detection.
- **Safety by category** ([[dsc-robustness]], EACL 2026): routers send jailbreaks to *weaker* models (less aligned), and coding/math to the strongest regardless of need.
- **Route-to-Rome attack** (R2A, ACL 2026): routing manipulation attacks.
- **Malicious intermediaries** (*Your Agent Is Mine*, CCS 2026): API routers terminate TLS and see plaintext. Of 28 paid and 400 free routers measured, 9 injected malicious code into tool calls and 17 accessed planted credentials. Proposed defenses: fail-closed policy gating, response anomaly screening, transparency logs.
- **Model substitution** ([[model-substitution-audit]], NeurIPS 2025): software-only detection of a cheaper model behind an endpoint is unreliable, so the paper argues for TEE attestation.

**Gaps** ([[gap-adversarial-robustness]]): certified or worst-case-bounded routers; safety as a first-class routing objective (a safety floor per route); cost-DoS budgets per tenant; auditing whether a third-party router actually sends you to the model it claims ([[gap-transparency-and-control]]).
