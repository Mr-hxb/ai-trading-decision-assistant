from src.subagents.base import BaseSubagent, SubagentResult


class TechnicalThesisSubagent(BaseSubagent):
    name = "TechnicalThesisSubagent"

    def run(self, input_data):
        symbol = input_data["symbol"]
        darvas = input_data["pattern_result"]["darvas_box"]
        trend = input_data["trend_result"]
        parts = []
        if trend.get("trend_ok"):
            parts.append("趋势结构通过均线与阶段高位检查。")
        else:
            parts.append("趋势结构仍有未满足项，需要降低评级。")
        if darvas.get("breakout_signal"):
            parts.append("达瓦斯箱体出现放量突破信号。")
        elif darvas.get("has_box"):
            parts.append("存在箱体结构，但尚未出现有效突破信号。")
        else:
            parts.append("当前箱体结构不充分。")
        thesis = f"{symbol}: " + "".join(parts)
        return SubagentResult(self.name, "success", {"technical_thesis": thesis})
