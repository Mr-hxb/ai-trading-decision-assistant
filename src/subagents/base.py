from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


VALID_EXECUTION_STATUSES = {"success", "partial", "failed"}
VALID_DECISION_STATUSES = {"可关注", "等待", "观察", "放弃"}


@dataclass
class SubagentResult:
    name: str
    status: str
    data: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in VALID_EXECUTION_STATUSES:
            raise ValueError(f"Invalid execution status: {self.status}")


class BaseSubagent:
    name: str

    def run(self, input_data: dict[str, Any]) -> SubagentResult:
        raise NotImplementedError
