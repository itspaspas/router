---
type: gap
title: G4 Learning and evaluating from production logs
sources: [tsiourvas2025causal, bae2026retrials, openai2025gpt5, panda2025pilot, barp2025, gonuguntla2026replay]
---
# G4: Off-policy learning and evaluation for routers is almost absent

**Evidence.** Production routers learn from logged signals: switches, preferences and correctness for [[gpt5-router]], retrials in [[user-retrials]]. Academic routers almost all train on *full-information* benchmark matrices (every model answered every query). Causal LLM Routing (NeurIPS 2025) is one of the few that treats logs as *observational* data. Agentic routing logs are proposed as a flywheel ([[agentic-routing]]).

**Why it matters.** In deployment you only see the outcome of the model you chose (bandit feedback). Logs are confounded by the old router, and feedback is implicit, delayed and noisy.

**What is missing.** (1) Off-policy evaluation (IPS/doubly-robust) estimators validated for routing. (2) Logging-policy design (exploration rates that are safe and cheap). (3) Calibrated mappings from implicit signals (retry, edit, thumbs, abandonment) to utility. (4) A public **logged-bandit routing dataset**. (5) Counterfactual benchmarks that let academics test log-learning without a production system.

**Proposal.** P3 in [[06-research-proposals]].

## Prior art and counter-evidence (iteration 2)
- **Bandit-feedback training exists**: PILOT (preference-prior LinUCB plus knapsack budget, EMNLP-F 2025), MixLLM, BaRP (2025, trains only on the chosen model's outcome), and Causal LLM Routing (NeurIPS 2025, surrogate regret losses with causal adjustment for the logging policy). Learning *from* logs is therefore started.
- **Still missing**: (a) **off-policy *evaluation*** validated for routers, so that a new router can be ranked from old logs; (b) logged propensities, which production systems rarely record; (c) a public logged dataset; (d) long-horizon settings, where [[replay-gap]] shows replay-based evaluation of agent model switching is unsound and importance weights collapse.
- No public A/B results for learned routers on live traffic were found this session. Practitioner material is guidance only. This supports the claim that academia lacks deployment evidence.
