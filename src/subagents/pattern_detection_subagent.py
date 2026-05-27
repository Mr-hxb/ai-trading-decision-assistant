from src.indicators.box_detection import detect_darvas_box
from src.strategy.darvas_box import evaluate_darvas_setup
from src.subagents.base import BaseSubagent, SubagentResult


class PatternDetectionSubagent(BaseSubagent):
    name = "PatternDetectionSubagent"

    def run(self, input_data):
        config = input_data["config"].get("darvas", {})
        bars = detect_darvas_box(
            input_data["bars"],
            lookback_days=int(config.get("lookback_days", 40)),
            max_range_pct=float(config.get("max_range_pct", 0.15)),
            breakout_volume_ratio=float(config.get("breakout_volume_ratio", 1.5)),
        )
        darvas = evaluate_darvas_setup(bars, config)
        return SubagentResult(
            self.name,
            "success",
            {
                "bars": bars,
                "pattern_result": {
                    "darvas_box": darvas,
                    "one_two_three_reversal": {"status": "TODO", "detected": False},
                    "two_b_false_breakout": {"status": "TODO", "detected": False},
                },
            },
        )
