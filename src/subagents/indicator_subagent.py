from src.indicators.moving_average import add_moving_averages
from src.indicators.volume import add_volume_indicators
from src.subagents.base import BaseSubagent, SubagentResult


class IndicatorSubagent(BaseSubagent):
    name = "IndicatorSubagent"

    def run(self, input_data):
        bars = input_data["bars"]
        with_ma = add_moving_averages(bars)
        enriched = add_volume_indicators(with_ma)
        return SubagentResult(self.name, "success", {"bars": enriched, "latest": enriched.iloc[-1].to_dict()})
