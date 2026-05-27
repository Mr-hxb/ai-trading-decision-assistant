from src.subagents.base import BaseSubagent, SubagentResult


class BullCaseSubagent(BaseSubagent):
    name = "BullCaseSubagent"

    def run(self, input_data):
        darvas = input_data["pattern_result"]["darvas_box"]
        trend = input_data["trend_result"]
        evidence: list[str] = []
        if trend.get("trend_ok"):
            evidence.append("趋势检查通过，可作为进入观察池的正向证据。")
        if darvas.get("has_box"):
            evidence.append("存在可识别箱体结构。")
        if darvas.get("breakout_signal"):
            evidence.append("突破信号与成交量条件同时满足。")
        if not evidence:
            evidence.append("暂未形成足够正向结构证据。")
        return SubagentResult(self.name, "success", {"bullish_evidence": evidence})
