---
type: paper
title: Routing with prefill activations (NVIDIA, 2026)
sources: [nvidia2026prefill]
---
# LLM Router: Rethinking Routing with Prefill Activations
NVIDIA, arXiv:2603.20895 (Mar 2026). Category: [[quality-estimation]].

**Idea.** Replace semantic sentence embeddings with **internal activations from the prefill pass** as router features. Prefill is computed anyway and reveals what the model "makes of" the prompt.
**Why it matters.** It is one of the first concrete moves past the query-embedding ceiling identified by [[routing-plateau]]. It connects to probe-based reasoning gates ([[reasoning-effort-routing]]).
**Open.** Prefill activations are only available for white-box or self-hosted models, so this does not work for closed APIs. The open question is which model's activations to use (a proxy vs. the target) ([[gap-query-only-signal-ceiling]]).
