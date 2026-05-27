from src.runtime.agent_runtime import AgentRuntime


class CrewAIRuntime(AgentRuntime):
    def run_subagent(self, subagent, input_data):
        raise NotImplementedError("TODO: future CrewAI role/task experiment only.")
