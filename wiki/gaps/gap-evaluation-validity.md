---
type: gap
title: G1 Evaluation validity
sources: [dars2026, chen2026gapreal, garg2026unsolvability, lu2026plateau, li2026llmrouterbench, lee2026tasktype, li2025knn]
---
# G1: We cannot yet measure router progress reliably

**Evidence.** Single-draw labels inflate the oracle by 12–36% of the gap ([[routing-gap-noise]]). Truncation, judge and format artifacts manufacture "unsolvable" queries ([[unsolvability-ceiling]]). 21 methods sit inside one narrow band ([[routing-plateau]]). kNN and simple baselines tie sophisticated and commercial routers ([[knn-router]], [[llmrouterbench]]). The recoverable residue looks like task type ([[task-type-gap]]).

**What is missing**
1. A **multi-sample, artifact-audited oracle** as the default (k ≥ 5 samples per query–model pair; report pass@1 expectations rather than lucky draws).
2. **Mandatory baselines**: best single model, kNN, task-type oracle (per-task best model), and random routing at matched cost.
3. **Real prices and real traffic mixes**. Static 2023 prices and benchmark mixtures misrepresent deployment; Arena/OpenRouter-like distributions are rarely used.
4. **Uncertainty**: confidence intervals over query resampling and seeds. Most leaderboard gaps are within noise.
5. **Freshness**: pools go stale within months, so the benchmark needs to be *living* ([[routerarena]] is a start).
6. Metrics for **gap recovered beyond task type**, which isolates real instance-level routing.

**Proposal.** See P1 in [[06-research-proposals]].

## Prior art (iteration 7)
DARS (2026) builds router supervision from *repeated observations*, crossing meaning-preserving query rewrites with repeated stochastic decoding to get distributional capability estimates. Together with [[routing-gap-noise]], this means multi-sample labels are already proposed. P1's remaining novelty is the **full protocol** (artifact audit, task-type oracle, real prices, confidence intervals, living pool) and its adoption as a benchmark standard, not multi-sampling itself.
