---
type: paper
title: RACER — risk-controlled set routing (ICML 2026)
sources: [hao2026racer, conformal2026, su2025cprouter]
---
# RACER: Risk-Aware Calibrated Efficient Routing for Large Language Models
Hao, Zeng, Wei, Jing, arXiv:2603.06616, ICML 2026 (PMLR 306). Category: [[gap-guarantees-under-shift]], [[collaborative-routing]].

**Idea.** "α-VOR": output a *set* of models (to be aggregated) that keeps the expected set size small while bounding the probability of misrouting. Thresholds come from finite-sample concentration bounds, which allows variable set sizes and *abstention*. It is post hoc and wraps any base router.
**Guarantee.** Distribution-free risk control on exchangeable test data.
**Limits.** It needs base-router scores for all candidates. Guarantees are marginal and assume exchangeability, so they say nothing under shift. Conformal LLM Routing (ACL SRW 2026) critiques CP-Router and RACER for output dependence and marginal-only coverage.
