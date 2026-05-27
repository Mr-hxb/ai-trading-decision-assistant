from src.subagents.base import BaseSubagent, SubagentResult


class BearCaseSubagent(BaseSubagent):
    name = "BearCaseSubagent"

    def run(self, input_data):
        darvas = input_data["pattern_result"]["darvas_box"]
        trend = input_data["trend_result"]
        bearish: list[str] = []
        serious = False
        if not trend.get("trend_ok"):
            bearish.append("趋势条件不完整，可能不符合趋势优先原则。")
            serious = True
        if not darvas.get("breakout_signal"):
            bearish.append("未出现有效箱体突破信号。")
        if darvas.get("chase_risk"):
            bearish.append("价格已远离箱体上沿，存在 FOMO 风险。")
            serious = True
        if not darvas.get("volume_breakout"):
            bearish.append("成交量未达到突破确认要求。")
        return SubagentResult(self.name, "success", {"bearish_evidence": bearish, "serious_risk": serious})
