---
type: paper
title: Unsolvability Ceiling is an evaluation artifact (2026)
sources: [garg2026unsolvability]
---
# Unsolvability Ceiling in Multi-LLM Routing: An Empirical Study of Evaluation Artifacts
Garg & Sagtani, arXiv:2605.07395 (May 2026). Category: [[oracle-gap]], [[decision-aware-training]].

**Setup.** ~206K query–model pairs across MMLU, MedQA, HumanEval, MBPP, Alpaca and ShareGPT with Gemma 4 and Llama 3.1 families, judged by an LLM judge and exact match.
**Findings.** Much "unsolvable" mass is artifact: truncation under fixed generation budgets (65% of MMLU, 57% of MedQA cases), judge bias toward verbosity, and 5–12% parse failures. Standard routers collapse to *majority-class* prediction (~79% smallest-tier optimal), confirmed by random-feature and shuffled-label controls, which costs 13–17 pp.
**Recommendations.** Dual-judge validation, exact-match anchoring, truncation-aware budgets, cost-sensitive training ([[gap-evaluation-validity]]).
