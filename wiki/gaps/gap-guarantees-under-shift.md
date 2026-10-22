---
type: gap
title: G10 Guarantees under distribution shift
sources: [su2025cprouter, conformal2026, somerstep2025carrot, jitkrittum2025uniroute, dekoninck2024unified]
---
# G10: Few routers come with guarantees, and none hold under shift

**Evidence.** Conformal routers (CP-Router; Conformal LLM Routing, ACL SRW 2026), rate-optimal estimation ([[carrot]]), excess-risk bounds ([[uniroute]]) and optimal policies given estimators ([[unified-routing-cascading]]) exist. All assume exchangeable or i.i.d. data.

**What is missing.** Risk-controlling routers: "quality ≥ q with probability 1−α at minimal cost" under *covariate and label shift* (new user populations, new tasks); online conformal recalibration as traffic drifts; regret bounds versus the best fixed model in hindsight (so a router is *never* much worse than not routing). This guarantee is what operators need before deploying a learned router instead of a rule ([[gateways-and-semantic-router-libs]]).
