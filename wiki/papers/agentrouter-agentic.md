---
type: paper
title: AgentRouter — per-step agent routing (ICML 2026 WS)
sources: [agentrouter2026icml]
---
# AgentRouter: Heterogeneous Model Routing for Cost-Optimal Multi-Step Agentic Workflows
ICML 2026 AdaptFM workshop. Category: [[agentic-routing]].

**Idea.** Treat per-step model choice in an agent trajectory as sequential assignment. A 12M-parameter classifier (<5 ms per step) maps each step to one of four model tiers.
**Evidence (authors, 2,400 held-out trajectories).** −72% cost vs frontier-only with <3% end-to-end completion drop. Per-step [[routellm]] gives −31% and [[frugalgpt]] −44%.
**Caveat.** Workshop paper with self-reported baselines. The note "AgentRouter (2510.05445)" in the catalog is a *different* paper with the same name.
