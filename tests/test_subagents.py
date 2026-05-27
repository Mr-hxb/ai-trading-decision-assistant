from src.data.mock_provider import MockProvider
from src.subagents.base import SubagentResult
from src.subagents.bear_case_subagent import BearCaseSubagent
from src.subagents.bull_case_subagent import BullCaseSubagent
from src.subagents.decision_committee_subagent import DecisionCommitteeSubagent
from src.subagents.doctrine_subagents import DarvasDoctrineSubagent, LivermoreTapeReadingSubagent, SperandeoPrinciplesSubagent
from src.subagents.discipline_subagent import DisciplineSubagent
from src.subagents.indicator_subagent import IndicatorSubagent
from src.subagents.market_regime_subagent import MarketRegimeSubagent
from src.subagents.market_data_subagent import MarketDataSubagent
from src.subagents.pattern_detection_subagent import PatternDetectionSubagent
from src.subagents.risk_subagent import RiskSubagent
from src.subagents.scoring_subagent import ScoringSubagent
from src.subagents.technical_thesis_subagent import TechnicalThesisSubagent
from src.subagents.trading_skill_subagent import TradingSkillSubagent
from src.subagents.trend_subagent import TrendSubagent
from src.config_loader import load_strategy_config


def test_runtime_subagents_return_subagent_result():
    context = {"symbol": "AAPL", "start_date": "2024-01-01", "end_date": "2026-05-25", "config": load_strategy_config()}
    subagents = [
        MarketDataSubagent(MockProvider()),
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
    for subagent in subagents:
        result = subagent.run(context)
        assert isinstance(result, SubagentResult)
        assert result.status in {"success", "partial", "failed"}
        assert isinstance(result.warnings, list)
        assert isinstance(result.errors, list)
        assert result.status == "success"
        context.update(result.data)
