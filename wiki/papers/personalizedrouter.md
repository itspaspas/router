---
type: paper
title: PersonalizedRouter (TMLR 2025)
sources: [dai2025personalized, gmtrouter2025]
---
# PersonalizedRouter: Personalized LLM Routing via Graph-based User Preference Modeling
Dai et al. (UIUC), arXiv:2511.16883, TMLR 2025. Category: [[personalized-routing]].

**Idea.** A heterogeneous graph over users, queries and LLMs, built from interaction histories (which model the user preferred). Routing is user-conditioned link prediction that trades off performance, cost and response style.
**Benchmark.** PersonaRoute-Bench (1,000 simulated users). The authors report large gains over the best baselines and few-shot adaptation to new users and LLMs.
**Sibling.** GMTRouter (arXiv:2511.08590) models multi-turn user–LLM–query–response graphs.
**Open.** Simulated users; privacy of per-user preference graphs ([[gap-transparency-and-control]]).
