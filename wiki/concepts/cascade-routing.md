---
type: concept
title: Cascade routing (unifying routing and cascading)
sources: [dekoninck2024unified, nvidia2026prefill, lu2026plateau]
---
# Cascade routing

[[unified-routing-cascading]] (Dekoninck, Baader, Vechev, ICML 2025) treats model selection as a sequential decision. At every step, *given what has been observed so far*, the policy picks the next model to run, or stops. Routing is the zero-step special case and cascading is the fixed-order special case. They prove the optimal policy and find **quality estimators are the critical factor**: with poor estimators, no strategy helps.

**Why it matters for the frontier.** The routing plateau ([[routing-plateau]]) says query-only routers have hit a ceiling and recommends looking at *partial trajectories*. Cascade routing is the natural formal home for that: a cheap, partial observation (prefill activations, a 32-token draft, a probe) is one more "step" with its own cost. The open problem is to choose *which observation to buy* (value of information), as laid out in [[gap-query-only-signal-ceiling]] and proposal P2 in [[06-research-proposals]].
