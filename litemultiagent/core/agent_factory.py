from typing import Dict, Any, Union
from litemultiagent.agents.agent_type.atomic import AtomicAgent
from litemultiagent.agents.agent_type.composite import CompositeAgent
from litemultiagent.agents.agent_class.base import BaseAgent
from litemultiagent.agents.agent_class.high_level_planning import HighLevelPlanningAgent

class AgentFactory:
    @staticmethod
    def create_agent(config: Dict[str, Any]) -> Union[AtomicAgent, CompositeAgent]:
        agent_type = config["type"]
        agent_name = config["name"]
        agent_class = config["agent_class"]
        agent_description = config["agent_description"]
        parameter_description = config["parameter_description"]
        tools = config.get("tools", [])
        meta_data = config.get("meta_data", {})

        agent_class_map = {
            "BaseAgent": BaseAgent,
            "HighLevelPlanningAgent": HighLevelPlanningAgent
        }

        if agent_class not in agent_class_map:
            raise ValueError(f"Unknown agent class: {agent_class}")

        selected_agent_class = agent_class_map[agent_class]

        if agent_type == "atomic":
            return AtomicAgent(agent_name, agent_description, parameter_description,
                               tools, meta_data, selected_agent_class)
        elif agent_type == "composite":
            sub_agent_configs = config.get("sub_agents", [])
            return CompositeAgent(agent_name, agent_description, parameter_description,
                                  sub_agent_configs, tools, meta_data, selected_agent_class)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")