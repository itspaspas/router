---
type: gap
title: G6 Agentic routing and credit assignment
sources: [agentrouter2026icml, agenticrouting2026, zhang2025routerr1, masrouter2025, budgetagentic2026, gonuguntla2026replay, xrouter2025]
---
# G6: Step-level routing for agents lacks credit assignment and benchmarks

**Evidence.** Early results are promising: per-step routing reportedly cuts cost ~72% ([[agentrouter-agentic]]), and harness-native flywheels ([[agentic-routing]]) and RL routers ([[router-r1]]) exist. But labels are *trajectory-level* (task success), while decisions are *step-level*.

**What is missing.**
- **Credit assignment**: which step's downgrade caused a failure? This calls for counterfactual replays (re-run step t with the strong model) and learned value functions over harness state.
- **Error-recovery-aware routing**: escalate after a tool error or a loop is detected (a cascade in time).
- **Benchmarks**: standard agent-routing suites with logged per-step counterfactuals (SWE-style, browsing, data analysis).
- **Security**: routers and gateways in agent loops are man-in-the-middle points (*Your Agent Is Mine*, [[router-security]]).
- **Joint routing of model and tool** (latency-quality routing for tools exists but is narrow).

## Prior art and counter-evidence (iteration 2)
- **[[replay-gap]]** (2026) shows that log-stitching replay evaluation of per-step model switching *mispredicts every success-relevant outcome* on SWE-bench Verified. Swaps change 61–94% of later actions, and stronger models can pay a "thoroughness tax" under tight step budgets. Credible agent-routing evaluation therefore needs **live forked re-execution with same-model controls**. That is expensive but necessary, and it is now the design basis for P5.
- MasRouter (ACL 2025) adds collaboration-mode and role routing, with up to 52% cost cut on HumanEval (authors). xRouter (Salesforce, 2025) reports that small open models struggle to learn orchestration via RL. That is a capacity floor for LLM-as-router designs.
