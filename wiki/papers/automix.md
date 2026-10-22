---
type: paper
title: AutoMix (NeurIPS 2024)
sources: [madaan2023automix]
---
# AutoMix: Automatically Mixing Language Models
Madaan et al., arXiv:2310.12963, NeurIPS 2024. Category: [[cascades]].

**Idea.** The small model answers, then *verifies itself* few-shot (entailment against context). A POMDP-based meta-verifier turns these noisy self-verification signals into an escalate/stop decision.
**Why it matters.** It showed that cheap self-assessment is enough to drive a cascade with no trained scorer. It became the ancestor of the confidence-token and self-routing lines (Self-REF, SATER, DiSRouter).
**Limits.** Self-verification is weak when the small model is confidently wrong. It was evaluated mainly on context-grounded QA.
