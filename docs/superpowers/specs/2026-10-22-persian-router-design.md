# Design spec: Persian-first LLM router (production system + research study)

- **Date:** 2026-10-22
- **Status:** approved in brainstorming (sections 1–5); awaiting written-spec review
- **Scope:** sub-projects **A** (study / paper) and **B** (production router), designed together because they share one platform. Sub-project **C** (reshaping the knowledge base) gets its own, smaller spec later.
- **Background:** the literature review and gap analysis in `research/` (especially `05-gaps-and-agenda.md` and `06-research-proposals.md`).

## 1. Intent and success criteria

**Stated by the repository owner**
- Success means **a publishable paper and a production router, equally**.
- Compute: self-hosted open-weight models and API models (GPT, Claude), **all reached only through the Hooshyar API** (`https://hooshyar.golrang.ai/api/v1`, OpenAI-compatible, Bearer token). There is no white-box access to model internals.
- Hooshyar already provides a router (`model="auto"`) and `model="auto-judge"`, which returns the model `auto` would pick.
- Current traffic: an **internal assistant / chat** with low volume and plans to expand.
- Queries are **mostly Persian**, sometimes mixed Persian–English.
- Benchmark data: **public and synthetic only for now**; no internal conversations.

**Success criteria**
- *Production:* a router policy that beats Hooshyar `auto` on utility at matched or lower cost and passes the gate in §6.2, deployed without ever making production depend on the router's health.
- *Research:* (1) the first noise-aware, artifact-audited Persian / mixed-language routing benchmark; (2) evidence on whether English-built routers and `auto` transfer to Persian; (3) a black-box value-of-information (VOI) router that beats query-only routers at equal total cost.

**Gaps addressed** (see `research/05-gaps-and-agenda.md`): G12 (language coverage: Persian routing is a confirmed open slot), G1 (evaluation validity), G2 (query-only signal ceiling, in its black-box form). Logging is designed to enable G4 (learning from logs) later.

## 2. Architecture

```
 client apps ──OpenAI-compatible API (model="auto" | tier)──►  Router gateway
   1 normalizer   language (fa / en / mixed), conversation id, app id, budget hints
   2 policy engine   one pluggable RoutingPolicy → model, effort, reasons, P(model) for all models
   3 session manager   sticky model per conversation unless switching pays
   4 executor   calls Hooshyar; tier fallback on error/timeout
   5 decision logger   async, features + decision + outcome (no text by default)
                │
                ├──► observation service (research): cheap extra Hooshyar calls
                │      (short drafts, draft agreement, logprobs if available)
                └──► Hooshyar API: self-hosted open-weight tiers (small / medium)
                                   + API frontier tier (GPT, Claude) + auto / auto-judge
```

