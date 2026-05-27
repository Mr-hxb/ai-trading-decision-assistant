from pathlib import Path

from src.reports.daily_report import generate_daily_report
from src.subagents.base import BaseSubagent, SubagentResult


class ReportSubagent(BaseSubagent):
    name = "ReportSubagent"

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def run(self, input_data):
        path = generate_daily_report(
            project_root=self.project_root,
            report_date=input_data["report_date"],
            analysis_results=input_data["analysis_results"],
            failed_symbols=input_data.get("failed_symbols", []),
            subagent_order=input_data.get("subagent_order", []),
        )
        return SubagentResult(self.name, "success", {"report_path": str(path)})
