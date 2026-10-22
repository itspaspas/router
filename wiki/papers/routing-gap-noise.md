---
type: paper
title: How Much of the Routing Gap Is Real? (2026)
sources: [chen2026gapreal]
---
# How Much of the Routing Gap Is Real? Decomposing the Router-to-Oracle Gap into Reproducible Specialist Advantage and Single-Draw Label Noise
Teng-Ruei Chen, arXiv:2607.03436 (Jul 2026). Category: [[oracle-gap]], [[router-evaluation]].

**Problem.** Oracles use one sampled correctness label per (query, model). Under stochastic decoding that label is a random draw, so the oracle "picks the lucky sample" and overstates headroom.
**Result.** Expected oracle = reproducible part + a non-negative *selection floor*. On open-model pools (arithmetic, competition math, science), **~12–36% of the router–oracle gap is single-draw noise**. The share grows on less saturated benchmarks and approaches half on the hardest queries. The paper also proves a recoverability asymmetry.
**Deliverable.** A multi-sample oracle protocol that benchmarks should adopt ([[gap-evaluation-validity]]).
