from typing import List, Dict, Any, Type
from litemultiagent.agents.agent_class.base import BaseAgent
from litemultiagent.tools.registry import ToolRegistry, Tool

class CompositeAgent:
    def __init__(self, agent_name: str, agent_description: str, parameter_description: str,
                 sub_agent_configs: List[Dict[str, Any]], tool_names: List[str], self_defined_tools, meta_data: Dict[str, Any],
                 agent_class: Type[BaseAgent]):
        self.available_tools = {}
        self.tools = []

        for self_defined_tool in self_defined_tools:
            tool_registry.register(self_defined_tool)
            tool_names.append(self_defined_tool.name)

        for tool_name in tool_names:
            self.available_tools[tool_name] = ToolRegistry.get_tool(tool_name).func
            self.tools.append(ToolRegistry.get_tool_description(tool_name))

        self.sub_agents = self._build_sub_agents(sub_agent_configs)
        self._register_sub_agents_as_tools()

        self.agent = agent_class(agent_name, agent_description, parameter_description,
                                 self.tools, self.available_tools, meta_data)

    def set_shared_config(self, shared_config):
        self.agent.set_shared_config(shared_config)
        for sub_agent in self.sub_agents:
            sub_agent.set_shared_config(shared_config)

    def _build_sub_agents(self, sub_agent_configs: List[Dict[str, Any]]) -> List[BaseAgent]:
        from litemultiagent.core.agent_factory import AgentFactory
        return [AgentFactory.create_agent(config) for config in sub_agent_configs]

    def _register_sub_agents_as_tools(self):
        for sub_agent in self.sub_agents:
            ToolRegistry.register(Tool(
                sub_agent.agent_name,
                sub_agent,
                sub_agent.agent_description,
                {
                    "task": {
                        "type": "string",
                        "description": sub_agent.parameter_description,
                        "required": True
                    }
                }
            ))
        self.tools.extend([ToolRegistry.get_tool_description(sub_agent.agent_name) for sub_agent in self.sub_agents])
        self.available_tools.update({sub_agent.agent_name: sub_agent for sub_agent in self.sub_agents})

    def execute(self, task: str) -> str:
        return self.agent.send_prompt(task)

    def __getattr__(self, name):
        return getattr(self.agent, name)

    def __call__(self, task: str) -> str:
        return self.execute(task)