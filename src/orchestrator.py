from __future__ import annotations

from pathlib import Path
from typing import Any

from src.config_loader import PROJECT_ROOT, load_project_env, load_strategy_config
from src.data.akshare_provider import AkshareProvider
from src.data.base import MarketDataProvider
from src.data.eodhd_provider import EodhdProvider
from src.data.mock_provider import MockProvider
from src.research_context import get_research_context
from src.runtime.local_runtime import LocalRuntime
from src.subagents import RUNTIME_SUBAGENT_ORDER
from src.subagents.bear_case_subagent import BearCaseSubagent
from src.subagents.bull_case_subagent import BullCaseSubagent
from src.subagents.decision_committee_subagent import DecisionCommitteeSubagent
from src.subagents.doctrine_subagents import DarvasDoctrineSubagent, LivermoreTapeReadingSubagent, SperandeoPrinciplesSubagent
from src.subagents.discipline_subagent import DisciplineSubagent
from src.subagents.human_approval_gate import HumanApprovalGate
from src.subagents.indicator_subagent import IndicatorSubagent
from src.subagents.market_regime_subagent import MarketRegimeSubagent
from src.subagents.market_data_subagent import MarketDataSubagent
from src.subagents.pattern_detection_subagent import PatternDetectionSubagent
from src.subagents.report_subagent import ReportSubagent
from src.subagents.risk_subagent import RiskSubagent
from src.subagents.scoring_subagent import ScoringSubagent
from src.subagents.technical_thesis_subagent import TechnicalThesisSubagent
from src.subagents.trading_skill_subagent import TradingSkillSubagent
from src.subagents.trend_subagent import TrendSubagent


def build_provider(provider_name: str, adjust: str | None = None) -> MarketDataProvider:
    if provider_name == "mock":
        return MockProvider()
    if provider_name == "akshare":
        return AkshareProvider(adjust=adjust or "qfq")
    if provider_name == "eodhd":
        return EodhdProvider()
    raise ValueError(f"Unsupported provider for MVP: {provider_name}")


class Orchestrator:
    def __init__(
        self,
        provider: MarketDataProvider,
        runtime: LocalRuntime | None = None,
        config: dict[str, Any] | None = None,
        project_root: Path | None = None,
    ) -> None:
        load_project_env()
        self.provider = provider
        self.runtime = runtime or LocalRuntime()
        self.config = config or load_strategy_config()
        self.project_root = project_root or PROJECT_ROOT

    def run_scan(
        self,
        symbols: list[str],
        start_date: str,
        end_date: str,
        research_contexts: dict[str, dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        successes: list[dict[str, Any]] = []
        failed: list[dict[str, str]] = []
        per_symbol_results: dict[str, Any] = {}

        for symbol in symbols:
            context: dict[str, Any] = {
                "symbol": symbol,
                "start_date": start_date,
                "end_date": end_date,
                "config": self.config,
                "research_context": get_research_context(research_contexts or {}, symbol),
                "subagent_results": {},
            }
            symbol_failed = False
            for subagent in self._symbol_subagents():
                result = self.runtime.run_subagent(subagent, context)
                context["subagent_results"][result.name] = result
                if result.status == "failed":
                    failed.append({"symbol": symbol, "reason": "; ".join(result.errors) or f"{result.name} failed"})
                    symbol_failed = True
                    break
                result_data = dict(result.data)
                if "doctrine_reviews" in result_data:
                    context.setdefault("doctrine_reviews", {}).update(result_data.pop("doctrine_reviews"))
                context.update(result_data)
            per_symbol_results[symbol] = context
            if not symbol_failed:
                successes.append(context)

        report_result = self.runtime.run_subagent(
            ReportSubagent(self.project_root),
            {
                "report_date": end_date,
                "analysis_results": successes,
                "failed_symbols": failed,
                "subagent_order": RUNTIME_SUBAGENT_ORDER,
            },
        )
        human_gate_result = self.runtime.run_subagent(HumanApprovalGate(), {"report_path": report_result.data.get("report_path")})
        return {
            "successful_symbols": [item["symbol"] for item in successes],
            "failed_symbols": failed,
            "report_path": report_result.data.get("report_path"),
            "human_gate": human_gate_result.data.get("human_gate"),
            "per_symbol_results": per_symbol_results,
            "report_result": report_result,
            "human_gate_result": human_gate_result,
        }

    def _symbol_subagents(self):
        return [
            MarketDataSubagent(self.provider),
            IndicatorSubagent(),
            PatternDetectionSubagent(),
            TrendSubagent(),
            MarketRegimeSubagent(),
            TechnicalThesisSubagent(),
            BullCaseSubagent(),
            BearCaseSubagent(),
            RiskSubagent(),
            DisciplineSubagent(),
            DarvasDoctrineSubagent(),
            SperandeoPrinciplesSubagent(),
            LivermoreTapeReadingSubagent(),
            ScoringSubagent(),
            DecisionCommitteeSubagent(),
            TradingSkillSubagent(),
        ]
