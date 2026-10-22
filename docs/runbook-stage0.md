# Stage 0 runbook

Stage 0 runs the gateway as a pass-through to Hooshyar `auto`, logs every decision, and shadows
`auto-judge` for comparison. All commands run from the repository root.

## 1. Environment

| Variable | Required | Meaning |
|---|---|---|
| `HOOSHYAR_TOKEN` | yes | Hooshyar bearer token. Environment only; never in files or the repo. |
| `ROUTER_APP_KEYS` | yes | JSON object `{app_key: app_id}`, e.g. `{"k-chat-1":"chat"}`. |
| `ROUTER_LOG_SALT` | yes | Secret salt for hashing user ids in the decision log. |
| `HOOSHYAR_BASE_URL` | no | Default `https://hooshyar.golrang.ai/api/v1`. |
| `ROUTER_CONFIG` | no | Default `config/router.yaml`. |
| `ROUTER_LOG_PATH` | no | Default `logs/decisions.jsonl`. |
| `ROUTER_LOG_TEXT` | no | `true` also logs query/answer text. Default `false`; keep it off unless needed. |

## 2. Install

```
pip install -e . uvicorn
```

## 3. Run discovery

```
export HOOSHYAR_TOKEN=... ROUTER_APP_KEYS='{"k1":"chat"}' ROUTER_LOG_SALT=...
python scripts/discover_hooshyar.py
```

It prints a table and writes `discovery/report-<UTC date>.json` (gitignored, contains no token). The
report answers: which model ids exist (`models`), whether `logprobs` come back for `auto` and each
configured tier (`logprobs`: true / false / null = error), what `auto-judge` returns for five
fixed prompts (`auto_judge[].raw`, latency, usage), and whether a streamed `auto` reply carries
usage when the request sets `stream_options.include_usage` (`stream_include_usage`: true / false /
null = error). Run it once with empty tiers (logprobs are then
probed on `auto` only), fill the tiers as below, and run it again to probe each tier.

## 4. Fill the config from the report

- `config/router.yaml` `tiers`: set `small`, `medium`, `frontier` to Hooshyar model ids taken from
  `models.data[].id` (the ids `auto-judge` names in `auto_judge[].raw` are good candidates). An empty
  string means the tier is unconfigured.
- `config/prices.yaml` `models`: add `model id: [input, output]` USD per 1M tokens. Leave
  `verified: false` until the prices are confirmed with Hooshyar admins; only then set
  `verified: true`. Logged costs carry `cost_verified` accordingly.
- The budget guard is inert until `config/prices.yaml` has prices: an unpriced model's cost is
  unknown (`cost: null`) and never counts toward the daily cap.
- An over-budget app with no `small` tier configured keeps using `auto` (decision reason
  `budget_cap_unenforceable`), so the cap cannot be enforced until `small` is set.
- Streamed requests count toward cost and budget only when the upstream stream carries `usage`.
  Clients may send `stream_options: {"include_usage": true}` to ask for it; check
  `stream_include_usage` in the discovery report to see whether Hooshyar honours it. The gateway
  does not inject it yet; that is planned for Stage 2 once support is confirmed.

Check connectivity afterwards: `python scripts/smoke_hooshyar.py` prints one `ok` / error-kind row
for `auto`, `auto-judge` and each configured tier (exit code 1 if any row is not `ok`).

## 5. Start the gateway

```
uvicorn --factory gateway.app:create_app_from_env --host 0.0.0.0 --port 8080
```

Health check: `GET /healthz`. Models listed at `GET /v1/models`: `auto` plus each configured tier
(`small`, `medium`, `frontier`; an unconfigured tier is not listed). A request naming an
unconfigured tier gets 400 `model tier '<tier>' is not configured`.

- Run a single uvicorn worker (no `--workers N`): the budget is kept in memory and one process
  writes the JSONL decision log.
- `--host 0.0.0.0` exposes the gateway on every interface. Put it behind a reverse proxy with TLS
  on an internal network; do not expose it directly.

## 6. Point the internal chat client at it

- Base URL: `http://<host>:<port>/v1`
- API key: `Bearer <app key>` (one of the keys in `ROUTER_APP_KEYS`)
- Model: `auto`

Clients should send `model: "auto"`. In Stage 0 the default policy passes everything to Hooshyar
`auto`; a request naming a tier (`small`, `medium`, `frontier`) or a Hooshyar model id is honoured
as asked. A concrete model id is sent verbatim and bypasses the budget cap and the fallback chain.
Upstream 4xx errors (e.g. context too long, rate limited) are returned to the client with the
upstream error object and any `Retry-After` header; 5xx and network errors return a generic error.

## 7. Logs and the shadow comparison

- Decision log: `ROUTER_LOG_PATH` (default `logs/decisions.jsonl`), one JSON record per request.
  Records contain routing metadata, tokens, cost, latency and error kind, not text (unless
  `ROUTER_LOG_TEXT=true`). `logs/` is gitignored.
- Shadow: when `shadow.enabled` is true in `config/router.yaml`, a sampled fraction
  (`shadow.sample_rate`) of requests also calls `auto-judge` in the background. Its result is stored in
  each record's `shadow_auto_judge` field (raw reply, parsed model, latency). Compare it (the model
  `auto` would pick) with `response_model` / `served_by` to see how closely a
  future policy would track `auto`. Shadow failures never affect the user request.
- Shadow cost: at `sample_rate: 1.0` every request makes a second Hooshyar call, roughly doubling
  Hooshyar calls; lower `sample_rate` if that is too much. Shadow calls use their own small
  connection pool and at most 8 run at once; when all 8 are busy the shadow is skipped for that
  request (`shadow_auto_judge: null`).
