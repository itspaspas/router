---
type: gap
title: G6 Agentic routing and credit assignment
sources: [agentrouter2026icml, agenticrouting2026, zhang2025routerr1, masrouter2025, budgetagentic2026]
---
# G6: Step-level routing for agents lacks credit assignment and benchmarks

**Evidence.** Early results are promising: per-step routing reportedly cuts cost ~72% ([[agentrouter-agentic]]), and harness-native flywheels ([[agentic-routing]]) and RL routers ([[router-r1]]) exist. But labels are *trajectory-level* (task success), while decisions are *step-level*.

**What is missing.**
- **Credit assignment**: which step's downgrade caused a failure? This calls for counterfactual replays (re-run step t with the strong model) and learned value functions over harness state.
- **Error-recovery-aware routing**: escalate after a tool error or a loop is detected (a cascade in time).
- **Benchmarks**: standard agent-routing suites with logged per-step counterfactuals (SWE-style, browsing, data analysis).
- **Security**: routers and gateways in agent loops are man-in-the-middle points (*Your Agent Is Mine*, [[router-security]]).
- **Joint routing of model and tool** (latency-quality routing for tools exists but is narrow).
