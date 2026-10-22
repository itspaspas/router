---
type: gap
title: G10 Guarantees under distribution shift
sources: [su2025cprouter, conformal2026, somerstep2025carrot, jitkrittum2025uniroute, dekoninck2024unified, hao2026racer]
---
# G10: Few routers come with guarantees, and none hold under shift

**Evidence.** Conformal routers (CP-Router; Conformal LLM Routing, ACL SRW 2026), rate-optimal estimation ([[carrot]]), excess-risk bounds ([[uniroute]]) and optimal policies given estimators ([[unified-routing-cascading]]) exist. All assume exchangeable or i.i.d. data.

**What is missing.** Risk-controlling routers: "quality ≥ q with probability 1−α at minimal cost" under *covariate and label shift* (new user populations, new tasks); online conformal recalibration as traffic drifts; regret bounds versus the best fixed model in hindsight (so a router is *never* much worse than not routing). This guarantee is what operators need before deploying a learned router instead of a rule ([[gateways-and-semantic-router-libs]]).

## Prior art and counter-evidence (iteration 2)
[[racer]] (ICML 2026) gives *distribution-free* misrouting-risk control for set-valued routing with abstention, and conformal routing work continues (CP-Router at AAAI 2026; Conformal LLM Routing at ACL SRW 2026). Guarantees under **exchangeability** are therefore now available. The gap narrows to (1) shift and drift, (2) conditional rather than marginal coverage (per user or task), (3) query-only guarantees that do not need every model's output, and (4) "never worse than best fixed model" regret guarantees online.
