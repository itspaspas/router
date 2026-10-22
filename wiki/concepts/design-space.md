---
type: concept
title: Design space of LLM routers
---
# Design space

Every router chooses a value on each of these axes. The literature clusters in a few cells, and the gaps sit in the empty ones ([[05-gaps-and-agenda]]).

1. **Timing / information available**
   - *Pre-generation* (route on the query only): [[predictive-routers]], [[representation-matching-routers]], [[nonparametric-routers]]
   - *Post-generation* (inspect an answer, then escalate): [[cascades]]
   - *Mixed* (cheap probe, then route): [[cascade-routing]], prefill-activation routers ([[quality-estimation]]), draft agreement ([[reasoning-effort-routing]])
2. **Granularity**: conversation → query → agent step ([[agentic-routing]]) → reasoning segment → token ([[token-level-routing]])
3. **Action space**: pick 1 model; pick k and aggregate ([[collaborative-routing]]); pick model × reasoning effort × #samples ([[reasoning-effort-routing]]); pick a serving replica ([[serving-aware-routing]])
4. **Objective**: accuracy, quality − λ·cost, a hard budget ([[budgeted-online-routing]]), latency SLO, energy, safety, or user preference ([[personalized-routing]])
5. **Supervision**: benchmark correctness labels, pairwise human preference (Arena), reward models, LLM-judge, implicit feedback (switches, retrials), RL outcome rewards
6. **Model representation**: one-hot head per model (closed pool) vs. learned/derived model embeddings that allow unseen models ([[cold-start-and-model-representation]])
7. **Learning regime**: offline supervised, online bandit, RL, training-free (kNN, voting)
8. **Deployment locus**: client/on-device, gateway, provider-internal (GPT-5), inference engine (vLLM SR) ([[industry-landscape]])
