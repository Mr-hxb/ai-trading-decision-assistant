from src.runtime.agent_runtime import AgentRuntime


class OpenAIAgentsRuntime(AgentRuntime):
    def run_subagent(self, subagent, input_data):
        raise NotImplementedError("TODO: future OpenAI Agents SDK handoff, guardrails, and tracing integration only.")
