from src.data.mock_provider import MockProvider
from src.orchestrator import Orchestrator
from src.skill.prompt_builder import build_trading_skill_prompt


def test_prompt_contains_required_sections():
    result = Orchestrator(MockProvider()).run_scan(["AAPL"], "2024-01-01", "2026-05-25")
    context = result["per_symbol_results"]["AAPL"]
    prompt = build_trading_skill_prompt(context)
    for text in ["达瓦斯箱体", "买点", "止损", "FOMO", "风险收益比", "Bull Case", "Bear Case", "不构成投资建议"]:
        assert text in prompt
