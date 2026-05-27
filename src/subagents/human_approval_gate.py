from src.subagents.base import BaseSubagent, SubagentResult


class HumanApprovalGate(BaseSubagent):
    name = "HumanApprovalGate"

    def run(self, input_data):
        return SubagentResult(
            self.name,
            "success",
            {
                "human_gate": {
                    "human_review_required": True,
                    "message": "最终交易决策由使用者自行判断；系统只输出辅助状态，不触发交易。",
                    "report_path": input_data.get("report_path"),
                }
            },
        )
