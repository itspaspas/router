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
configured tier (`logprobs`: true / false / null = error), and what `auto-judge` returns for five
fixed prompts (`auto_judge[].raw`, latency, usage). Run it once with empty tiers (logprobs are then
probed on `auto` only), fill the tiers as below, and run it again to probe each tier.

## 4. Fill the config from the report

- `config/router.yaml` `tiers`: set `small`, `medium`, `frontier` to Hooshyar model ids taken from
  `models.data[].id` (the ids `auto-judge` names in `auto_judge[].raw` are good candidates). An empty
  string means the tier is unconfigured.
- `config/prices.yaml` `models`: add `model id: [input, output]` USD per 1M tokens. Leave
  `verified: false` until the prices are confirmed with Hooshyar admins; only then set
  `verified: true`. Logged costs carry `cost_verified` accordingly.
- An over-budget app with no `small` tier configured keeps using `auto` (decision reason
  `budget_cap_unenforceable`), so the cap cannot be enforced until `small` is set.

Check connectivity afterwards: `python scripts/smoke_hooshyar.py` prints one `ok` / error-kind row
for `auto`, `auto-judge` and each configured tier (exit code 1 if any row is not `ok`).

## 5. Start the gateway

```
uvicorn --factory gateway.app:create_app_from_env --host 0.0.0.0 --port 8080
```

Health check: `GET /healthz`. Models listed at `GET /v1/models`: `auto`, `small`, `medium`, `frontier`.

## 6. Point the internal chat client at it

- Base URL: `http://<host>:<port>/v1`
- API key: `Bearer <app key>` (one of the keys in `ROUTER_APP_KEYS`)
- Model: `auto`

In Stage 0 the default policy passes everything to Hooshyar `auto`; a request naming a tier
(`small`, `medium`, `frontier`) or a Hooshyar model id is honoured as asked.

## 7. Logs and the shadow comparison

- Decision log: `ROUTER_LOG_PATH` (default `logs/decisions.jsonl`), one JSON record per request.
  Records contain routing metadata, tokens, cost, latency and error kind, not text (unless
  `ROUTER_LOG_TEXT=true`). `logs/` is gitignored.
- Shadow: when `shadow.enabled` is true in `config/router.yaml`, a sampled fraction
  (`shadow.sample_rate`) of requests also calls `auto-judge` in the background. Its result is stored in
  each record's `shadow_auto_judge` field (raw reply, parsed model, latency). Compare it (the model
  `auto` would pick) with `response_model` / `served_by` to see how closely a
  future policy would track `auto`. Shadow failures never affect the user request.
