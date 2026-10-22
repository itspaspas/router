---
type: paper
title: How Robust Are Router-LLMs? (DSC, EACL 2026)
sources: [kassem2025robust]
---
# How Robust Are Router-LLMs? Analysis of the Fragility of LLM Routing Capabilities
Kassem, Schölkopf, Jin, arXiv:2504.07113, EACL 2026. Category: [[router-security]], [[router-evaluation]].

**Benchmark.** DSC (Diverse, Simple, Categorized) covers coding, translation, math, instruction following, general knowledge and jailbreaking, plus privacy and safety checks.
**Findings.** Across three preference-trained routers and two commercial routers, routing is *category-driven*. A BERT router sends all coding and math to the strongest model regardless of difficulty, and sends **jailbreak attempts to weaker models**, which raises safety risk.
**Lesson.** Routers must be evaluated on safety outcomes, not only cost and accuracy ([[gap-adversarial-robustness]]).
