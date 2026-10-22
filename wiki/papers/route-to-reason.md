---
type: paper
title: Route to Reason (2025)
sources: [pan2025rtr]
---
# Route to Reason: Adaptive Routing for LLM and Reasoning Strategy Selection
arXiv:2505.19435 (May 2025). Category: [[reasoning-effort-routing]].

**Idea.** Jointly select *(model, reasoning strategy)*, e.g. CoT, direct answer, or program-aided, by learning representations of both and predicting accuracy and token cost for every pair. It then picks the best pair under a budget.
**Evidence (authors).** Higher accuracy than the best single model with >60% fewer tokens.
**Relation to G7.** Together with [[best-route]] (model × samples) and RADAR (model × budget), this covers *two* knobs at a time. A single policy over model × effort × samples × aggregation is still missing ([[gap-unified-compute-allocation]]).
