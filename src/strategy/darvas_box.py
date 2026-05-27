from __future__ import annotations

from typing import Any

import pandas as pd


def evaluate_darvas_setup(df: pd.DataFrame, config: dict[str, Any]) -> dict[str, Any]:
    latest = df.iloc[-1]
    box_high = latest.get("box_high")
    close = float(latest["close"])
    chase_risk_pct = float(config.get("chase_risk_pct", 0.08))
    has_box = bool(pd.notna(box_high) and latest.get("in_box", False))
    distance = float((close - box_high) / box_high) if pd.notna(box_high) and box_high else None
    chase_risk = bool(distance is not None and distance > chase_risk_pct)
    return {
        "has_box": has_box,
        "box_high": float(latest["box_high"]) if pd.notna(latest.get("box_high")) else None,
        "box_low": float(latest["box_low"]) if pd.notna(latest.get("box_low")) else None,
        "box_width": float(latest["box_width"]) if pd.notna(latest.get("box_width")) else None,
        "box_range_pct": float(latest["box_range_pct"]) if pd.notna(latest.get("box_range_pct")) else None,
        "breakout_signal": bool(latest.get("breakout_signal", False)),
        "volume_breakout": bool(latest.get("volume_ratio", 0) > config.get("breakout_volume_ratio", 1.5)),
        "distance_from_box_high": distance,
        "chase_risk": chase_risk,
    }
