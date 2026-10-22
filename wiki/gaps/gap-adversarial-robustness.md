---
type: gap
title: G9 Adversarial robustness and safety-aware routing
sources: [cascadefail2026, shafran2025rerouting, rerouteguard2026, kassem2025robust, r2a2026, youragent2026]
---
# G9: Routers are an unprotected control plane

**Evidence.** Confounder gadgets ([[rerouting-llm-routers]]), real-system cost escalation ([[rerouteguard]]), jailbreaks routed to weak models ([[dsc-robustness]]), R2A, and malicious intermediaries.

**What is missing.**
- **Robust training**: adversarial training for routers and *certified* routing margins (bounded change under token insertions).
- **Safety-aware objectives**: a per-route safety floor, so that risky intents never go to a less-aligned model, and a joint router plus guardrail ([[vllm-semantic-router]] bundles both heuristically).
- **Economic DoS**: per-tenant cost budgets and rate-limiting at the router.
- **Adaptive attacks** on detectors like RerouteGuard.
- **Supply-chain integrity**: verifying a third-party router actually called the claimed model (model fingerprinting / attestation; see [[gap-transparency-and-control]]).

## Prior art (iteration 8)
**R2A** (ACL 2026) makes rerouting a *black-box* attack: a hybrid ensemble surrogate router plus adversarial-suffix optimization raises the expensive-model routing rate on open-source *and commercial* routers. White-box access is no longer needed, which raises the priority of P8. A 2026 preprint also reports that adversarial attacks can trigger *cascade failures* in LLM cascades. Cascade designs ([[cascades]]) need their own threat model.
