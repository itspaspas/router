---
type: concept
title: Reasoning-effort and test-time-compute routing
sources: [su2025cprouter, radar2025, thinkwhenneeded2026, dart2026, ding2025bestroute, routereason2025, difficulty2025, openai2025gpt5, dmr2026]
---
# Reasoning-effort routing

Since 2025, frontier models have exposed *effort knobs* (thinking on/off, thinking budgets, reasoning-effort levels). The routing action space is now **model × effort × number of samples**, not just "model".

- **Model ↔ reasoning model**: CP-Router uses conformal sets to choose LLM vs. LRM; GPT-5's production router chooses between main and thinking variants ([[gpt5-router]]).
- **Think or not (same model)**: Think When Needed (SIGIR 2026); probe-based "pre-decisional" reasoning gates; [[dart]], which is training-free and decides via no-think draft agreement.
- **Budget-aware IRT**: RADAR treats (model, budget) pairs as respondents in an IRT model.
- **Samples as a dimension**: [[best-route]] routes jointly over model and best-of-n (up to 60% cost cut, <1% drop).
- **Strategy as a dimension**: [[route-to-reason]] routes jointly over model and reasoning strategy (>60% token cut).
- **Output length as a dimension**: R2-Router (ICML 2026) routes over (LLM, length budget).
- **Precision as a dimension**: DMR routes across quantization levels of one model.
- **Step-level effort in agents**: per-step high/medium/low effort selection ([[agentic-routing]]).

**Gap.** No unified "compute router" jointly allocates model, effort, samples, retrieval and tools under one budget with a shared quality estimator ([[gap-unified-compute-allocation]]).
