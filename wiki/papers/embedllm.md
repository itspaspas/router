---
type: paper
title: EmbedLLM (ICLR 2025)
sources: [zhuang2024embedllm]
---
# EmbedLLM: Learning Compact Representations of Large Language Models
Zhuang et al., arXiv:2410.02223, ICLR 2025. Category: [[cold-start-and-model-representation]].

**Idea.** Learn one compact vector per LLM with an encoder–decoder over a large model×question correctness matrix. The vectors predict correctness, which enables routing, and they reveal model similarity.
**Significance.** The canonical "model embedding" paper. It is a building block for routing that scales to many models.
**Critique.** Shown to exhibit routing collapse ([[routing-collapse]]).
