from __future__ import annotations

from typing import Any

import pandas as pd


def calculate_risk(df: pd.DataFrame, darvas_result: dict[str, Any]) -> dict[str, Any]:
    latest = df.iloc[-1]
    close = float(latest["close"])
    candidates: list[tuple[str, float]] = []
    for reason, value in [
        ("box_low", darvas_result.get("box_low")),
        ("breakout_bar_low", latest.get("low")),
        ("ma20", latest.get("ma20")),
    ]:
        if value is not None and pd.notna(value) and float(value) < close:
            candidates.append((reason, float(value)))

    if not candidates:
        return {
            "stop_loss": None,
            "stop_loss_reason": "no_valid_reference",
            "risk_amount": 0.0,
            "reward_estimate": 0.0,
            "rr_ratio": 0.0,
            "risk_flags": ["止损参考不清晰"],
        }

    stop_loss_reason, stop_loss = max(candidates, key=lambda item: item[1])
    risk_amount = close - stop_loss
    box_high = darvas_result.get("box_high")
    box_width = darvas_result.get("box_width")
    reward_target = (box_high + box_width) if box_high and box_width else close
    reward_estimate = max(float(reward_target) - close, 0.0)
    rr_ratio = reward_estimate / risk_amount if risk_amount > 0 else 0.0
    flags: list[str] = []
    if rr_ratio < 2.0:
        flags.append("风险收益比不足")
    return {
        "stop_loss": round(stop_loss, 4),
        "stop_loss_reason": stop_loss_reason,
        "risk_amount": round(risk_amount, 4),
        "reward_estimate": round(reward_estimate, 4),
        "rr_ratio": round(rr_ratio, 4),
        "risk_flags": flags,
    }
