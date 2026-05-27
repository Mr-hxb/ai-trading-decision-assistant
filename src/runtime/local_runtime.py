from __future__ import annotations

from typing import Any

from src.runtime.agent_runtime import AgentRuntime


class LocalRuntime(AgentRuntime):
    def run_subagent(self, subagent, input_data: dict[str, Any]):
        return subagent.run(input_data)
