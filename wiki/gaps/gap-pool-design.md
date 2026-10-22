---
type: gap
title: G11 Pool design and complementarity
sources: [li2026llmrouterbench, huang2025routereval, modelglue2024, flexrouter2026, mohammadshahi2024routoo]
---
# G11: Which models should be in the pool at all?

**Evidence.** LLMRouterBench: curation beats size; larger ensembles give diminishing returns ([[llmrouterbench]]). RouterEval: model-level scaling-up with candidate count ([[routereval]]). Model-GLUE compares merging, mixing and routing over model zoos. These are partly contradictory and lack theory.

**What is missing.** Pool selection as an optimization problem: choose a subset maximizing *complementarity* (low error correlation, distinct "specialist advantage" per [[routing-gap-noise]]) subject to hosting and cost constraints. Submodular selection, a theory of when adding a model helps a *realistic* router (not the oracle), and the interaction with training specialist models *for* routing (co-design of experts and router, like MoE but across separately trained models; see [[routing-vs-moe]]).

## Prior art and counter-evidence (iteration 2)
[[flexrouter]] (COLM 2026) selects complementary model *sets* per query with DPPs, Routoo pre-selects a complementary "universe", and LLMRouterBench found top-by-average-accuracy subsets work best among simple heuristics. Per-query set selection is therefore addressed. **Deployment-time pool design** under hosting and cost constraints, and its theory for non-oracle routers, remains open.
