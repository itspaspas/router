---
type: concept
title: Budgeted, constrained and online (bandit) routing
sources: [sakota2023forc, optllm2024, omnirouter2025, metallm2024, wang2025mixllm, panda2025pilot, streaming2025, somerstep2025carrot, tsiourvas2025causal, bae2026retrials, auction2026]
---
# Budgeted and online routing

**Batch-constrained assignment.** Given N queries and a total budget B, assign queries to models to maximize total predicted quality: FORC, OptLLM (multi-objective), OmniRouter (a global budget with a controllable performance target). This is a knapsack/LP over predicted scores, so it inherits all of their errors ([[decision-aware-training]]).

**Online / bandit.** Queries arrive one by one, and feedback is only seen for the chosen model. MetaLLM uses a multi-armed bandit. MixLLM runs a contextual bandit with latency constraints and continual updates. PILOT (EMNLP Findings 2025) uses a preference-prior contextual bandit plus an online budget policy. *Near-Optimal Online Deployment and Routing for Streaming LLMs* (ICLR 2026) handles models that *arrive over time*.

**Learning from logs.** Causal LLM Routing (NeurIPS 2025) learns from *observational* data (logged decisions) with an end-to-end regret objective. Bae et al. (2026) learn routing *and scheduling* from user retrials using contextual queueing bandits ([[user-retrials]]). Both point to the largely untapped resource of production logs ([[gap-learning-from-logs]]).

**Mechanisms.** Truthful reverse auctions (AAMAS 2026) treat providers as strategic bidders ([[economics-and-incentives]]).

**Verified details (iteration 2).** PILOT is a preference-prior LinUCB with an online multi-choice-knapsack budget policy. MixLLM reports 97.25% of GPT-4 quality at 24.18% cost under a time constraint. BaRP (2025) trains under pure bandit feedback. Causal LLM Routing uses surrogate regret losses (a classification upper bound and a softmax-weighted approximation) with causal adjustment for the logging policy.
