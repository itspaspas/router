---
type: paper
title: LLMs Encode Their Failures (ICLR 2026)
sources: [lugoloobi2026encode]
---
# LLMs Encode Their Failures: Predicting Success from Pre-Generation Activations
Lugoloobi, Foster, Bankes, Russell, arXiv:2602.09924, ICLR 2026. Code: KabakaWilliam/llms_know_difficulty. Category: [[quality-estimation]].

**Finding.** Linear probes on activations taken *before generation* predict whether the model will succeed under a given decoding policy (math, code), beating surface features. Models have a **model-specific notion of difficulty** that diverges from human difficulty (E2H-AMC), and the divergence grows with extended reasoning.
**Routing.** Probe-guided routing beats the best single model, with up to 70% cost reduction on MATH (and a 40% figure in another setting). Probe reliability, not routing sophistication, is the bottleneck.
**Significance.** It is strong evidence for the signal-ceiling thesis: the information a router needs is in the model's own state, not the query text ([[prefill-activation-router]], [[gap-query-only-signal-ceiling]]). Open: probes need white-box access, and ReLope (2026) shows probes degrade on image queries ([[multimodal-routing]]).
