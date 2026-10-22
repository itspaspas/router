---
type: concept
title: Token- and segment-level routing
sources: [relayllm2026, roro2026, leviathan2023spec, shen2024coll, zheng2025citer, fu2025r2r, fusionroute2026, steer2026, narasimhan2024fastcascade]
---
# Token- and segment-level routing

Most tokens in a response are easy, and a few *critical* tokens decide correctness. Routing per token or per reasoning step lets a small model write most of the text.

- **Speculative decoding** (Leviathan et al. 2023): a lossless small→large collaboration, the systems ancestor of this line.
- **Co-LLM** (ACL 2024): a latent variable decides which model emits each token.
- **CITER** ([[citer]]): an RL-trained token router between an SLM and an LLM, with reward = quality − cost.
- **R2R** ([[r2r]], NeurIPS 2025): routes only *path-divergent* tokens to the large reasoning model.
- **STEER** (AAAI 2026): confidence-guided *step-level* routing in reasoning chains.
- **RelayLLM** (2026): the *small* model is the controller and emits a command token to borrow the large model for a few tokens. The large model writes only ~1.07% of tokens.
- **FusionRoute** (ICML 2026): picks an expert per step *and* adds a corrective logit. It proves expert-only token routing cannot reach the optimal policy without coverage assumptions.
- **STEER follow-ups**: RoRo (2026) replaces per-step confidence with trajectory-aware process rewards.
- **Faster Cascades** ([[cascades]]): deferral rules executed speculatively.

**Open issues.** Tokenizer mismatch across model families; KV-cache handoff cost; the absence of a cross-granularity benchmark; and almost no work on routing across *providers* at token level, because API boundaries prevent it ([[gap-serving-coupling]]).
