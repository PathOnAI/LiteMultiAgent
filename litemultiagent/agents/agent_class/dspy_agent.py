from typing import List, Dict, Any, Callable
from .base import BaseAgent
from dspy.predict.react import ReAct, Tool
from litemultiagent.tools.registry import ToolRegistry
import dspy

class DSPyAgent(BaseAgent):
    def __init__(self, agent_name: str, system_prompt, agent_description, parameter_description, tools: List[Dict[str, Any]], available_tools: Dict[str, Callable], meta_data):
        super().__init__(agent_name, system_prompt, agent_description, parameter_description, tools, available_tools, meta_data)
        self.system_prompt = system_prompt
        self._agent = self._build_agent()

    def _build_agent(self) -> dspy.Module:
            """Build the agent workflow using dspy
            Can be expanded to build more complex workflows, using multiple signatures and modules
            """
            # TODO: tools needs to be loaded properly instead of loading everything
            return dspy.ReAct(signature="goal -> result",
                                    tools=[Tool(func=tool.func, name=tool.name, desc=tool.description, args=tool.parameters) for tool in ToolRegistry.get_all_tools().values()])

    def send_prompt(self, goal: str) -> str:
        # TODO: model_name needs to be passed
        with dspy.settings.context(lm=dspy.LM('openai/gpt-4o-mini'), system_propmt=self.system_prompt):
            res = self._agent(goal=goal).result
        return res
