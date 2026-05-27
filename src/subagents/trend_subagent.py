from src.strategy.trend_rules import evaluate_trend
from src.subagents.base import BaseSubagent, SubagentResult


class TrendSubagent(BaseSubagent):
    name = "TrendSubagent"

    def run(self, input_data):
        trend = evaluate_trend(input_data["bars"], input_data["config"].get("trend", {}))
        return SubagentResult(self.name, "success", {"trend_result": trend})
