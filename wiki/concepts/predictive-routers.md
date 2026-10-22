---
type: concept
title: Predictive (score-based) routers
sources: [ding2024hybrid, ong2024routellm, lu2023zooter, hari2023tryage, song2025irtrouter, frick2025p2l, somerstep2025carrot, nvidia2026prefill, srivatsa2024multipleminds]
---
# Predictive routers

Learn f(x) → ŝ ∈ ℝ^k, the predicted quality (and sometimes cost) of each model on query x, then apply a decision rule (argmax utility, or a threshold on the strong-vs-weak gap).

**Lineage**
- *Binary strong/weak*: Hybrid LLM ([[hybrid-llm]]) predicts the quality gap with a BERT classifier and exposes a test-time threshold. [[routellm]] learns the same decision from Chatbot Arena preferences using matrix factorization, BERT, causal-LLM and similarity-weighted ranking routers.
- *Multi-model regression/classification*: Zooter distils reward-model scores ([[zooter]]); Tryage predicts per-model loss; FORC uses a meta-model plus assignment.
- *Psychometric*: [[irt-router]] fits item-response-theory ability and difficulty parameters, which makes routing interpretable. RADAR extends this to model × reasoning-budget configurations.
- *Prompt-conditioned leaderboards*: Prompt-to-Leaderboard ([[p2l]]) predicts a Bradley–Terry vector per prompt.
- *Rate-optimal estimation*: [[carrot]] estimates cost and accuracy with minimax guarantees.
- *Richer inputs*: NVIDIA's prefill-activation router reads model internals instead of a sentence embedding ([[quality-estimation]]).

**Known weaknesses.** They regress *average* trends and miss instance-specific wins ([[routing-plateau]]). Scalar-score training is misaligned with the argmax decision, which causes collapse to the strongest model ([[routing-collapse]]). A closed output head means retraining whenever the pool changes ([[cold-start-and-model-representation]]). An early study already found routers rarely beat the best single model on reasoning (Srivatsa et al. 2024).

Compare [[nonparametric-routers]], which often match these with no training ([[knn-router]]).
