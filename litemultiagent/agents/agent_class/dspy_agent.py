from typing import List, Dict, Any, Callable
from .base import BaseAgent
from dspy.predict.react import ReAct, Tool
from litemultiagent.tools.registry import ToolRegistry
import dspy


class Edvidence(dspy.Signature):
    """Extract key evidence from a statement based on the goal."""
    statement: str = dspy.InputField(desc="The statement to be evaluated")
    goal: str = dspy.InputField(desc="The goal of the statement")
    evidence: str = dspy.OutputField(desc="The evidence extracted from the statement")

class Judgement(dspy.Signature):
    """Give the score of the given evidence based on the goal. The higher the score the more likely the statement can prove the goal has been achieved. And give the reason why a specific score is given. The score is an integer between 0 and 10."""
    goal: str = dspy.InputField(desc="The goal of the statement")
    evidence: str = dspy.InputField(desc="The evidence extracted from the statement")
    score: int = dspy.OutputField(desc="The score of the statement")
    reason: str = dspy.OutputField(desc="The reason for the score")

class JudgeAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.evidence_extractor = dspy.ChainOfThought(Edvidence)
        self.judge = dspy.ChainOfThought(Judgement)

    def forward(self, goal, statement) -> dspy.Prediction:
        evidence = self.evidence_extractor(goal=goal, statement=statement).evidence
        judegment = self.judge(goal=goal, evidence=evidence)
        return dspy.Prediction(score=judegment.score, reason=judegment.reason, evidence=evidence)

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
