from typing import Dict, Any, Union
from litemultiagent.agents.agent_type.atomic import AtomicAgent
from litemultiagent.agents.agent_type.composite import CompositeAgent
from litemultiagent.agents.agent_class.function_calling import FunctionCallingAgent
from litemultiagent.agents.agent_class.high_level_planning import HighLevelPlanningAgent
from litemultiagent.agents.agent_class.react import ReActAgent
class AgentFactory:
    @staticmethod
    def create_agent(config: Dict[str, Any]) -> Union[AtomicAgent, CompositeAgent]:
        agent_type = config["type"]
        agent_name = config["name"]
        agent_class = config["agent_class"]
        system_prompt = config["system_prompt"]
        agent_description = config["agent_description"]
        parameter_description = config["parameter_description"]
        tool_names = config.get("tool_names", [])
        self_defined_tools = config.get("self_defined_tools", [])
        meta_data = config.get("meta_data", {})

        agent_class_map = {
            "FunctionCallingAgent": FunctionCallingAgent,
            "HighLevelPlanningAgent": HighLevelPlanningAgent,
            "ReActAgent": ReActAgent
        }

        if agent_class not in agent_class_map:
            raise ValueError(f"Unknown agent class: {agent_class}")

        selected_agent_class = agent_class_map[agent_class]

        if agent_type == "atomic":
            return AtomicAgent(agent_name, system_prompt, agent_description, parameter_description,
                               tool_names, self_defined_tools, meta_data, selected_agent_class)
        elif agent_type == "composite":
            sub_agent_configs = config.get("sub_agents", [])
            return CompositeAgent(agent_name, system_prompt, agent_description, parameter_description,
                                  sub_agent_configs, tool_names, self_defined_tools, meta_data, selected_agent_class)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")