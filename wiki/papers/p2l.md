---
type: paper
title: Prompt-to-Leaderboard (ICML 2025)
sources: [frick2025p2l]
---
# Prompt-to-Leaderboard (P2L)
Frick et al. (LMArena), arXiv:2502.14855, ICML 2025. Category: [[predictive-routers]].

**Idea.** An LLM takes a prompt and outputs a *Bradley–Terry coefficient vector* over all models: a prompt-specific leaderboard trained on Arena votes. Routing is the argmax (or a cost-aware variant).
**Significance.** It unifies evaluation and routing, scales with Arena data, and handles many models at once. It inherits preference-data biases (style, length) and needs Arena-like traffic to train.
