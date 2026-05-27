from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_research_contexts(path: str | Path | None) -> dict[str, dict[str, Any]]:
    if not path:
        return {}
    file_path = Path(path)
    payload = json.loads(file_path.read_text(encoding="utf-8"))
    return normalize_research_contexts(payload)


def normalize_research_contexts(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if "symbols" in payload and isinstance(payload["symbols"], dict):
        return {_normalize_symbol(symbol): context for symbol, context in payload["symbols"].items() if isinstance(context, dict)}
    if "items" in payload and isinstance(payload["items"], list):
        contexts: dict[str, dict[str, Any]] = {}
        for item in payload["items"]:
            if isinstance(item, dict) and item.get("symbol"):
                contexts[_normalize_symbol(item["symbol"])] = item
        return contexts
    if payload.get("symbol"):
        return {_normalize_symbol(payload["symbol"]): payload}
    return {}


def get_research_context(contexts: dict[str, dict[str, Any]], symbol: str) -> dict[str, Any]:
    normalized = _normalize_symbol(symbol)
    if normalized in contexts:
        return contexts[normalized]
    without_exchange = normalized.split(".")[0]
    for key, value in contexts.items():
        if key.split(".")[0] == without_exchange:
            return value
    return {}


def _normalize_symbol(symbol: str) -> str:
    return str(symbol).strip().upper()
