"""Settings (environment) and router configuration (YAML) loading."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

DEFAULT_BASE_URL = "https://hooshyar.golrang.ai/api/v1"
DEFAULT_CONFIG_PATH = "config/router.yaml"
DEFAULT_LOG_PATH = "logs/decisions.jsonl"
DEFAULT_TIMEOUT_S = 120.0


@dataclass(frozen=True)
class Settings:
    base_url: str
    token: str
    config_path: Path
    app_keys: dict[str, str]  # app key -> app id
    log_path: Path
    log_text: bool
    log_salt: str


def _require(env: Mapping[str, str], name: str) -> str:
    value = env.get(name)
    if value is None or value == "":
        raise ValueError(f"missing required environment variable {name}")
    return value


def load_settings(env: Mapping[str, str] = os.environ) -> Settings:
    token = _require(env, "HOOSHYAR_TOKEN")
    raw_keys = _require(env, "ROUTER_APP_KEYS")
    salt = _require(env, "ROUTER_LOG_SALT")
    try:
        app_keys = json.loads(raw_keys)
    except json.JSONDecodeError as e:
        raise ValueError("ROUTER_APP_KEYS must be a JSON object of app key -> app id") from e
    if not isinstance(app_keys, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in app_keys.items()
    ):
        raise ValueError("ROUTER_APP_KEYS must be a JSON object of app key -> app id")
    return Settings(
        base_url=env.get("HOOSHYAR_BASE_URL") or DEFAULT_BASE_URL,
        token=token,
        config_path=Path(env.get("ROUTER_CONFIG") or DEFAULT_CONFIG_PATH),
        app_keys=app_keys,
        log_path=Path(env.get("ROUTER_LOG_PATH") or DEFAULT_LOG_PATH),
        log_text=env.get("ROUTER_LOG_TEXT", "false") == "true",
        log_salt=salt,
    )


@dataclass(frozen=True)
class Prices:
    verified: bool
    models: dict[str, tuple[float, float]]  # model -> (input, output) USD per 1M tokens


@dataclass(frozen=True)
class RouterConfig:
    tiers: dict[str, str]
    fallback: dict[str, list[str]]
    default_daily_budget: float
    per_app_budget: dict[str, float]
    shadow_enabled: bool
    shadow_sample_rate: float
    timeout_s: float
    prices: Prices

    def model_for(self, tier: str) -> str | None:
        """Hooshyar model id for a tier; None when the tier is unconfigured."""
        return self.tiers.get(tier) or None


def _read_yaml(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


def _load_prices(path: Path) -> Prices:
    data = _read_yaml(path)
    models = {
        name: (float(p[0]), float(p[1])) for name, p in (data.get("models") or {}).items()
    }
    return Prices(verified=data.get("verified") is True, models=models)


def load_config(path: Path) -> RouterConfig:
    path = Path(path)
    data = _read_yaml(path)
    budget = data.get("budget") or {}
    shadow = data.get("shadow") or {}
    prices_file = Path(data.get("prices_file", "config/prices.yaml"))
    if not prices_file.is_absolute() and not prices_file.exists():
        sibling = path.parent / prices_file.name
        if sibling.exists():
            prices_file = sibling
    return RouterConfig(
        tiers={k: (v or "") for k, v in (data.get("tiers") or {}).items()},
        fallback={k: list(v or []) for k, v in (data.get("fallback") or {}).items()},
        default_daily_budget=float(budget.get("default_daily_usd", 5.0)),
        per_app_budget={k: float(v) for k, v in (budget.get("per_app") or {}).items()},
        shadow_enabled=bool(shadow.get("enabled", True)),
        shadow_sample_rate=float(shadow.get("sample_rate", 1.0)),
        timeout_s=float(data.get("timeout_s", DEFAULT_TIMEOUT_S)),
        prices=_load_prices(prices_file),
    )
