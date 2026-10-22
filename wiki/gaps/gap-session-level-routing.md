---
type: gap
title: G5 Session- and conversation-level routing
sources: [gmtrouter2025, openai2025gpt5, mahmood2026userchoice]
---
# G5: Routing is studied per query, but users live in sessions

**Evidence.** Nearly all benchmarks are single-turn ([[router-evaluation]]). GMTRouter models multi-turn *preferences* but not switching dynamics. GPT-5's router switches models mid-conversation, and users noticed ([[gpt5-router]]).

**What is missing.** A formulation as an MDP with **switching costs**: losing the prompt/KV cache (re-prefill of a long context on a new model), style and persona discontinuity, and tool-state transfer. Also missing are the *option value* of starting cheap and escalating later in the session, and routing on *conversation trajectory* features (frustration, repeated corrections). Prompt-caching price discounts make "stickiness" economically significant and create an interesting interaction with [[serving-aware-routing]].

**Proposal.** P4 in [[06-research-proposals]].
