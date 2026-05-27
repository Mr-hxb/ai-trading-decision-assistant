from __future__ import annotations

from typing import Any

from src.subagents.base import BaseSubagent, SubagentResult


class MarketRegimeSubagent(BaseSubagent):
    name = "MarketRegimeSubagent"

    def run(self, input_data: dict[str, Any]) -> SubagentResult:
        symbol = input_data["symbol"]
        research_context = input_data.get("research_context") or {}
        market_context = research_context.get("market_context") if isinstance(research_context.get("market_context"), dict) else {}
        inferred_market = market_context.get("market") or self._infer_market(symbol)
        proxies = market_context.get("proxies") or self._default_proxies(inferred_market)
        summary = market_context.get("summary") or "未提供市场环境研究上下文。"
        risk_appetite = market_context.get("risk_appetite") or "unknown"
        trend = market_context.get("trend") or "unknown"
        sector_proxy = market_context.get("sector_proxy")

        risk_level = "unknown"
        if str(risk_appetite).lower() in {"positive", "risk_on", "strong"}:
            risk_level = "supportive"
        elif str(risk_appetite).lower() in {"negative", "risk_off", "weak"}:
            risk_level = "unfavorable"
        elif str(risk_appetite).lower() in {"neutral", "mixed"}:
            risk_level = "neutral"

        result = {
            "market": inferred_market,
            "proxies": proxies,
            "sector_proxy": sector_proxy,
            "summary": summary,
            "risk_appetite": risk_appetite,
            "trend": trend,
            "risk_level": risk_level,
            "context_provided": bool(market_context),
        }
        warnings = [] if market_context else ["Market research context was not provided; market regime is unknown."]
        return SubagentResult(self.name, "success", {"market_regime": result}, warnings=warnings)

    @staticmethod
    def _infer_market(symbol: str) -> str:
        normalized = symbol.strip().upper()
        if normalized.endswith(".HK") or normalized.isdigit() and len(normalized) == 5:
            return "hk"
        if normalized.endswith((".SH", ".SZ", ".BJ")) or normalized.isdigit() and len(normalized) == 6:
            return "cn"
        return "us"

    @staticmethod
    def _default_proxies(market: str) -> list[str]:
        if market == "hk":
            return ["HSI", "HSTECH"]
        if market == "cn":
            return ["000001.SH", "399300.SZ", "399006.SZ"]
        return ["SPY", "QQQ"]
