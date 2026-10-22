---
type: concept
title: LLM routing (hub)
---
# LLM routing

**Definition.** An *LLM router* is a policy π(x, state) → action that, for an input x, decides **which model(s), at which effort, and in what order** to invoke from a candidate pool M = {m₁…m_k}, optimizing a utility such as quality − λ·cost under constraints (budget, latency SLO, safety, privacy). It sits *outside* the models, unlike Mixture-of-Experts gating ([[routing-vs-moe]]).

**Why it exists.** No single model dominates every query; cost spans 2–3 orders of magnitude across a pool; most traffic is "easy". RouterEval found a *model-level scaling-up* effect: with a good router, adding candidates keeps raising the ceiling ([[routereval]]). On static benchmarks the oracle router beats the best single model by a large margin (≈92% vs ≈70–72% top routers on [[llmrouterbench]]), and that headroom drives the field. How much of it is real is now disputed ([[oracle-gap]]).

## Map of the field
- Design dimensions: [[design-space]]
- Before generation: [[predictive-routers]], [[representation-matching-routers]], [[nonparametric-routers]]
- After or during generation: [[cascades]], [[cascade-routing]], [[collaborative-routing]], [[token-level-routing]]
- Objectives and learning: [[budgeted-online-routing]], [[decision-aware-training]], [[personalized-routing]]
- New axes: [[reasoning-effort-routing]], [[agentic-routing]], [[serving-aware-routing]], [[multimodal-routing]]
- Inputs to every router: [[quality-estimation]], [[cold-start-and-model-representation]]
- Evaluation: [[router-evaluation]], [[oracle-gap]]
- Risks and economics: [[router-security]], [[economics-and-incentives]]
- Deployed reality: [[industry-landscape]]
- What is missing: [[05-gaps-and-agenda]]
