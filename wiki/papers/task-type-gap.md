---
type: paper
title: Most of the LLM Routing Gap Is Task Type (2026)
sources: [lee2026tasktype]
---
# Most of the LLM Routing Gap Is Task Type
Janghoon Lee, arXiv:2608.23023 (Aug 2026). Category: [[oracle-gap]].

**Question.** Different router designs land within a fraction of a point of each other and far below the oracle, so *what is the gap made of*, in coordinates a policy could condition on? Prior decompositions by difficulty find the hardest 11–35% of queries carry 70–91% of the gap.
**Claim (title-level; full results not verified here).** Most of the recoverable gap aligns with *task type*.
**Implication.** If true, a large part of the "learned routing" value is achievable with a task classifier plus per-task best model, which is roughly what [[arch-router]] and semantic routers do. Papers should report a **task-type oracle** baseline ([[gap-evaluation-validity]]).
