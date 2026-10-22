---
type: paper
title: Arch-Router (2025) + archgw
sources: [tran2025archrouter]
---
# Arch-Router: Aligning LLM Routing with Human Preferences
Tran et al. (Katanemo), arXiv:2506.16655. Model: `katanemo/Arch-Router-1.5B`. Category: [[representation-matching-routers]], [[personalized-routing]].

**Idea.** Don't predict quality. Let operators write **preference policies** as `(domain, action) → model` in natural language. A 1.5B generative model maps each conversation to a policy. New models are added by editing policies, with no retraining.
**Evidence (vendor-reported).** State-of-the-art policy-matching accuracy on conversational data vs larger proprietary LLMs; ~50 ms p50 / <75 ms p99 routing latency. It is integrated in the Arch (archgw) AI gateway and was reportedly adopted for Hugging Face's chat routing.
**Significance.** It reframes routing as *alignment with user intent* rather than benchmark accuracy, which matters for [[gap-transparency-and-control]].
**Limits.** It routes by topic, so it is blind to difficulty, and it inherits the quality of the policy author's judgement.
