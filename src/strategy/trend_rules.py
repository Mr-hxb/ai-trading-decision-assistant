from __future__ import annotations

from typing import Any

import pandas as pd


def evaluate_trend(df: pd.DataFrame, config: dict[str, Any]) -> dict[str, Any]:
    latest = df.iloc[-1]
    near_high_days = int(config.get("near_high_days", 120))
    near_high_pct = float(config.get("near_high_pct", 0.05))
    recent_high = float(df["close"].tail(near_high_days).max())
    ma50_prior = df["ma50"].iloc[-6] if len(df) >= 6 else df["ma50"].iloc[0]
    checks = {
        "close_above_ma20": bool(latest["close"] > latest["ma20"]),
        "ma20_above_ma50": bool(latest["ma20"] > latest["ma50"]),
        "ma50_up": bool(latest["ma50"] >= ma50_prior),
        "near_stage_high": bool(latest["close"] >= recent_high * (1 - near_high_pct)),
    }
    checks["not_obvious_downtrend"] = bool(latest["close"] >= latest["ma50"] and latest["ma20"] >= latest["ma50"] * 0.995)
    trend_score = round(sum(1 for value in checks.values() if value) / len(checks) * 30, 2)
    trend_ok = all(checks.values())
    return {
        "trend_ok": trend_ok,
        "trend_score": trend_score,
        "recent_high": recent_high,
        "checks": checks,
    }
