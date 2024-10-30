from typing import List, Dict, Any, Type
from litemultiagent.agents.agent_class.base import BaseAgent
from litemultiagent.core.agent_system import AgentSystem
from litemultiagent.tools.registry import ToolRegistry


class AtomicAgent:
    def __init__(self, agent_name: str, agent_description: str, parameter_description: str,
                 tool_names: List[str], self_defined_tools, meta_data: Dict[str, Any],
                 agent_class: Type[BaseAgent]):
        tool_registry = ToolRegistry()
        available_tools = {}
        tools = []
        for self_defined_tool in self_defined_tools:
            tool_registry.register(self_defined_tool)
            tool_names.append(self_defined_tool.name)
        for tool_name in tool_names:
            available_tools[tool_name] = tool_registry.get_tool(tool_name).func
            tools.append(tool_registry.get_tool_description(tool_name))

        self.agent = agent_class(agent_name, agent_description, parameter_description,
                                 tools, available_tools, meta_data)

    def execute(self, task: str) -> str:
        return self.agent.send_prompt(task)

    def set_system(self, system: AgentSystem):
        self.agent.set_system(system)

    def __getattr__(self, name):
        return getattr(self.agent, name)

    def __call__(self, task: str) -> str:
        return self.execute(task)