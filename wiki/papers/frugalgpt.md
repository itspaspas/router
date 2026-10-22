---
type: paper
title: FrugalGPT (2023)
sources: [chen2023frugalgpt]
---
# FrugalGPT: How to Use LLMs While Reducing Cost and Improving Performance
Chen, Zaharia, Zou, arXiv:2305.05176 (TMLR 2024). Category: [[cascades]].

**Idea.** An LLM cascade: query APIs in a learned order and stop when a learned scorer (a small DistilBERT-style regressor over query+answer) judges the answer reliable. The paper also proposes prompt adaptation and LLM approximation (caching or fine-tuning a cheaper model).
**Evidence.** Reported up to ~98% cost reduction at GPT-4 quality, or better quality at equal cost, on several classification/QA datasets of the era.
**Legacy.** It set up the cost–quality framing every router since inherits. It is the standard "cascade" baseline in [[routerwise]] and [[agentrouter-agentic]].
**Limits.** The scorer needs labelled per-task data, and the evaluation was on short-answer tasks. Every query pays for the first model, which overloads the cheap model's queue under load ([[serving-aware-routing]]).
