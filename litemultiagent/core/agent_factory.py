from typing import Dict, Any
from litemultiagent.agents.atomic import AtomicAgent
from litemultiagent.agents.composite import CompositeAgent
from litemultiagent.agents.base import BaseAgent

class AgentFactory:
    @staticmethod
    def create_agent(config: Dict[str, Any]) -> BaseAgent:
        agent_type = config["type"]
        agent_name = config["name"]
        meta_data = config.get("meta_data")
        # meta_task_id = config.get("meta_task_id")
        # task_id = config.get("task_id")
        tools = config.get("tools", [])
        agent_description = config["agent_description"]
        parameter_description = config["parameter_description"]

        if agent_type == "atomic":
            return AtomicAgent(agent_name, agent_description, parameter_description, tools, meta_data)
        elif agent_type == "composite":
            sub_agent_configs = config.get("sub_agents", [])
            return CompositeAgent(agent_name, agent_description, parameter_description, sub_agent_configs, tools, meta_data)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")