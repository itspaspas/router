---
type: paper
title: Zooter (NAACL 2024)
sources: [lu2023zooter]
---
# Routing to the Expert: Efficient Reward-guided Ensemble of LLMs (Zooter)
Lu et al., arXiv:2311.08692, NAACL 2024. Category: [[predictive-routers]].

**Idea.** Score every candidate's answer with a reward model offline, then *distil* the normalized rewards into a lightweight router that sees only the query. It adds tag-based label enhancement to reduce reward noise.
**Significance.** An early demonstration that reward models can supervise routers, so no gold labels are needed. Its weakness is that it inherits reward-model biases.
