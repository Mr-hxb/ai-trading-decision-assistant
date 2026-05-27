from src.strategy.risk_rules import calculate_risk
from src.subagents.base import BaseSubagent, SubagentResult


class RiskSubagent(BaseSubagent):
    name = "RiskSubagent"

    def run(self, input_data):
        darvas = input_data["pattern_result"]["darvas_box"]
        risk = calculate_risk(input_data["bars"], darvas)
        if darvas.get("chase_risk"):
            risk.setdefault("risk_flags", []).append("买点距离过远")
        return SubagentResult(self.name, "success", {"risk_result": risk})
