---
type: paper
title: DialRouter — sequential multi-turn routing (2026)
sources: [zhang2026dialrouter, mtrouter2026, seqroute2026, swrouter2026]
---
# From Myopic Selection to Long-Horizon Awareness: Sequential LLM Routing for Multi-Turn Dialogue
Zhang et al., arXiv:2604.12385 (Apr 2026). Category: [[personalized-routing]], [[gap-session-level-routing]].

**Idea.** Per-turn routers are *myopic*. DialRouter runs **MCTS** over dialogue branches created by different model choices, keeps high-reward trajectories, and distils them into a lightweight policy with retrieval-based future-state approximation, so no search is needed at inference. A cost-aware reward trades quality for cost.
**Siblings (2026).** SeqRoute (finite-horizon MDP, offline RL under a global budget); MTRouter (history–model joint embeddings, and notes that switching models breaks prompt caching); SWRouter (similarity-contractive windows).
**What remains open.** Simulated users and rewards; switch costs modelled as re-billing input rather than measured provider cache economics; style and persona continuity; real-user validation. See [[gap-session-level-routing]].
