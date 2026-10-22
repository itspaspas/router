# Stage 0: Router Gateway Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A production-safe, OpenAI-compatible router gateway that passes every request through to Hooshyar `auto`, with tier fallback, a per-app budget guard, privacy-first decision logging, a shadow `auto-judge` comparison, and a discovery/smoke script that answers the spec's open items (§7).

**Architecture:** A FastAPI app (`gateway/`) authenticates internal apps, normalizes each request (language detection), asks a pluggable `RoutingPolicy` (`policies/`, here only B0 = pass-through to `auto`) for a decision, executes it against Hooshyar through an httpx client with a fallback chain, and logs a `DecisionRecord` asynchronously to JSONL. A fire-and-forget shadow task asks `auto-judge` what it would pick. Later stages add policies without touching the gateway.

**Tech Stack:** Python ≥ 3.11, FastAPI ≥ 0.110, httpx ≥ 0.27, PyYAML ≥ 6, pytest ≥ 8, pytest-asyncio ≥ 0.23, respx ≥ 0.21 (mocks httpx, which stands in for the spec's "mock OpenAI-compatible server").

**Spec:** `docs/superpowers/specs/2026-10-22-persian-router-design.md` (§2 architecture, §3 flow, §5 logging/privacy/failures, §6.1 testing, §6.3 Stage 0, §7 discovery). Stage 0 deliberately omits the session manager, observation service and policies R1–R3. Those belong to the Stage 2 and 3 plans.

## Global Constraints

- Upstream base URL default: `https://hooshyar.golrang.ai/api/v1` (env `HOOSHYAR_BASE_URL`). Auth: `Authorization: Bearer <HOOSHYAR_TOKEN>`.
- Hooshyar model ids used verbatim: `auto` (router) and `auto-judge` (returns the model `auto` would pick).
- Tiers are exactly `small`, `medium`, `frontier`. Policies and clients name tiers, and `config/router.yaml` maps tier → Hooshyar model id. An empty string means *unconfigured*.
- Secrets only from environment variables: `HOOSHYAR_TOKEN`, `ROUTER_APP_KEYS`, `ROUTER_LOG_SALT`. Never in code, config files, logs or the repo. The uploaded `tokens.json` is never used or copied.
- No query or answer text in the decision log unless `ROUTER_LOG_TEXT=true` (default `false`).
- Router failure must never fail a request that Hooshyar `auto` could serve.
- Prices are unverified until confirmed: `config/prices.yaml` carries `verified: false`, and every logged cost carries `cost_verified`.
- Upstream timeout default `120` s (matches Hooshyar's sample).

## Review Focus

1. **`stream: true` requests** (chat UIs stream). They must stream through unchanged. Fallback is allowed only before the first byte reaches the client, never mid-stream. → test in Task 5 and Task 8.
2. **Upstream 4xx** (bad request, context too long, invalid model). The error must pass through to the client and must *not* trigger fallback to a more expensive tier. → test in Task 5.
3. **Text leaking into logs when text logging is off**, including through error messages and exception strings in error records. → test in Task 6.
4. **Shadow `auto-judge` slow or failing.** The user's response status and latency must be unaffected. → test in Task 7 and Task 8.
5. **Unknown price for the model that answered** (prices unverified at launch). Cost is logged as `null`, the budget guard counts nothing for it, and the request still succeeds. → test in Task 4.

---

### Task 1: Project scaffold, settings and config loading

**Files:**
- Create: `pyproject.toml`, `gateway/__init__.py`, `gateway/config.py`, `config/router.yaml`, `config/prices.yaml`, `tests/__init__.py`, `tests/test_config.py`
- Modify: `.gitignore` (add `logs/`, `discovery/`, `.env`, `tokens.json`)

**Interfaces:**
- Produces:
  - `@dataclass(frozen=True) class Settings: base_url: str; token: str; config_path: Path; app_keys: dict[str, str]; log_path: Path; log_text: bool; log_salt: str` (`app_keys` maps app key → app id)
  - `def load_settings(env: Mapping[str, str] = os.environ) -> Settings`
  - `@dataclass(frozen=True) class RouterConfig: tiers: dict[str, str]; fallback: dict[str, list[str]]; default_daily_budget: float; per_app_budget: dict[str, float]; shadow_enabled: bool; shadow_sample_rate: float; timeout_s: float; prices: Prices`
  - `@dataclass(frozen=True) class Prices: verified: bool; models: dict[str, tuple[float, float]]` (input, output price per 1M tokens)
  - `def load_config(path: Path) -> RouterConfig`
  - `RouterConfig.model_for(tier: str) -> str | None` (None when unconfigured)

- [ ] **Step 1: Write the failing tests** in `tests/test_config.py`

```python
def test_settings_defaults_and_required(tmp_path):
    env = {"HOOSHYAR_TOKEN": "t", "ROUTER_APP_KEYS": '{"k1": "chat"}', "ROUTER_LOG_SALT": "s"}
    s = load_settings(env)
    assert s.base_url == "https://hooshyar.golrang.ai/api/v1"
    assert s.app_keys == {"k1": "chat"}
    assert s.log_text is False
    assert s.log_path == Path("logs/decisions.jsonl")
    assert s.config_path == Path("config/router.yaml")

@pytest.mark.parametrize("missing", ["HOOSHYAR_TOKEN", "ROUTER_APP_KEYS", "ROUTER_LOG_SALT"])
def test_settings_missing_secret_raises(missing):
    env = {"HOOSHYAR_TOKEN": "t", "ROUTER_APP_KEYS": "{}", "ROUTER_LOG_SALT": "s"}
    del env[missing]
    with pytest.raises(ValueError, match=missing):
        load_settings(env)

def test_example_config_loads_with_unconfigured_tiers():
    cfg = load_config(Path("config/router.yaml"))
    assert set(cfg.tiers) == {"small", "medium", "frontier"}
    assert cfg.model_for("small") is None          # "" means unconfigured
    assert cfg.fallback["auto"] == ["medium", "frontier"]
    assert cfg.fallback["small"] == ["medium", "frontier"]
    assert cfg.fallback["frontier"] == []
    assert cfg.timeout_s == 120
    assert cfg.prices.verified is False
```

- [ ] **Step 2: Run** `pytest tests/test_config.py -v`. Expected: FAIL (module missing).

- [ ] **Step 3: Implement** `gateway/config.py`, `config/router.yaml`, `config/prices.yaml`, `pyproject.toml` (deps from Tech Stack; `[tool.pytest.ini_options] asyncio_mode = "auto"`).
  `config/router.yaml` holds exactly: `tiers: {small: "", medium: "", frontier: ""}`; `fallback: {auto: [medium, frontier], small: [medium, frontier], medium: [frontier], frontier: []}`; `budget: {default_daily_usd: 5.0, per_app: {}}`; `shadow: {enabled: true, sample_rate: 1.0}`; `timeout_s: 120`; `prices_file: config/prices.yaml`.
  `config/prices.yaml` holds: `verified: false`, `currency: USD`, `models: {}`. Env defaults: `ROUTER_CONFIG=config/router.yaml`, `ROUTER_LOG_PATH=logs/decisions.jsonl`, `ROUTER_LOG_TEXT=false` (true only for the literal `"true"`).

- [ ] **Step 4: Run** `pytest tests/test_config.py -v`. Expected: PASS.

- [ ] **Step 5: Commit** `git add pyproject.toml gateway config tests .gitignore && git commit -m "feat(gateway): settings and router config loading"`

---

### Task 2: Language detection

**Files:** Create `gateway/language.py`, `tests/test_language.py`

**Interfaces:**
- Produces: `def detect_language(text: str) -> Literal["fa", "en", "mixed", "unknown"]`

- [ ] **Step 1: Write the failing tests**

```python
@pytest.mark.parametrize("text,expected", [
    ("یک شعر کوتاه درباره باران بنویس", "fa"),
    ("Write a short poem about rain.", "en"),
    ("لطفاً این function را در Python بازنویسی کن", "mixed"),
    ("می‌خواهم", "fa"),                 # ZWNJ (U+200C) must not count as Latin
    ("۱۲۳ 456 !!!", "unknown"),         # digits/punctuation only
    ("", "unknown"),
])
def test_detect_language(text, expected):
    assert detect_language(text) == expected
```

- [ ] **Step 2: Run** `pytest tests/test_language.py -v`. Expected: FAIL.

- [ ] **Step 3: Implement `detect_language`.** Count letters only (`str.isalpha()`). Arabic-script letters are code points in U+0600–U+06FF, U+0750–U+077F, U+FB50–U+FDFF and U+FE70–U+FEFF; Latin letters are ASCII `a–zA–Z`. With `r = arabic / (arabic + latin)`: no letters → `"unknown"`; `r ≥ 0.8` → `"fa"`; `r ≤ 0.2` → `"en"`; otherwise `"mixed"`. (Arabic-language text is labelled `fa`. This is a known limitation, noted in a docstring.)

- [ ] **Step 4: Run** `pytest tests/test_language.py -v`. Expected: PASS.

- [ ] **Step 5: Commit** `git commit -am "feat(gateway): Persian/English/mixed language detection"` (after `git add` of the new files)

---

### Task 3: Policy interface and B0 pass-through policy

**Files:** Create `policies/__init__.py`, `policies/base.py`, `policies/auto_passthrough.py`, `tests/test_policies.py`

**Interfaces:**
- Produces:
  - `@dataclass(frozen=True) class RouteRequest: body: dict; app_id: str; conversation_id: str | None; language: str`
  - `@dataclass(frozen=True) class Decision: target: str; policy: str; probs: dict[str, float]; reasons: tuple[str, ...] = (); effort: str | None = None`. Here `target` is `"auto"`, a tier name, or a concrete Hooshyar model id.
  - `class RoutingPolicy(Protocol): name: str; def decide(self, req: RouteRequest) -> Decision: ...`
  - `class AutoPassthrough: name = "b0_auto"`

- [ ] **Step 1: Write the failing tests**

```python
def req(model=None):
    body = {"messages": [{"role": "user", "content": "سلام"}]}
    if model: body["model"] = model
    return RouteRequest(body=body, app_id="chat", conversation_id=None, language="fa")

def test_b0_routes_auto_by_default():
    d = AutoPassthrough().decide(req())
    assert d.target == "auto" and d.policy == "b0_auto" and d.probs == {"auto": 1.0}

@pytest.mark.parametrize("m", ["auto", "small", "medium", "frontier", "some-hooshyar-model"])
def test_b0_honours_explicit_model(m):
    d = AutoPassthrough().decide(req(m))
    assert d.target == m and d.probs == {m: 1.0} and "explicit" in d.reasons[0]
```

- [ ] **Step 2: Run** `pytest tests/test_policies.py -v`. Expected: FAIL.
- [ ] **Step 3: Implement** the dataclasses, the Protocol and `AutoPassthrough.decide`. A missing `model` or `model == "auto"` targets `auto` (reason `"default: hooshyar auto"`); anything else targets the given value (reason `"explicit model requested"`).
- [ ] **Step 4: Run** `pytest tests/test_policies.py -v`. Expected: PASS.
- [ ] **Step 5: Commit** `git commit -m "feat(policies): RoutingPolicy interface and B0 auto pass-through"`

---

### Task 4: Hooshyar client, cost computation and budget guard

**Files:** Create `gateway/hooshyar.py`, `gateway/budget.py`, `tests/test_hooshyar.py`, `tests/test_budget.py`

**Interfaces:**
- Consumes: `Settings`, `RouterConfig`, `Prices` (Task 1)
- Produces:
  - `class UpstreamError(Exception): status: int | None; retryable: bool`. Retryable means timeout, connection error or status ≥ 500. A 4xx is not retryable.
  - `class HooshyarClient: def __init__(self, base_url: str, token: str, timeout_s: float, http: httpx.AsyncClient | None = None)`
    - `async def chat(self, body: dict) -> dict` (non-stream; raises `UpstreamError`)
    - `async def open_stream(self, body: dict) -> AsyncIterator[bytes]`. Raises `UpstreamError` *before* yielding if the status is not 200. Once it yields, it yields raw SSE bytes unchanged.
    - `async def list_models(self) -> dict` (`GET /models`)
  - `def compute_cost(model: str | None, usage: dict | None, prices: Prices) -> float | None`: USD, or None if the model or usage is missing.
  - `class BudgetGuard: def __init__(self, cfg: RouterConfig, clock: Callable[[], datetime] = utcnow)`
    - `def over_cap(self, app_id: str) -> bool`
    - `def record(self, app_id: str, cost: float | None) -> None` (ignores None; resets at UTC midnight)

- [ ] **Step 1: Write the failing tests** (respx mocks `https://h.test/v1`)

```python
async def test_chat_sends_bearer_and_returns_json(respx_mock):
    route = respx_mock.post("https://h.test/v1/chat/completions").respond(200, json={"model": "m1", "choices": []})
    c = HooshyarClient("https://h.test/v1", "TOKEN", 5)
    assert (await c.chat({"model": "auto", "messages": []}))["model"] == "m1"
    assert route.calls[0].request.headers["authorization"] == "Bearer TOKEN"

@pytest.mark.parametrize("status,retryable", [(400, False), (413, False), (500, True), (503, True)])
async def test_chat_error_classification(respx_mock, status, retryable):
    respx_mock.post("https://h.test/v1/chat/completions").respond(status, json={"error": {"message": "x"}})
    with pytest.raises(UpstreamError) as e:
        await HooshyarClient("https://h.test/v1", "T", 5).chat({})
    assert e.value.status == status and e.value.retryable is retryable

async def test_timeout_is_retryable(respx_mock):
    respx_mock.post("https://h.test/v1/chat/completions").mock(side_effect=httpx.ReadTimeout("t"))
    with pytest.raises(UpstreamError) as e:
        await HooshyarClient("https://h.test/v1", "T", 5).chat({})
    assert e.value.retryable is True and e.value.status is None

async def test_stream_yields_raw_bytes(respx_mock):
    sse = b'data: {"choices":[{"delta":{"content":"hi"}}]}\n\ndata: [DONE]\n\n'
    respx_mock.post("https://h.test/v1/chat/completions").respond(200, content=sse, headers={"content-type": "text/event-stream"})
    chunks = [c async for c in HooshyarClient("https://h.test/v1", "T", 5).open_stream({"stream": True})]
    assert b"".join(chunks) == sse

def test_cost_known_and_unknown():
    p = Prices(verified=False, models={"m1": (1.0, 2.0)})
    assert compute_cost("m1", {"prompt_tokens": 1_000_000, "completion_tokens": 500_000}, p) == pytest.approx(2.0)
    assert compute_cost("unpriced", {"prompt_tokens": 10, "completion_tokens": 10}, p) is None
    assert compute_cost("m1", None, p) is None

def test_budget_cap_and_midnight_reset(cfg_with_budget):   # fixture: default 5.0, per_app {"chat": 1.0}
    now = [datetime(2026, 10, 22, 23, 0, tzinfo=UTC)]
    g = BudgetGuard(cfg_with_budget, clock=lambda: now[0])
    g.record("chat", 0.6); assert not g.over_cap("chat")
    g.record("chat", 0.5); assert g.over_cap("chat")
    g.record("chat", None); assert g.over_cap("chat")           # unknown cost ignored
    assert not g.over_cap("other")                               # default cap 5.0
    now[0] = datetime(2026, 10, 23, 0, 1, tzinfo=UTC); assert not g.over_cap("chat")
```

- [ ] **Step 2: Run** `pytest tests/test_hooshyar.py tests/test_budget.py -v`. Expected: FAIL.
- [ ] **Step 3: Implement** `gateway/hooshyar.py` with a shared `httpx.AsyncClient` (`timeout=timeout_s`) and `client.stream("POST", ...)` for streaming. Implement `gateway/budget.py`: in-memory `dict[app_id, float]` keyed by the UTC date, with the cap `per_app_budget.get(app, default_daily_budget)`.
- [ ] **Step 4: Run** the same tests. Expected: PASS.
- [ ] **Step 5: Commit** `git commit -m "feat(gateway): Hooshyar client, cost computation, budget guard"`

---

### Task 5: Executor with fallback chain

**Files:** Create `gateway/executor.py`, `tests/test_executor.py`

**Interfaces:**
- Consumes: `HooshyarClient`, `UpstreamError` (Task 4); `RouterConfig.fallback`, `RouterConfig.model_for` (Task 1); `Decision` (Task 3)
- Produces:
  - `@dataclass class ExecResult: served_by: str; attempts: list[str]; response: dict | None; stream: AsyncIterator[bytes] | None`. `served_by` is the upstream model id string sent (`"auto"` or a Hooshyar id), and `attempts` lists every target tried, in order.
  - `async def execute(decision: Decision, body: dict, client: HooshyarClient, cfg: RouterConfig, stream: bool) -> ExecResult`. It raises the last `UpstreamError` if every target fails, or the first non-retryable one immediately.

Resolution rule: a target that is a tier name resolves through `cfg.model_for`, and unconfigured tiers are skipped (recorded in `attempts` as `"<tier>:unconfigured"`). The chain is `[decision.target] + cfg.fallback.get(decision.target, [])`. A concrete model id has no fallback.

- [ ] **Step 1: Write the failing tests**

```python
async def test_auto_success_no_fallback(respx_mock, cfg_tiers):   # tiers: small="s1", medium="m1", frontier="f1"
    respx_mock.post(URL).respond(200, json={"model": "x"})
    r = await execute(Decision("auto", "b0_auto", {"auto": 1.0}), BODY, client, cfg_tiers, stream=False)
    assert r.served_by == "auto" and r.attempts == ["auto"]

async def test_auto_500_falls_back_to_medium(respx_mock, cfg_tiers):
    respx_mock.post(URL).mock(side_effect=[httpx.Response(500), httpx.Response(200, json={"model": "m1"})])
    r = await execute(Decision("auto", "b0_auto", {"auto": 1.0}), BODY, client, cfg_tiers, stream=False)
    assert r.served_by == "m1" and r.attempts == ["auto", "medium"]
    assert json.loads(respx_mock.calls[1].request.content)["model"] == "m1"

async def test_4xx_is_not_retried(respx_mock, cfg_tiers):
    respx_mock.post(URL).respond(400, json={"error": {"message": "context too long"}})
    with pytest.raises(UpstreamError) as e:
        await execute(Decision("auto", "b0_auto", {"auto": 1.0}), BODY, client, cfg_tiers, stream=False)
    assert e.value.status == 400 and len(respx_mock.calls) == 1

async def test_unconfigured_tier_skipped(respx_mock, cfg_no_medium):   # medium=""
    respx_mock.post(URL).mock(side_effect=[httpx.Response(503), httpx.Response(200, json={"model": "f1"})])
    r = await execute(Decision("auto", "b0_auto", {"auto": 1.0}), BODY, client, cfg_no_medium, stream=False)
    assert r.attempts == ["auto", "medium:unconfigured", "frontier"] and r.served_by == "f1"

async def test_stream_fallback_only_before_first_byte(respx_mock, cfg_tiers):
    respx_mock.post(URL).mock(side_effect=[httpx.Response(502), httpx.Response(200, content=b"data: [DONE]\n\n")])
    r = await execute(Decision("auto", "b0_auto", {"auto": 1.0}), {**BODY, "stream": True}, client, cfg_tiers, stream=True)
    assert r.attempts == ["auto", "medium"] and b"".join([c async for c in r.stream]) == b"data: [DONE]\n\n"
```

- [ ] **Step 2: Run** `pytest tests/test_executor.py -v`. Expected: FAIL.
- [ ] **Step 3: Implement `execute`.** Send `{**body, "model": resolved_id}` for each target. For streams, fall back only when `open_stream` raises before its first yield. Get that first chunk eagerly inside `execute` and return a generator that re-yields it followed by the rest, so mid-stream errors propagate to the client instead of triggering fallback.
- [ ] **Step 4: Run** `pytest tests/test_executor.py -v`. Expected: PASS.
- [ ] **Step 5: Commit** `git commit -m "feat(gateway): executor with tier fallback chain"`

---

### Task 6: Privacy-first decision logger

**Files:** Create `gateway/decision_log.py`, `tests/test_decision_log.py`

**Interfaces:**
- Consumes: `Decision` (Task 3)
- Produces:
  - `@dataclass class DecisionRecord`, with fields: `request_id: str, ts: str, app_id: str, user_hash: str | None, conversation_id: str | None, language: str, n_messages: int, prompt_chars: int, policy: str, target: str, probs: dict, reasons: list, attempts: list, served_by: str | None, response_model: str | None, prompt_tokens: int | None, completion_tokens: int | None, cost: float | None, cost_verified: bool, latency_ms: int, status: int, error_kind: str | None, stream: bool, shadow_auto_judge: dict | None = None, text: dict | None = None`
  - `def hash_user(user: str | None, salt: str) -> str | None` (sha256 hex of `salt + user`)
  - `class DecisionLogger: def __init__(self, path: Path, log_text: bool)`; `def emit(self, rec: DecisionRecord) -> None` (non-blocking enqueue); `async def run(self) -> None` (background writer, one JSON object per line, `ensure_ascii=False`); `async def close(self) -> None` (drains the queue)
  - `error_kind` is a fixed vocabulary only: `"timeout" | "connection" | "upstream_4xx" | "upstream_5xx" | "auth" | "internal"`. It is never an exception message.

- [ ] **Step 1: Write the failing tests**

```python
async def test_no_text_written_when_disabled(tmp_path):
    log = DecisionLogger(tmp_path / "d.jsonl", log_text=False)
    task = asyncio.create_task(log.run())
    log.emit(make_record(text={"query": "رمز عبور من 1234 است", "answer": "SECRET-ANSWER"}, error_kind="upstream_4xx"))
    await log.close(); task.cancel()
    raw = (tmp_path / "d.jsonl").read_text(encoding="utf-8")
    assert "1234" not in raw and "SECRET-ANSWER" not in raw and "رمز" not in raw
    assert json.loads(raw.splitlines()[0])["text"] is None

async def test_text_written_when_enabled(tmp_path):
    log = DecisionLogger(tmp_path / "d.jsonl", log_text=True)
    task = asyncio.create_task(log.run())
    log.emit(make_record(text={"query": "سلام", "answer": "hi"}))
    await log.close(); task.cancel()
    assert json.loads((tmp_path / "d.jsonl").read_text(encoding="utf-8"))["text"]["query"] == "سلام"

def test_hash_user_stable_and_salted():
    assert hash_user("ali", "s1") == hash_user("ali", "s1") != hash_user("ali", "s2")
    assert hash_user(None, "s1") is None

def test_error_kind_vocabulary_enforced():
    with pytest.raises(ValueError):
        make_record(error_kind="Traceback: something with user text")
```

- [ ] **Step 2: Run** `pytest tests/test_decision_log.py -v`. Expected: FAIL.
- [ ] **Step 3: Implement.** The logger sets `rec.text = None` before serializing when `log_text` is false. `DecisionRecord.__post_init__` validates `error_kind` against the vocabulary. Writes are appends, and `run` creates the parent directory.
- [ ] **Step 4: Run** `pytest tests/test_decision_log.py -v`. Expected: PASS.
- [ ] **Step 5: Commit** `git commit -m "feat(gateway): privacy-first async decision logger"`

---

### Task 7: Shadow `auto-judge`

**Files:** Create `gateway/shadow.py`, `tests/test_shadow.py`

**Interfaces:**
- Consumes: `HooshyarClient` (Task 4)
- Produces: `async def shadow_auto_judge(client: HooshyarClient, messages: list[dict], known_models: set[str], timeout_s: float = 30.0) -> dict`. It returns `{"raw": str | None, "parsed_model": str | None, "latency_ms": int, "ok": bool}` and never raises.

`raw` is the first 200 characters of `choices[0].message.content` (the output format is unverified; see spec §7.3). `parsed_model` is the first id in `known_models` that occurs in `raw` (longest match first), else None.

- [ ] **Step 1: Write the failing tests**

```python
async def test_parses_known_model(respx_mock):
    respx_mock.post(URL).respond(200, json={"choices": [{"message": {"content": "  gpt-4o-mini\n"}}]})
    r = await shadow_auto_judge(client, MSGS, {"gpt-4o", "gpt-4o-mini"})
    assert r["ok"] and r["parsed_model"] == "gpt-4o-mini" and r["raw"].strip() == "gpt-4o-mini"
    assert json.loads(respx_mock.calls[0].request.content)["model"] == "auto-judge"

async def test_never_raises_on_error_or_timeout(respx_mock):
    respx_mock.post(URL).mock(side_effect=httpx.ConnectError("x"))
    r = await shadow_auto_judge(client, MSGS, set())
    assert r == {"raw": None, "parsed_model": None, "latency_ms": r["latency_ms"], "ok": False}
```

- [ ] **Step 2: Run** `pytest tests/test_shadow.py -v`. Expected: FAIL.
- [ ] **Step 3: Implement** with `asyncio.wait_for(..., timeout_s)`, catching every `Exception`. The body is `{"model": "auto-judge", "stream": False, "messages": messages}`.
- [ ] **Step 4: Run** `pytest tests/test_shadow.py -v`. Expected: PASS.
- [ ] **Step 5: Commit** `git commit -m "feat(gateway): shadow auto-judge comparison"`

---

### Task 8: FastAPI app wiring

**Files:** Create `gateway/app.py`, `tests/test_app.py`

**Interfaces:**
- Consumes: everything above.
- Produces: `def create_app(settings: Settings, cfg: RouterConfig, policy: RoutingPolicy | None = None, client: HooshyarClient | None = None) -> FastAPI` (default policy `AutoPassthrough()`). Endpoints:
  - `POST /v1/chat/completions`: OpenAI-compatible; `Authorization: Bearer <app key>` is looked up in `settings.app_keys` (401 otherwise); optional headers `X-Conversation-Id` and `X-User-Id` (hashed before logging).
  - `GET /v1/models`: lists `auto`, `small`, `medium`, `frontier`.
  - `GET /healthz`: `{"ok": true}`.
- Response headers on chat: `X-Router-Policy`, `X-Router-Served-By`.

Request flow: auth → `detect_language` (last user message) → policy decide; if the policy raises, use `AutoPassthrough` with reason `"policy_error"`. Budget: if `over_cap(app)` and target == `auto`, the target becomes `small` (reason `"budget_cap"`). Explicit tiers and models are honoured. Then `execute` → respond. Log asynchronously (stream: after the stream ends, from the final usage chunk if present). If shadow is enabled, sample at `shadow_sample_rate` and run `shadow_auto_judge` as a background task whose result is merged into the record before it is emitted. The response never waits for the shadow call.

- [ ] **Step 1: Write the failing tests** (use `httpx.AsyncClient(transport=ASGITransport(app))` plus respx for upstream; a `tmp_path` log)

```python
async def test_unauthorized(app_client):
    r = await app_client.post("/v1/chat/completions", json=BODY)
    assert r.status_code == 401

async def test_passthrough_to_auto_and_logs(app_client, respx_mock, log_lines):
    respx_mock.post(UP).respond(200, json={"model": "m1", "choices": [{"message": {"content": "سلام"}}], "usage": {"prompt_tokens": 5, "completion_tokens": 3}})
    r = await app_client.post("/v1/chat/completions", json=BODY_FA, headers=AUTH)
    assert r.status_code == 200 and r.headers["x-router-policy"] == "b0_auto"
    rec = (await log_lines())[0]
    assert rec["language"] == "fa" and rec["target"] == "auto" and rec["response_model"] == "m1"
    assert rec["text"] is None and rec["cost"] is None and rec["cost_verified"] is False

async def test_upstream_400_passes_through(app_client, respx_mock):
    respx_mock.post(UP).respond(400, json={"error": {"message": "bad"}})
    r = await app_client.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 400 and len(respx_mock.calls) == 1

async def test_streaming_passthrough(app_client, respx_mock):
    sse = b'data: {"choices":[{"delta":{"content":"hi"}}]}\n\ndata: [DONE]\n\n'
    respx_mock.post(UP).respond(200, content=sse, headers={"content-type": "text/event-stream"})
    r = await app_client.post("/v1/chat/completions", json={**BODY, "stream": True}, headers=AUTH)
    assert r.headers["content-type"].startswith("text/event-stream") and r.content == sse

async def test_slow_failing_shadow_does_not_delay(app_client_shadow, respx_mock):
    respx_mock.post(UP).mock(side_effect=route_by_model({"auto-judge": slow_then_error(seconds=5)}, default=ok_json))
    t0 = time.monotonic()
    r = await app_client_shadow.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 200 and time.monotonic() - t0 < 1.0

async def test_budget_cap_downgrades_auto_only(app_client_capped, respx_mock):   # cap 0.0 for app "chat"
    respx_mock.post(UP).respond(200, json={"model": "s1", "choices": []})
    await app_client_capped.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert json.loads(respx_mock.calls[-1].request.content)["model"] == "s1"            # auto -> small
    await app_client_capped.post("/v1/chat/completions", json={**BODY, "model": "frontier"}, headers=AUTH)
    assert json.loads(respx_mock.calls[-1].request.content)["model"] == "f1"            # explicit honoured

async def test_policy_exception_falls_back_to_auto(app_client_broken_policy, respx_mock):
    respx_mock.post(UP).respond(200, json={"model": "m1", "choices": []})
    r = await app_client_broken_policy.post("/v1/chat/completions", json=BODY, headers=AUTH)
    assert r.status_code == 200 and json.loads(respx_mock.calls[0].request.content)["model"] == "auto"
```

- [ ] **Step 2: Run** `pytest tests/test_app.py -v`. Expected: FAIL.
- [ ] **Step 3: Implement `create_app`.** It uses a lifespan that starts and stops `DecisionLogger.run`. Upstream errors that exhaust the chain return the upstream status (or 502 for timeout or connection failures) with an OpenAI-style error body. `cfg_with_budget` (cap 0.0) makes `over_cap` true from the first request.
- [ ] **Step 4: Run** `pytest -v` (full suite). Expected: all PASS.
- [ ] **Step 5: Commit** `git commit -m "feat(gateway): FastAPI app with auth, fallback, budget, shadow, logging"`

---

### Task 9: Discovery and smoke scripts plus runbook

**Files:** Create `gateway/probe.py`, `scripts/discover_hooshyar.py`, `scripts/smoke_hooshyar.py`, `tests/test_probe.py`, `docs/runbook-stage0.md`

**Interfaces:**
- Consumes: `HooshyarClient`, `load_settings`, `load_config`
- Produces:
  - `PROBE_PROMPTS: list[str]`: exactly these 5, in order: `"Write a short poem about rain."`, `"یک شعر کوتاه درباره باران بنویس."`, `"Solve: 17 * 23 = ?"`, `"این تابع Python را توضیح بده: def f(x): return x[::-1]"`, `"خلاصه‌ای سه‌جمله‌ای از مزایای انرژی خورشیدی بنویس."`
  - `async def discover(client: HooshyarClient, cfg: RouterConfig) -> dict` returns `{"models": <GET /models json or {"error": kind}>, "logprobs": {tier_or_auto: bool | None}, "auto_judge": [{"prompt_idx": int, "raw": str|None, "latency_ms": int, "usage": dict|None}], "ts": iso}`. Logprobs are tested with `{"logprobs": true, "max_tokens": 5}` on `auto` and on each configured tier, recording True if `choices[0].logprobs` is non-null, False if null, and None on error.
  - `async def smoke(client, cfg) -> list[tuple[str, str]]`: one `(target, "ok" | error_kind)` row each for `auto`, `auto-judge` and every configured tier, using the first probe prompt with `max_tokens: 16`.
  - Scripts read env via `load_settings`. `discover_hooshyar.py` writes `discovery/report-<UTC date>.json` (directory gitignored); both scripts print a table. The token never appears in output.

- [ ] **Step 1: Write the failing tests**

```python
async def test_discover_shape_and_logprobs(respx_mock, cfg_tiers):
    respx_mock.get(MODELS).respond(200, json={"data": [{"id": "s1"}]})
    respx_mock.post(UP).mock(side_effect=route_by_model(
        {"auto-judge": ok_text("s1")}, default=lambda req: httpx.Response(200, json={"choices": [{"logprobs": None, "message": {"content": "x"}}]})))
    rep = await discover(client, cfg_tiers)
    assert rep["models"]["data"][0]["id"] == "s1"
    assert rep["logprobs"] == {"auto": False, "small": False, "medium": False, "frontier": False}
    assert len(rep["auto_judge"]) == 5 and rep["auto_judge"][0]["raw"] == "s1"

async def test_smoke_reports_errors_without_raising(respx_mock, cfg_tiers):
    respx_mock.post(UP).respond(503)
    rows = await smoke(client, cfg_tiers)
    assert rows[0] == ("auto", "upstream_5xx") and len(rows) == 5

def test_scripts_never_print_token(capsys, monkeypatch):   # run the smoke main() against respx with token "SECRET-T"
    ...
    assert "SECRET-T" not in capsys.readouterr().out
```

- [ ] **Step 2: Run** `pytest tests/test_probe.py -v`. Expected: FAIL.
- [ ] **Step 3: Implement** `gateway/probe.py` and the two thin scripts (`asyncio.run`). Write `docs/runbook-stage0.md`: required env vars, how to run the discovery script, how to fill `config/router.yaml` tiers and `config/prices.yaml` from the report, `uvicorn gateway.app:app` startup (a module-level `app = create_app(load_settings(), load_config(...))` guarded behind a factory for tests), and how to point the internal chat client at the gateway.
- [ ] **Step 4: Run** `pytest -v`. Expected: all PASS.
- [ ] **Step 5: Commit** `git commit -m "feat: Hooshyar discovery and smoke scripts, Stage 0 runbook"`

---

## After this plan
The owner runs `scripts/discover_hooshyar.py` with their token, fills the tier map and prices, and deploys the gateway in pass-through/shadow mode. The discovery report then feeds the Stage 1 (benchmark) and Stage 2 (R1 router plus session manager) plans.
