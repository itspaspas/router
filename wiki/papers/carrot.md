---
type: paper
title: CARROT (ICLR WS 2025)
sources: [somerstep2025carrot]
---
# CARROT: A Cost Aware Rate Optimal Router
Somerstep et al., arXiv:2502.03261. Category: [[budgeted-online-routing]], [[predictive-routers]].

**Idea.** Estimate each model's cost and accuracy for a query separately and plug them into a utility. The authors prove the estimator is minimax rate-optimal. They release the SPROUT dataset.
**Evidence.** Among the top three on RouterArena's initial leaderboard ([[routerarena]]).
**Note.** It is one of the few routers with statistical guarantees, but those cover estimation, not robustness under shift ([[gap-guarantees-under-shift]]).
