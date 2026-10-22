---
type: gap
title: G5 Session- and conversation-level routing
sources: [zhang2026dialrouter, mtrouter2026, seqroute2026, gmtrouter2025, openai2025gpt5, mahmood2026userchoice]
---
# G5: Session-level routing is emerging (2026) but rests on simulated sessions

**Revised in iteration 2.** The first draft called this area "unstudied". That was wrong. In 2026 several papers model multi-turn routing as sequential decision-making: [[dialrouter]] (MCTS, then a distilled policy), SeqRoute (finite-horizon MDP, offline RL under a global budget), MTRouter (history–model joint embeddings, explicitly noting that switching breaks prompt caching) and SWRouter. GMTRouter models multi-turn *preferences*.

**What is still missing.**
1. **Real switch economics.** Papers model switch cost as re-billing the history at the input price. Real providers have cache write/read tiers, cache TTLs and per-provider KV reuse, so the true switch cost depends on timing and cache state ([[serving-aware-routing]]).
2. **Real users.** Rewards come from LLM judges or simulated users. No public dataset logs *routed* sessions with outcomes. GPT-5's router is the only large-scale deployment, and its data is private ([[gpt5-router]], [[gap-learning-from-logs]]).
3. **Continuity costs beyond money**: style, persona and memory inconsistency after a switch, which users notice (GPT-5 backlash).
4. **Trajectory signals.** Frustration, repeated corrections and abandonment as routing features. These are linked to the user-choice game ([[user-choice-stackelberg]]).

**Proposal.** P4 in [[06-research-proposals]] is re-scoped to these four points.
