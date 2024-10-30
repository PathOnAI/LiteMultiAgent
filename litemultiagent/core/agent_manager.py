from typing import Dict, Any, Union
from litemultiagent.agents.agent_type.atomic import AtomicAgent
from litemultiagent.agents.agent_type.composite import CompositeAgent
from litemultiagent.core.agent_factory import AgentFactory

class AgentManager:
    def __init__(self):
        self.agents: Dict[str, Union[AtomicAgent, CompositeAgent]] = {}

    def get_agent(self, config: Dict[str, Any]) -> Union[AtomicAgent, CompositeAgent]:
        agent_name = config['name']
        if agent_name not in self.agents:
            self.agents[agent_name] = AgentFactory.create_agent(config)
        return self.agents[agent_name]

    def execute_task(self, agent_name: str, task: str) -> str:
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found. Create the agent first using get_agent().")
        return self.agents[agent_name].execute(task)