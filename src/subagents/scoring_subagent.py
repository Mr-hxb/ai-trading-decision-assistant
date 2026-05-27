from src.strategy.scoring import calculate_score
from src.subagents.base import BaseSubagent, SubagentResult


class ScoringSubagent(BaseSubagent):
    name = "ScoringSubagent"

    def run(self, input_data):
        score = calculate_score(
            input_data["trend_result"],
            input_data["pattern_result"]["darvas_box"],
            input_data["risk_result"],
            input_data["config"].get("scoring", {}),
        )
        return SubagentResult(self.name, "success", {"score_result": score})
