---
type: system
title: LLMRouter library + xRouteBench (UIUC, 2026)
sources: [llmrouterlib2026]
---
# LLMRouter: Unified Infrastructure for Developing, Evaluating, and Deploying LLM Routers
ulab-uiuc/LLMRouter (MIT; `pip install llmrouter-lib`); paper arXiv:2608.06867 (Aug 2026). Locus: open-source research toolkit ([[industry-landscape]], [[router-evaluation]]).

- 16+ routers behind one `MetaRouter` interface: kNN, SVM, MLP, BERT-based, graph ([[graphrouter]]), personalized ([[personalizedrouter]]), and multi-round RL ([[router-r1]]). Includes data generation, training, inference, evaluation and a CLI.
- **xRouteBench**: 5 scenarios covering generic QA/math/code, long-context memory, vision, time-series and personalization.
- Reported: learned routers beat the strongest fixed model by 14.6% (relative), and **no single router wins across tasks and budgets**.
