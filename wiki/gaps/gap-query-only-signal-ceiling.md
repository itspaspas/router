---
type: gap
title: G2 Query-only signal ceiling
sources: [lu2026plateau, dekoninck2024unified, nvidia2026prefill, dart2026, fisch2026pandora, lugoloobi2026encode, relope2026, adaptivecomp2026]
---
# G2: Query-only routers have hit an information ceiling

**Evidence.** The plateau persists with more data and bigger encoders ([[routing-plateau]]). The estimator is the bottleneck ([[unified-routing-cascading]]). Instance-specific wins (the 1–3 models that solve a hard query) are invisible from the prompt alone ([[llmrouterbench]] recall failures).

**What is missing.** A principled **value-of-information router** that decides *what to observe before deciding*: nothing (route now), small-model prefill activations ([[prefill-activation-router]]), k-token drafts and their agreement ([[dart]]), a full cheap answer plus verifier ([[cascades]]), or a probe of a candidate. Each observation has a cost, and the policy should buy one only when its expected decision improvement exceeds that cost. [[cascade-routing]] gives the formal frame, but nobody has trained a policy over *observation actions* across heterogeneous signal types.

**Sub-questions.** Are proxy-model activations predictive of *other* models' success (cross-model transfer of difficulty)? How much does a 16-token draft reveal? Can KV-cache reuse make observations nearly free ([[gap-serving-coupling]])?

**Proposal.** P2 in [[06-research-proposals]].

## Prior art and counter-evidence (iteration 2)
- **VOI routing already exists in a two-level form.** [[pandora-router]] (NeurIPS 2026) casts costly value estimation as Pandora's Box, with closed-form VOI indices deciding when to call an expensive estimator. It matches exhaustive estimation with far fewer expensive calls. The gap is therefore *narrower* than first stated. What remains open is a policy over **many heterogeneous observation types** (activations, k-token drafts, full answers, probes of other models), correlated non-Gaussian signals, and multi-step acquisition.
- **Pre-generation probes work.** [[llms-encode-failures]] (ICLR 2026) shows linear probes on pre-generation activations predict success, beat the best single model, and save up to 70% on MATH. This supports the thesis that the needed signal is inside the model. Probes degrade on image queries (ReLope, 2026).
- **Survey confirmation.** The 2026 adaptive-computation survey concludes that adaptive policies are credible only when the decision signal is much cheaper than the action it avoids and is calibrated near the deployment threshold. That is exactly the VOI condition.
