from src.skill.prompt_builder import build_trading_skill_prompt
from src.subagents.base import BaseSubagent, SubagentResult


class TradingSkillSubagent(BaseSubagent):
    name = "TradingSkillSubagent"

    def run(self, input_data):
        prompt = build_trading_skill_prompt(input_data)
        return SubagentResult(self.name, "success", {"trading_skill_prompt": prompt})
