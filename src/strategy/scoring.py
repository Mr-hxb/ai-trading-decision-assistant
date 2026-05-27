from __future__ import annotations

from typing import Any


def calculate_score(
    trend_result: dict[str, Any],
    darvas_result: dict[str, Any],
    risk_result: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    trend_weight = float(config.get("trend_weight", 30))
    box_weight = float(config.get("box_weight", 30))
    volume_weight = float(config.get("volume_weight", 20))
    rr_weight = float(config.get("rr_weight", 10))
    fomo_penalty = float(config.get("fomo_penalty", 10))

    score = 0.0
    score += min(float(trend_result.get("trend_score", 0)), trend_weight)
    if darvas_result.get("has_box"):
        score += box_weight * 0.5
    if darvas_result.get("breakout_signal"):
        score += box_weight * 0.5
    if darvas_result.get("volume_breakout"):
        score += volume_weight
    rr_ratio = float(risk_result.get("rr_ratio") or 0)
    score += rr_weight if rr_ratio >= 2 else rr_weight * min(rr_ratio / 2, 1)
    if darvas_result.get("chase_risk"):
        score -= fomo_penalty
    score = max(0.0, min(100.0, score))
    return {"score": round(score, 2), "score_notes": ["分数只用于排序，不代表交易指令"]}
