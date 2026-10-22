---
type: concept
title: Collaborative and multi-round routing
sources: [jiang2023blender, wang2024moa, zhang2025routerr1, xrouter2025, masrouter2025, feng2025swarms, mot2025, avengers2025, fusionroute2026, lightrouter2025]
---
# Collaborative routing

Instead of choosing *one* model, a router composes several.

- **Generate-all, then rank/fuse**: LLM-Blender, Mixture-of-Agents. These give a high quality ceiling at a high cost and set the upper bound that routers try to approach cheaply.
- **Route-then-ensemble**: the Avengers (cluster routing plus voting among small open models), LightRouter.
- **LLM-as-router with multi-round calls**: [[router-r1]] (NeurIPS 2025) trains a policy LLM with RL to interleave *think* and *route* actions and aggregate answers, using a cost reward. xRouter trains a tool-calling orchestrator to answer itself or delegate.
- **Routing inside multi-agent systems**: MasRouter routes collaboration mode, roles and LLM per agent. Heterogeneous Swarms jointly optimizes roles and weights.
- **Latent/representation-level fusion**: Mixture of Thoughts (ICLR 2026), FusionRoute.
- **Finer granularity**: [[token-level-routing]], [[agentic-routing]].

**Tension.** Composition raises the ceiling *above* the single-model oracle that most routing benchmarks use, so benchmarks built on "pick one" understate what is possible ([[router-evaluation]]).
