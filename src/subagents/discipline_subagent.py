from src.subagents.base import BaseSubagent, SubagentResult


class DisciplineSubagent(BaseSubagent):
    name = "DisciplineSubagent"

    def run(self, input_data):
        darvas = input_data["pattern_result"]["darvas_box"]
        trend = input_data["trend_result"]
        risk = input_data["risk_result"]
        flags: list[str] = []
        fomo = False
        if darvas.get("chase_risk"):
            flags.append("FOMO: 价格已远离可解释的突破区域。")
            fomo = True
        if not risk.get("stop_loss"):
            flags.append("缺少清晰止损参考。")
        if not trend.get("trend_ok"):
            flags.append("趋势不成立时不能幻想反转。")
        if not darvas.get("breakout_signal"):
            flags.append("没有有效突破信号，不能把观察状态升级。")
        return SubagentResult(self.name, "success", {"discipline_result": {"discipline_flags": flags, "fomo_risk": fomo}})
