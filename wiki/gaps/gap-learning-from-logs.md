---
type: gap
title: G4 Learning and evaluating from production logs
sources: [tsiourvas2025causal, bae2026retrials, openai2025gpt5, panda2025pilot]
---
# G4: Off-policy learning and evaluation for routers is almost absent

**Evidence.** Production routers learn from logged signals: switches, preferences and correctness for [[gpt5-router]], retrials in [[user-retrials]]. Academic routers almost all train on *full-information* benchmark matrices (every model answered every query). Causal LLM Routing (NeurIPS 2025) is one of the few that treats logs as *observational* data. Agentic routing logs are proposed as a flywheel ([[agentic-routing]]).

**Why it matters.** In deployment you only see the outcome of the model you chose (bandit feedback). Logs are confounded by the old router, and feedback is implicit, delayed and noisy.

**What is missing.** (1) Off-policy evaluation (IPS/doubly-robust) estimators validated for routing. (2) Logging-policy design (exploration rates that are safe and cheap). (3) Calibrated mappings from implicit signals (retry, edit, thumbs, abandonment) to utility. (4) A public **logged-bandit routing dataset**. (5) Counterfactual benchmarks that let academics test log-learning without a production system.

**Proposal.** P3 in [[06-research-proposals]].
