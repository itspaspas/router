---
type: paper
title: FlexRouter — complementary model sets (COLM 2026)
sources: [flexrouter2026, mohammadshahi2024routoo, li2026llmrouterbench]
---
# FlexRouter: Learning Complementary Model Sets for Flexible LLM Routing
Adobe Research, COLM 2026. Category: [[gap-pool-design]], [[collaborative-routing]].

**Idea.** Route to a *subset* chosen by a **determinantal point process** that balances competence and redundancy, maximizing the probability that at least one selected model answers correctly. Greedy selection sets the subset size adaptively.
**Context.** LLMRouterBench suggests future work should pick complementary small sets via coverage or diversity ([[llmrouterbench]]). Routoo's "universe constructor" also pre-selects a complementary subset.
**What remains.** Per-query set routing is not the same as *deployment-time pool design* under hosting constraints. A theory of when adding a model helps a realistic (non-oracle) router is still missing.
