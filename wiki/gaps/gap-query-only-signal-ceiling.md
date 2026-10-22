---
type: gap
title: G2 Query-only signal ceiling
sources: [lu2026plateau, dekoninck2024unified, nvidia2026prefill, dart2026]
---
# G2: Query-only routers have hit an information ceiling

**Evidence.** The plateau persists with more data and bigger encoders ([[routing-plateau]]). The estimator is the bottleneck ([[unified-routing-cascading]]). Instance-specific wins (the 1–3 models that solve a hard query) are invisible from the prompt alone ([[llmrouterbench]] recall failures).

**What is missing.** A principled **value-of-information router** that decides *what to observe before deciding*: nothing (route now), small-model prefill activations ([[prefill-activation-router]]), k-token drafts and their agreement ([[dart]]), a full cheap answer plus verifier ([[cascades]]), or a probe of a candidate. Each observation has a cost, and the policy should buy one only when its expected decision improvement exceeds that cost. [[cascade-routing]] gives the formal frame, but nobody has trained a policy over *observation actions* across heterogeneous signal types.

**Sub-questions.** Are proxy-model activations predictive of *other* models' success (cross-model transfer of difficulty)? How much does a 16-token draft reveal? Can KV-cache reuse make observations nearly free ([[gap-serving-coupling]])?

**Proposal.** P2 in [[06-research-proposals]].
