from src.subagents.base import BaseSubagent, SubagentResult
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

RUNTIME_SUBAGENT_ORDER = [
    "MarketDataSubagent",
    "IndicatorSubagent",
    "PatternDetectionSubagent",
    "TrendSubagent",
    "MarketRegimeSubagent",
    "TechnicalThesisSubagent",
    "BullCaseSubagent",
    "BearCaseSubagent",
    "RiskSubagent",
    "DisciplineSubagent",
    "DarvasDoctrineSubagent",
    "SperandeoPrinciplesSubagent",
    "LivermoreTapeReadingSubagent",
    "ScoringSubagent",
    "DecisionCommitteeSubagent",
    "TradingSkillSubagent",
    "ReportSubagent",
    "HumanApprovalGate",
]

SUBAGENT_RESPONSIBILITIES = {
    "MarketDataSubagent": "获取日线数据、统一字段、检查缺失，不做策略判断。",
    "IndicatorSubagent": "计算均线、成交量均线、量比和最近指标快照。",
    "PatternDetectionSubagent": "识别达瓦斯箱体、箱体突破，并预留 1-2-3 与 2B 接口。",
    "TrendSubagent": "判断趋势、均线结构、阶段高位接近程度。",
    "MarketRegimeSubagent": "读取市场环境研究上下文，给出市场和板块环境摘要。",
    "TechnicalThesisSubagent": "只说明技术结构是否符合系统。",
    "BullCaseSubagent": "寻找支持进入观察池的结构化证据。",
    "BearCaseSubagent": "寻找反对理由和风险，防止过度乐观。",
    "RiskSubagent": "计算止损参考、风险收益比、买点距离和风险标签。",
    "DisciplineSubagent": "检查交易纪律、FOMO、止损清晰度和趋势幻想。",
    "DarvasDoctrineSubagent": "按达瓦斯箱体流派审查选股结构、行情配合和舆论上下文。",
    "SperandeoPrinciplesSubagent": "按专业投机原则审查趋势定义、风险参考和风险收益比。",
    "LivermoreTapeReadingSubagent": "按股票大作手回忆录风格审查关键价位、市场配合和情绪风险。",
    "ScoringSubagent": "给出 0-100 排序分，不代表交易指令。",
    "DecisionCommitteeSubagent": "汇总多方审查，输出辅助状态和降级理由。",
    "TradingSkillSubagent": "生成可复制给 LLM 的分析 Prompt，不调用 OpenAI API。",
    "ReportSubagent": "生成每日 Markdown 报告。",
    "HumanApprovalGate": "提示人工最终确认，不把辅助状态升级为真实交易动作。",
}

__all__ = [
    "BaseSubagent",
    "SubagentResult",
    "RUNTIME_SUBAGENT_ORDER",
    "SUBAGENT_RESPONSIBILITIES",
]
