---
type: concept
title: Agentic (step-level) routing
sources: [skillorch2026, agentrouter2026icml, agenticrouting2026, masrouter2025, budgetagentic2026, xrouter2025, agentselect2026, lqm2026, youragent2026]
---
# Agentic routing

In agent loops (plan → tool call → observe → …), the unit of routing is a **step**. Errors compound, steps differ hugely in difficulty, and per-step costs dominate total spend.

- **AgentRouter** ([[agentrouter-agentic]], ICML 2026 WS): a 12M-parameter classifier maps each step to one of four model tiers. Reported: −72% cost, <3% task-completion drop vs frontier-only, against −31% (RouteLLM) and −44% (FrugalGPT) when those are applied per step.
- **Agentic Routing: the harness-native data flywheel** (2026): routes from the full harness state, choosing a single model (cost regime) or a complementary set (accuracy regime). The execution logs become router training data.
- **Budget-Aware Agentic Routing via Boundary-Guided Training** (2026); latency-quality routing for tools (LQM-ContextRoute); AgentSelect benchmark.
- Multi-agent: MasRouter ([[collaborative-routing]]).

**Gaps** ([[gap-agentic-credit-assignment]]): credit assignment of a final outcome to step-level routing choices; switching cost (context re-prefill); safety, since a malicious router or intermediary can hijack agents (*Your Agent Is Mine*, CCS 2026; see [[router-security]]); and few standard agent-routing benchmarks.

**Evaluation warning.** [[replay-gap]] (2026) shows that log-replay evaluation of per-step model switching on SWE-bench Verified mispredicts every success-relevant outcome. Agent-routing results that rely on spliced logs should be treated as unverified.

**Skill-based routing.** SkillOrchestra (NeurIPS 2026) learns per-agent competence and cost per *skill* from execution experience instead of end-to-end RL. It reports that RL orchestrators collapse in multi-turn settings, and claims 700× lower learning cost than Router-R1. AgentSelect (ICML 2026) benchmarks query → agent-configuration (backbone + toolkit) recommendation over 108K configurations.
