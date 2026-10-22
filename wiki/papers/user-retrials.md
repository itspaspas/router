---
type: paper
title: Learning to Route and Schedule from User Retrials (2026)
sources: [bae2026retrials]
---
# Learning to Route and Schedule LLMs from User Retrials via Contextual Queueing Bandits
Bae, Son, Lee, arXiv:2602.02061 (Feb 2026). Category: [[budgeted-online-routing]].

**Idea.** Treat routing *and* scheduling as one online learning problem. Use **implicit feedback** (a user retrying a query signals dissatisfaction) via contextual queueing bandits with multinomial-logit feedback.
**Significance.** It is a rare paper learning from the signals production systems actually log, rather than benchmark labels. It is a seed for [[gap-learning-from-logs]].
