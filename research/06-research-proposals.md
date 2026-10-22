---
type: index
title: Research proposals P1–P9
---
# Research proposals

Each proposal targets one or more gaps from [[05-gaps-and-agenda]] and is scoped for a small academic team using open-weight models. The proposals are ordered by priority.

---

## P1: HonestRoute, a noise-aware, living router benchmark (G1, G11, G12)
**Hypothesis.** Once labels are multi-sample and artifact-audited, and once a task-type oracle is included, the ranking of routers changes. Most of the claimed instance-level gains then shrink below statistical significance.
**Method.**
1. Pool of about 12 open models spanning sizes and families, plus the reasoning modes of 2–3 hybrid models.
2. k = 8 samples per (query, model) at deployment temperature, giving per-pair success probabilities p̂ rather than 0/1 labels ([[routing-gap-noise]]).
3. Artifact audit: truncation-aware budgets, exact-match plus dual judge ([[unsolvability-ceiling]]).
4. Baselines: best single model, random at matched cost, kNN ([[knn-router]]), **task-type oracle**, **expected oracle** (argmax of p̂ − λc), and the lucky-draw oracle for contrast.
5. Metrics: utility at real prices, *gap recovered beyond task type*, and bootstrap confidence intervals.
6. A living protocol: quarterly pool refresh with versioned price tables, reusing the [[routerarena]] update mechanics.
**Expected contribution.** The reference evaluation protocol for routing papers in 2027.
**Prior art to build on.** DARS (2026) already uses multi-sample plus paraphrase supervision for *training*, and [[routing-gap-noise]] proposes a multi-sample oracle. P1's novelty is the integrated, audited, living *evaluation protocol*.
**Risk.** Compute cost of k samples. Mitigate with adaptive sampling, drawing more samples only where p̂ is uncertain.

## P2: Value-of-information routing, learning what to look at (G2, G7)
**Hypothesis.** A policy that adaptively buys cheap observations before routing beats the query-only plateau at equal total cost.
**Formulation.** Extend [[cascade-routing]] with *observation actions* o ∈ {none, proxy-model prefill activations, target prefill activations, 16/64-token draft from the cheap model, 2-draft agreement, full cheap answer + verifier}. Each has a cost c_o, and the policy maximizes E[U] − Σ c_o. Train with (a) myopic VOI estimates (expected decision improvement from a learned estimator conditioned on the observation) and (b) RL for multi-step acquisition.
**Experiments.** On P1's benchmark: (i) the information value of each signal type, (ii) the Pareto frontier vs. the plateau band ([[routing-plateau]]), and (iii) cross-model transfer, i.e. whether one 1B proxy's activations predict success for *other* pool models ([[prefill-activation-router]]).
**Closest prior art (found in iteration 2).** [[pandora-router]] (NeurIPS 2026) already frames *cheap vs expensive value estimation* as Pandora's Box, with closed-form VOI indices under a Gaussian model. [[llms-encode-failures]] (ICLR 2026) shows pre-generation probes are strong routing signals.
**What is still novel here.** (a) A menu of *heterogeneous* observation types with very different costs and informativeness, rather than one cheap and one expensive estimator. (b) Observations of one model that inform the success of *other* models (cross-model transfer), which breaks Pandora's independence assumption. (c) Multi-step acquisition learned by RL rather than closed-form indices. (d) Evaluation on P1's noise-aware labels. Pandora's Router and probe routers are the baselines to beat.
**Risk.** Observation costs may be hard to compare across hardware. Report both FLOPs and $.

## P3: Off-policy router learning and evaluation from logged feedback (G4, G13)
**Hypothesis.** Routers trained from bandit-feedback logs with doubly-robust off-policy objectives approach full-information routers. Naive training on logs is biased by the logging router.
**Method.**
1. **Simulator**: replay P1's p̂ matrix as an environment. A logging router (e.g. [[routellm]]) chooses a model, and the environment reveals only that model's sampled outcome plus *implicit* signals (retry, abandon, thumbs) generated from a calibrated user model, following [[user-retrials]] and [[user-choice-stackelberg]].
2. Compare IPS, SNIPS, doubly-robust and causal-regret training ([[budgeted-online-routing]], Causal LLM Routing) against full-information training.
3. Study logging-policy design: how much ε-exploration, and how to make exploration safe (explore only among models above a quality floor).
4. Release the simulator plus a logged dataset format, so that labs with production traffic can share logs safely.
**Contribution.** It moves the methodology toward how [[gpt5-router]]-style systems actually learn.

