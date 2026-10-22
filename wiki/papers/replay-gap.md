---
type: paper
title: The Replay Gap (2026)
sources: [gonuguntla2026replay]
---
# The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World
Ashritha Gonuguntla, arXiv:2608.08239 (Aug 2026). Category: [[agentic-routing]], [[router-evaluation]].

**Problem.** Per-step agent routers are usually evaluated by *replaying logs* and splicing in another model's recorded output, which assumes the rest of the trajectory is unchanged.
**Method.** Fork live trajectories, re-execute the prefix in a fresh container, continue with a different model, and pair every swap with a same-model control fork.
**Findings (SWE-bench Verified).** Swaps change ~61–94% of post-fork actions beyond control noise. All outcome flips occur in swap arms (0 of 359 controls). A log-stitching replay evaluator **mispredicts every success-relevant outcome**. A stronger model sometimes exhausts tight step budgets (a "thoroughness tax"). Even same-model temperature-0 forks diverge on some serving stacks.
**Implication.** Offline, log-replay evaluation of step-level routers is unsound, so agent-routing claims, including our P5 design, require live counterfactual forks ([[gap-agentic-credit-assignment]], [[gap-evaluation-validity]]). It also undermines naive off-policy evaluation over long horizons ([[gap-learning-from-logs]]).
