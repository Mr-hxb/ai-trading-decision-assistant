from __future__ import annotations

from typing import Any

from src.subagents.base import BaseSubagent, SubagentResult


class DoctrineSubagent(BaseSubagent):
    doctrine_name: str

    def _build_result(
        self,
        verdict: str,
        score: float,
        selection_view: str,
        market_view: str,
        sentiment_view: str,
        evidence: list[str],
        blockers: list[str],
        trigger_conditions: list[str],
        invalid_conditions: list[str],
        risk_notes: list[str],
    ) -> SubagentResult:
        payload = {
            "name": self.doctrine_name,
            "verdict": verdict,
            "score": round(score, 2),
            "selection_view": selection_view,
            "market_view": market_view,
            "sentiment_view": sentiment_view,
            "evidence": evidence,
            "blockers": blockers,
            "trigger_conditions": trigger_conditions,
            "invalid_conditions": invalid_conditions,
            "risk_notes": risk_notes,
        }
        return SubagentResult(self.name, "success", {"doctrine_reviews": {self.name: payload}})

    @staticmethod
    def _sentiment_view(input_data: dict[str, Any]) -> tuple[str, list[str], list[str]]:
        research_context = input_data.get("research_context") or {}
        news_items = research_context.get("news_items") if isinstance(research_context.get("news_items"), list) else []
        company_events = research_context.get("company_events") if isinstance(research_context.get("company_events"), list) else []
        summary = research_context.get("sentiment_summary")
        evidence: list[str] = []
        blockers: list[str] = []
        if summary:
            evidence.append(f"舆论摘要：{summary}")
        if company_events:
            evidence.append(f"已提供 {len(company_events)} 条公司公告/事件上下文。")
        negative_count = sum(1 for item in news_items if str(item.get("sentiment", "")).lower() == "negative")
        positive_count = sum(1 for item in news_items if str(item.get("sentiment", "")).lower() == "positive")
        if positive_count:
            evidence.append(f"主流新闻正向条目 {positive_count} 条。")
        if negative_count:
            blockers.append(f"主流新闻负向条目 {negative_count} 条。")
        if not evidence and not blockers:
            return "未提供官方公告或主流新闻上下文。", evidence, blockers
        return summary or "已提供官方公告或主流新闻上下文。", evidence, blockers

    @staticmethod
    def _market_view(input_data: dict[str, Any]) -> tuple[str, list[str], list[str]]:
        market = input_data.get("market_regime", {})
        summary = market.get("summary", "未提供市场环境研究上下文。")
        evidence: list[str] = []
        blockers: list[str] = []
        if market.get("risk_level") == "supportive":
            evidence.append("市场风险偏好支持当前方向。")
        elif market.get("risk_level") == "unfavorable":
            blockers.append("市场风险偏好不配合。")
        elif not market.get("context_provided"):
            blockers.append("市场环境上下文缺失，置信度降低。")
        return summary, evidence, blockers


class DarvasDoctrineSubagent(DoctrineSubagent):
    name = "DarvasDoctrineSubagent"
    doctrine_name = "Darvas Box"

    def run(self, input_data: dict[str, Any]) -> SubagentResult:
        darvas = input_data["pattern_result"]["darvas_box"]
        trend = input_data["trend_result"]
        market_view, market_evidence, market_blockers = self._market_view(input_data)
        sentiment_view, sentiment_evidence, sentiment_blockers = self._sentiment_view(input_data)

        evidence: list[str] = []
        blockers: list[str] = []
        if trend.get("trend_ok"):
            evidence.append("趋势结构通过均线和阶段高位检查。")
        else:
            blockers.append("趋势结构未完整通过。")
        if darvas.get("has_box"):
            evidence.append("存在可识别箱体结构。")
        else:
            blockers.append("未形成可解释的窄箱体。")
        if darvas.get("breakout_signal"):
            evidence.append("箱体突破和成交量条件同时满足。")
        else:
            blockers.append("未出现有效箱体突破。")
        if darvas.get("chase_risk"):
            blockers.append("价格距离箱体上沿过远，追高风险偏高。")
        if not darvas.get("volume_breakout"):
            blockers.append("成交量未达到突破确认要求。")

        evidence.extend(market_evidence + sentiment_evidence)
        blockers.extend(market_blockers + sentiment_blockers)
        hard_blockers = [item for item in blockers if "过远" in item or "未出现有效箱体突破" in item or "未形成" in item]
        if darvas.get("breakout_signal") and not hard_blockers:
            verdict = "pass"
            score = 85
        elif darvas.get("has_box") or trend.get("trend_ok"):
            verdict = "wait"
            score = 58
        else:
            verdict = "reject"
            score = 30

        return self._build_result(
            verdict=verdict,
            score=score,
            selection_view="优先寻找强势趋势中的窄箱体和放量突破。",
            market_view=market_view,
            sentiment_view=sentiment_view,
            evidence=evidence,
            blockers=blockers,
            trigger_conditions=["收盘重新站上箱体上沿并放量确认。", "突破后不快速跌回箱体内部。"],
            invalid_conditions=["跌回箱体内部。", "跌破箱体下沿。", "放量后价格无法继续走强。"],
            risk_notes=["箱体上沿距离过远时不升级辅助状态。"],
        )


