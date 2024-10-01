from litemultiagent.agents.base import BaseAgent
from litemultiagent.tools.registry import ToolRegistry, Tool
from typing import List, Dict, Any, Optional

class CompositeAgent(BaseAgent):
    def __init__(self, agent_name: str, agent_description, parameter_description, sub_agent_configs: List[Dict[str, Any]], tool_names: List[str], meta_data):
        self.available_tools = {}

        self.tools = []

        for tool_name in tool_names:
            self.available_tools[tool_name] = ToolRegistry.get_tool(tool_name).func
            self.tools.append(ToolRegistry.get_tool_description(tool_name))

        self.sub_agents = self._build_sub_agents(sub_agent_configs)

        self._register_sub_agents_as_tools()

        super().__init__(agent_name, agent_description, parameter_description, self.tools, self.available_tools, meta_data)


    def _build_sub_agents(self, sub_agent_configs: List[Dict[str, Any]]) -> List[BaseAgent]:
        from litemultiagent.core.agent_factory import AgentFactory  # Import here to avoid circular dependency
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
        # Update the tools and available_tools after registering sub-agents
        self.tools.extend([self.tool_registry.get_tool_description(sub_agent.agent_name) for sub_agent in self.sub_agents])
        self.available_tools.update({sub_agent.agent_name: sub_agent for sub_agent in self.sub_agents})

    def execute(self, task: str) -> str:
        # Implementation of task execution using sub-agents
        # This could involve breaking down the task and delegating to sub-agents
        return self.send_prompt(task)

    def __call__(self, task: str) -> str:
        return self.execute(task)