- **Model tiers, not names.** Policies reason over `small` / `medium` / `frontier`. `config/` maps tiers to concrete Hooshyar model names and prices, so adding or swapping a model is a config change.
- **One `RoutingPolicy` interface** serves production and research, so every research router is deployable.
- **Shadow mode.** The gateway can serve every request through `auto` while logging its own policy's decision and `auto-judge`'s decision.
- **Language:** Python, FastAPI gateway, `openai` client (matching Hooshyar's sample code).

## 3. Routing policies and request flow

| ID | Policy | Role |
|---|---|---|
| B0 | Hooshyar `auto` (decision read through `auto-judge`) | incumbent to beat |
| B1 | always-small / always-frontier | cost and quality bounds |
| R1 | **Requirement matching**: a small multilingual classifier scores needs (reasoning, code, factual knowledge, Persian writing quality, tool use); per-model **per-language** capability profiles; choose the cheapest model covering the needs | first production policy |
| R2 | **kNN** over multilingual embeddings with multi-sample outcome memory | mandatory baseline |
| R3 | **Black-box VOI router**: before committing, optionally buy one observation (none; 32–64-token draft from the small tier; two-draft agreement; draft entropy if `logprobs` are returned; full small-tier answer + check). Buy only if expected decision improvement > observation cost | research contribution |

**Request flow**
1. Normalize: detect language and load conversation state.
2. Session check: stay on the conversation's current model unless expected gain > switch cost. Switch cost is modelled as re-sending the history at the new model's input price.
3. Policy: returns a decision with probabilities and reasons. R3 may call the observation service first.
4. No wasted drafts: if an observation already produced an acceptable small-tier answer, return it (cascade behaviour).
5. Execute via Hooshyar, with tier fallback.
6. Log asynchronously (§5).

## 4. Study design

**Research questions**
- **RQ1:** How much routing headroom exists for Persian and mixed-language queries under noise-aware, artifact-audited labels, and how does it compare with English?
- **RQ2:** Do English-built routers (RouteLLM-style, kNN on English outcomes) and Hooshyar `auto` transfer to Persian?
- **RQ3:** Does the black-box VOI router (R3) beat query-only routers at equal total cost, moving past the routing plateau?

**Benchmark (contribution 1)**
- *Queries:* public Persian sets (candidates: ParsiNLU, Khayyam Challenge / PersianMMLU; licences and availability **to be verified**), Persian versions of reasoning and code tasks, and **synthetic Persian chat queries** generated from an internal-assistant task taxonomy (writing/editing, summarizing, factual QA, reasoning/math, code, office/business tasks), each with mixed and code-switched variants. Persian speakers review a sample.
- *Contamination guard:* synthetic queries are generated by one model family and judged by others.
- *Pool:* 4–6 models across Hooshyar tiers.
- *Labels:* k = 5 samples per (query, model) at production temperature, giving per-pair success-rate estimates. Exact-match scoring where possible. Open-ended items use two independent LLM judges plus Persian-speaking human calibration samples.
- *Artifact audit:* truncation-safe generation budgets; parse-failure checks.
- *Utility definition:* U = success rate − λ · cost per query (cost at real Hooshyar prices). λ is fixed per experiment and swept to draw cost–quality curves.
- *Baselines and metrics:* best single model, random routing at matched cost, kNN, task-type oracle, B0, and the expected oracle (argmax of p̂ − λ·c). Utility uses real Hooshyar prices. Report gap recovered beyond task type, and bootstrap 95% confidence intervals. Persian, English and mixed slices are reported separately.

**VOI router (contribution 2)**
- A learned estimator q̂(model | query, observations) is trained on benchmark samples.
- A myopic VOI rule buys an observation only when the expected improvement exceeds its cost. RL for multi-step acquisition is an extension.
- Comparisons: query-only routers (R1, R2), DART-style draft agreement, a simple cascade, and a Pandora-style two-level estimator baseline.

**Production evidence (contribution 3):** shadow-mode results for R1 and R3 vs `auto`, reported as **aggregates only** (agreement, estimated cost change, tier mix, fallback rate).

## 5. Logging, privacy and failure handling

**Decision log (one record per request, async)**
- Identifiers: `request_id`, timestamp, app id, hashed user id, conversation id.
- Features: language label, embedding / classifier scores, length.
- Decision: chosen model, effort, **probability for every model**, reasons, observations bought and their cost.
- Outcome: tokens, cost at Hooshyar prices, latency, errors, implicit signals (regenerate, rephrase, abandon; thumbs if the UI offers them).
- Shadow: `auto-judge` decision alongside ours.

**Privacy**
- No query or answer text in the research log by default. Text logging is a separate switch, off by default, governed by organizational retention rules.
- Tokens only from environment variables or a secrets store; never in code or the repository. The uploaded `tokens.json` is not used or copied.
- Research data stays inside organizational infrastructure.

**Failures**
- Model error or timeout → next tier up (logged).
- Router or classifier failure → pass through to Hooshyar `auto`.
- Observation failure → treat as "no observation".
- Budget guard: per-app daily spend cap. Above the cap, the frontier tier needs an explicit request. This also limits rerouting / cost-escalation attacks (gap G9).
- Sticky model unavailable → switch, log the switch and its cost.

## 6. Testing, evaluation and stages

**6.1 Code layout and testing**
```
gateway/   normalizer, session manager, executor, logger, budget guard (FastAPI)
policies/  RoutingPolicy interface; B0, B1, R1, R2, R3
observe/   observation service
bench/     datasets, synthetic generation, k-sample labelling, scoring, reports
paper/     analysis scripts and figures
config/    tier→model map, prices, budgets (no secrets)
tests/     unit + contract tests
```
- Unit tests: policy interface, tier mapping, stickiness, fallback chain, budget guard, language detector, and "no text logged when text logging is off".
- Contract tests against a mock OpenAI-compatible server with recorded fixtures (the development sandbox cannot reach Hooshyar).
- `scripts/smoke_hooshyar.py`: live check of every tier and `auto-judge`, run on the owner's side with the token from an environment variable.
- Reproducibility: fixed seeds, saved prompts, versioned price and model tables.

**6.2 Go-live gate for any policy**
The policy must beat B0 on utility at matched or lower cost, with a bootstrap 95% CI excluding zero. It must also have a success rate no more than 1 percentage point below B0's **in every task category**, and separately on the Persian and mixed slices.

**6.3 Stages**
| Stage | Content | Deliverable |
|---|---|---|
| 0 | Discovery script (models, logprobs, `auto-judge` format; see §7); gateway skeleton passing through to `auto`; logging; shadow `auto-judge`; tests; smoke script | production-safe infrastructure + answers to §7 |
| 1 | Benchmark v0 (public + synthetic, k-sample labels, artifact audit); B0, B1, R2 results | first answers to RQ1 and RQ2 |
| 2 | R1 in shadow → gate → live | production savings |
| 3 | R3 VOI router + comparisons; paper draft | the paper's main result |
| later | Learning from logs (P3); multi-turn and agent routing | — |

## 7. Open items, resolved by discovery tasks rather than by asking
The repository owner does not know these answers, so the plan resolves them empirically. Nothing in the design depends on any particular answer.
1. **`logprobs` support.** The Stage 0 discovery script requests `logprobs=true` from each tier and records whether they come back. If not, R3 drops the entropy observation and keeps drafts and agreement.
2. **Model list, prices, rate limits.** The discovery script calls `GET /models` and records the response. Prices and limits are filled into `config/` from Hooshyar's documentation or administrators. Until then, a placeholder price table marked *unverified* is used and every cost figure is labelled as such.
3. **`auto-judge` output format and cost.** The discovery script calls it on a fixed probe set and records the raw output, latency and token usage. The B0 adapter parses that recorded format.
4. **Persian dataset licences.** A planning task checks each candidate's licence and availability. Unusable sets are replaced by more synthetic data.
5. **Multilingual encoder for R1/R2.** Chosen empirically on benchmark v0.

## 8. Out of scope (for this spec)
- Using internal conversation data (revisit after organizational approval).
- White-box signals (activations); not available through the API.
- Token-level routing; agent and multi-turn routing beyond session stickiness.
- Reshaping the knowledge base (sub-project C, separate spec).
