from litemultiagent.agents.base import BaseAgent
from litemultiagent.tools.registry import ToolRegistry
class AtomicAgent(BaseAgent):
    def __init__(self, agent_name: str, agent_description, parameter_description, tool_names: list[str], meta_data):
        tool_registry = ToolRegistry()
        available_tools = {}
        tools = []
        for tool_name in tool_names:
            available_tools[tool_name] = tool_registry.get_tool(tool_name).func
            tools.append(tool_registry.get_tool_description(tool_name))
        super().__init__(agent_name, agent_description, parameter_description, tools, available_tools, meta_data)

    def execute(self, task: str) -> str:
        return self.send_prompt(task)

    def __call__(self, task: str) -> str:
        return self.execute(task)