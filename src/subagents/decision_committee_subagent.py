from __future__ import annotations

from typing import Any

from src.subagents.base import BaseSubagent, SubagentResult, VALID_DECISION_STATUSES


class DecisionCommitteeSubagent(BaseSubagent):
    name = "DecisionCommitteeSubagent"

    def run(self, input_data: dict[str, Any]) -> SubagentResult:
        config = input_data["config"].get("decision_committee", {})
        min_rr = float(input_data["config"].get("risk", {}).get("min_rr_ratio", 2.0))
        symbol = input_data["symbol"]
        darvas = input_data["pattern_result"]["darvas_box"]
        trend = input_data["trend_result"]
        risk = input_data["risk_result"]
        discipline = input_data["discipline_result"]
        bearish = input_data["bearish_evidence"]
        score = float(input_data["score_result"].get("score", 0))
        doctrine_reviews = input_data.get("doctrine_reviews", {})

        blockers: list[str] = []
        if not risk.get("stop_loss"):
            blockers.append("缺少清晰止损参考")
        if darvas.get("chase_risk"):
            blockers.append("买点距离过远")
        if float(risk.get("rr_ratio") or 0) < min_rr:
            blockers.append("风险收益比低于配置要求")
        if not darvas.get("breakout_signal"):
            blockers.append("没有有效箱体突破信号")
        if not trend.get("trend_ok"):
            blockers.append("趋势条件不完整")
        if input_data.get("serious_risk"):
            blockers.append("Bear Case 标记严重风险")
        if discipline.get("fomo_risk"):
            blockers.append("纪律检查标记 FOMO")
        doctrine_rejects = [review.get("name", name) for name, review in doctrine_reviews.items() if review.get("verdict") == "reject"]
        doctrine_waits = [review.get("name", name) for name, review in doctrine_reviews.items() if review.get("verdict") == "wait"]
        if doctrine_rejects:
            blockers.append("流派审查存在拒绝项：" + "、".join(doctrine_rejects))
        if doctrine_waits:
            blockers.append("流派审查仍需等待：" + "、".join(doctrine_waits))

        if score >= 75 and not blockers:
            decision_status = "可关注"
            confidence = "高"
        elif score >= 60:
            decision_status = "等待"
            confidence = "中"
        elif score >= 40:
            decision_status = "观察"
            confidence = "中"
        else:
            decision_status = "放弃"
            confidence = "低"

        if blockers and decision_status == "可关注":
            decision_status = "等待"
        if darvas.get("chase_risk") and decision_status == "可关注":
            decision_status = "等待"
        if input_data.get("serious_risk") and decision_status in {"可关注", "等待"}:
            decision_status = "观察"
        if doctrine_waits and decision_status == "可关注":
            decision_status = "等待"
        if doctrine_rejects and decision_status in {"可关注", "等待"}:
            decision_status = "观察"
        if len(doctrine_rejects) >= 2 and score < 60:
            decision_status = "放弃"
        if "趋势条件不完整" in blockers and score < 60:
            decision_status = "观察" if score >= 40 else "放弃"

        output = {
            "symbol": symbol,
            "decision_status": decision_status,
            "confidence_level": confidence,
            "why_this_status": self._why_status(decision_status, score, blockers),
            "why_not_higher_status": "更高等级被限制，原因是：" + ("；".join(blockers) if blockers else "仍需人工确认与次日复核。"),
            "key_positive_factors": input_data.get("bullish_evidence", []),
            "key_negative_factors": bearish,
            "doctrine_summary": doctrine_reviews,
            "risk_flags": risk.get("risk_flags", []),
            "discipline_flags": discipline.get("discipline_flags", []),
            "invalid_conditions": [
                "跌回箱体内部",
                "跌破突破日低点或关键均线",
                "成交量放大但价格无法继续走强",
                "原有箱体或趋势条件消失",
            ],
            "human_review_required": bool(config.get("require_human_review", True)),
        }
        if output["decision_status"] not in VALID_DECISION_STATUSES:
            return SubagentResult(self.name, "failed", errors=["Invalid decision status"])
        return SubagentResult(self.name, "success", {"decision_result": output})

    @staticmethod
    def _why_status(status: str, score: float, blockers: list[str]) -> str:
        if blockers:
            return f"当前评分 {score:.1f}，但存在限制项：{'；'.join(blockers)}。"
        return f"当前评分 {score:.1f}，结构条件暂未触发硬性降级。"
