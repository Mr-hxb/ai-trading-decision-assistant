from src.runtime.agent_runtime import AgentRuntime


class LangGraphRuntime(AgentRuntime):
    def run_subagent(self, subagent, input_data):
        raise NotImplementedError("TODO: future LangGraph state graph integration only.")
