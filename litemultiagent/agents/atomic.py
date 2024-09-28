from litemultiagent.agents.base import BaseAgent
from typing import List, Optional
from litemultiagent.tools.registry import ToolRegistry, Tool
class AtomicAgent(BaseAgent):
    def __init__(self, agent_name: str, agent_description, parameter_description, tool_names: List[str], meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        print(tool_names)
        tool_registry = ToolRegistry()
        available_tools = {}
        tools = []
        for tool_name in tool_names:
            available_tools[tool_name] = tool_registry.get_tool(tool_name).func
            tools.append(tool_registry.get_tool_description(tool_name))
        super().__init__(agent_name, agent_description, parameter_description, tools, available_tools, meta_task_id, task_id)

    def execute(self, task: str) -> str:
        return self.send_prompt(task)

    def __call__(self, task: str) -> str:
        return self.execute(task)