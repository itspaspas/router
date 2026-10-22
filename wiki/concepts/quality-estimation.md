---
type: concept
title: Quality estimation signals for routing
sources: [dekoninck2024unified, nvidia2026prefill, lu2026plateau, dart2026, chuang2024selfref, gupta2024cascade]
---
# Quality estimation: what the router gets to see

Dekoninck et al. show the estimator, not the policy, is the bottleneck ([[unified-routing-cascading]]). The available signals, ordered by cost:

| Signal | Cost | Examples |
|---|---|---|
| Query text features or sentence embedding | ~0 | most routers; [[knn-router]] |
| Task / domain tag | ~0 | [[arch-router]], TagRouter |
| Small model's *internal* state on the prompt (prefill) | one forward pass of a small model | NVIDIA prefill-activation router (2026), probe-based reasoning routers |
| Linear probe on a candidate's pre-generation activations | prefill of that candidate | [[llms-encode-failures]] (ICLR 2026): beats best single model, up to 70% cost cut on MATH |
| Target model's own prefill activations | prefill of the target (often reused via KV cache) | [[prefill-activation-router]] |
| Short draft(s) | a few dozen decode tokens | DART draft agreement ([[dart]]) |
| Full cheap answer + verifier | full cheap generation | [[cascades]] |
| Trained confidence tokens / self-assessment | fine-tuning | Self-REF, SATER, DiSRouter |

The [[routing-plateau]] finding says the top row is saturated. The research opportunity is the *middle rows*: cheap partial observations chosen adaptively ([[cascade-routing]], [[gap-query-only-signal-ceiling]]).

**Choosing which signal to buy.** [[pandora-router]] (NeurIPS 2026) formalizes the cheap-vs-expensive estimator choice as Pandora's Box with closed-form value-of-information indices. That is the first principled treatment of *when to pay for a better estimate*.
