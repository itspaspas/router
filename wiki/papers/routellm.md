---
type: paper
title: RouteLLM (paper + framework)
sources: [ong2024routellm]
---
# RouteLLM: Learning to Route LLMs with Preference Data
Ong et al. (LMSYS / UC Berkeley), arXiv:2406.18665, ICLR 2025. Category: [[predictive-routers]]; also an open-source framework ([[industry-landscape]]).

**Idea.** Strong-vs-weak binary routing trained on Chatbot Arena pairwise preferences, augmented with LLM-judge labels and golden-labelled data. Four routers: similarity-weighted (SW) Elo ranking, matrix factorization, BERT classifier, and causal-LLM classifier.
**Evidence.** The project reports cost savings vs GPT-4-only of >85% on MT-Bench and ≈35% on GSM8K at matched quality, with routers transferring to other strong/weak pairs.
**Framework.** `routellm` ships an OpenAI-compatible server and an evaluation harness, and is widely used as a baseline.
**Limits.** Binary only. Preference data reflects Arena's query distribution. LLMRouterBench and per-step agent studies show it is matched by simple baselines and gives smaller savings per step ([[llmrouterbench]], [[agentrouter-agentic]]).