## P4: Session-level routing with real switch economics (G5, G8)
**Re-scoped in iteration 2.** Sequential multi-turn routers already exist ([[dialrouter]], SeqRoute, MTRouter), so this is no longer a first-formulation paper.
**Hypothesis.** Modelling *real* provider cache economics (write/read tiers, TTLs, timing) and continuity costs changes the optimal policy relative to existing sequential routers. Those routers treat a switch as re-billing the history at the input price.
**Method.** An MDP over multi-turn conversations whose state is (history features, current model, cache status). Cost includes re-prefill of the context on switch, using real prompt-caching price discounts. Train with fitted Q-iteration on multi-turn datasets (e.g. MT-Bench-101-style or WildChat-style) with simulated outcomes.
**Measures.** Cost per resolved session, number of switches, and user-model-estimated satisfaction.

## P5: Credit-assigned agentic routing (G6, G9)
**Hypothesis.** Step-level routers trained with counterfactual step replays outperform both trajectory-label routers and fixed tiering.
**Method.** For agent benchmarks (software engineering, web, data analysis), log trajectories with a strong model, then for sampled steps t *replay with a weaker model* and continue, estimating Δsuccess(t) as step-level credit. Train a value model over harness state ([[agentic-routing]]), with escalation triggers on tool errors or loops (a cascade in time). Evaluate against AgentRouter-style tiering ([[agentrouter-agentic]]) and [[router-r1]]. **All evaluation uses live forked re-execution with same-model control forks**, because [[replay-gap]] (2026) shows log-stitching replay mispredicts every success-relevant outcome of model switching on SWE-bench Verified.
**Security add-on.** Measure how a malicious intermediary or rerouting gadget in tool outputs (indirect injection) can manipulate step routing ([[router-security]]).

## P6: One budget, all knobs, a unified compute router (G7)
**Hypothesis.** A shared quality estimator over (model, effort, n samples, aggregation) achieves a better cost–quality frontier than routing each knob separately.
**Method.** Enumerate configurations for 3 hybrid-reasoning models (thinking off / low / high) × n ∈ {1, 3, 5} × {majority, reward-model best-of-n}. Learn q̂(x, config) with configuration embeddings (an IRT-style ability per config, cf. RADAR and [[irt-router]]), and route by utility. Compare against [[best-route]], [[route-to-reason]], [[dart]] and model-only routing. Use a single cost accounting that includes router, verifier and queueing costs, since the 2026 adaptive-computation survey finds most reported savings incomparable without one. Fit "compute-optimal routing" scaling curves.

## P7: Active cold-start profiling with computerized adaptive testing (G3, G10)
**Hypothesis.** Adaptive selection of probe queries (CAT on an IRT model) profiles a new model to a target routing-regret level with about 5–10× fewer probes than random anchors ([[zerorouter]], [[uniroute]]).
**Method.** Fit a multidimensional IRT model on the P1 matrix. For a held-out "new" model, choose probes by maximum Fisher information about the routing *decision* (not about ability), stopping when the regret bound is reached. Extensions: drift detection (sequential tests on live traffic outcomes) and price-shock re-routing with cost as an input feature.

## P8: Certifiably robust, safety-floored routing (G9, G10)
**Hypothesis.** Routers can be made robust to confounder gadgets with bounded cost, and a safety floor (risky intents are never routed below an alignment tier) removes the jailbreak-to-weak-model failure.
**Method.** (i) Adversarial training with gadget search in the loop ([[rerouting-llm-routers]]). (ii) Randomized-smoothing-style certification over token insertions for embedding routers. (iii) Joint router plus guardrail with a constrained objective. (iv) Adaptive attacks against detectors ([[rerouteguard]]). (v) The DSC benchmark ([[dsc-robustness]]) as a safety evaluation, with cost-escalation DoS budgets.

## P9: Verifiable routing disclosure (G13), re-scoped
**Why re-scoped.** [[model-substitution-audit]] (NeurIPS 2025) shows software-only detection of model substitution is unreliable, so a purely black-box audit is unlikely to work.
**Hypothesis.** A routed endpoint can cheaply *prove* which model and effort answered each request, using TEE attestation plus signed per-response routing receipts. Statistical spot-checks then only need to verify the receipts, not infer the model.
**Method.** Design a receipt format (model id, version hash, effort, router decision features), prototype attestation on an open-weight serving stack with [[vllm-semantic-router]] as the router, and measure overhead. Threat model: dishonest providers ([[gpt5-router]], [[azure-model-router]]) and malicious intermediaries (*Your Agent Is Mine*: 9 of 428 measured routers injected code; see [[router-security]]).

---

## Suggested sequencing
1. **P1 first.** It produces the data substrate, a multi-sample matrix, that P2, P3, P6 and P7 all reuse.
2. Then **P2 and P3** in parallel. They are the two main levers and give the highest publication value.
3. **P7 and P8** are cheap, self-contained follow-ups. **P5 and P4** need more infrastructure. **P9** is a policy-facing side project.
