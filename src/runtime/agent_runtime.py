from __future__ import annotations

from typing import Any


class AgentRuntime:
    def run_subagent(self, subagent, input_data: dict[str, Any]):
        raise NotImplementedError