class SperandeoPrinciplesSubagent(DoctrineSubagent):
    name = "SperandeoPrinciplesSubagent"
    doctrine_name = "Sperandeo Principles"

    def run(self, input_data: dict[str, Any]) -> SubagentResult:
        trend = input_data["trend_result"]
        risk = input_data["risk_result"]
        min_rr = float(input_data["config"].get("risk", {}).get("min_rr_ratio", 2.0))
        market_view, market_evidence, market_blockers = self._market_view(input_data)
        sentiment_view, sentiment_evidence, sentiment_blockers = self._sentiment_view(input_data)

        evidence: list[str] = []
        blockers: list[str] = []
        if trend.get("trend_ok"):
            evidence.append("趋势定义通过，未逆主要方向。")
        else:
            blockers.append("趋势定义不完整，不能按趋势延续处理。")
        if risk.get("stop_loss"):
            evidence.append(f"存在清晰风险参考：{risk.get('stop_loss_reason')}。")
        else:
            blockers.append("缺少清晰风险参考。")
        if float(risk.get("rr_ratio") or 0) >= min_rr:
            evidence.append("风险收益比达到配置要求。")
        else:
            blockers.append("风险收益比低于配置要求。")

        evidence.extend(market_evidence + sentiment_evidence)
        blockers.extend(market_blockers + sentiment_blockers)
        if trend.get("trend_ok") and risk.get("stop_loss") and float(risk.get("rr_ratio") or 0) >= min_rr and not market_blockers:
            verdict = "pass"
            score = 82
        elif risk.get("stop_loss"):
            verdict = "wait"
            score = 55
        else:
            verdict = "reject"
            score = 25

        return self._build_result(
            verdict=verdict,
            score=score,
            selection_view="优先选择趋势清晰、风险参考明确、风险收益比达标的结构。",
            market_view=market_view,
            sentiment_view=sentiment_view,
            evidence=evidence,
            blockers=blockers,
            trigger_conditions=["趋势条件重新完整通过。", "风险收益比重新达到配置要求。"],
            invalid_conditions=["跌破关键均线或最近结构低点。", "风险收益比恶化到配置要求以下。"],
            risk_notes=["无清晰风险参考时不能提高辅助状态。"],
        )


class LivermoreTapeReadingSubagent(DoctrineSubagent):
    name = "LivermoreTapeReadingSubagent"
    doctrine_name = "Livermore Tape Reading"

    def run(self, input_data: dict[str, Any]) -> SubagentResult:
        latest = input_data["bars"].iloc[-1].to_dict()
        trend = input_data["trend_result"]
        darvas = input_data["pattern_result"]["darvas_box"]
        market_view, market_evidence, market_blockers = self._market_view(input_data)
        sentiment_view, sentiment_evidence, sentiment_blockers = self._sentiment_view(input_data)

        checks = trend.get("checks", {})
        evidence: list[str] = []
        blockers: list[str] = []
        if checks.get("near_stage_high"):
            evidence.append("价格接近阶段关键高位。")
        else:
            blockers.append("尚未接近阶段关键高位。")
        if trend.get("trend_ok"):
            evidence.append("价格行为与主要趋势一致。")
        else:
            blockers.append("价格行为未与主要趋势完全一致。")
        if float(latest.get("volume_ratio") or 0) > 1.2:
            evidence.append("成交量相对近期均量放大。")
        else:
            blockers.append("成交量确认不足。")
        if darvas.get("chase_risk"):
            blockers.append("短线情绪可能过热，追高风险偏高。")

        evidence.extend(market_evidence + sentiment_evidence)
        blockers.extend(market_blockers + sentiment_blockers)
        if trend.get("trend_ok") and checks.get("near_stage_high") and not darvas.get("chase_risk") and not market_blockers:
            verdict = "pass"
            score = 80
        elif trend.get("trend_ok") or checks.get("near_stage_high"):
            verdict = "wait"
            score = 56
        else:
            verdict = "reject"
            score = 28

        return self._build_result(
            verdict=verdict,
            score=score,
            selection_view="优先观察顺大势、接近关键价位且有成交确认的强势标的。",
            market_view=market_view,
            sentiment_view=sentiment_view,
            evidence=evidence,
            blockers=blockers,
            trigger_conditions=["关键价位上方保持强势并有成交确认。", "市场和板块环境继续配合。"],
            invalid_conditions=["跌回关键价位下方。", "市场环境明显转弱。", "成交放大但价格停滞。"],
            risk_notes=["情绪过热或关键价位失败时不提高辅助状态。"],
        )
