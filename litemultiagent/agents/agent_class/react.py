from typing import List, Dict, Any
from .base import BaseAgent
import json


class ReActAgent(BaseAgent):
    def __init__(self, agent_name: str, agent_description: str, parameter_description: str,
                 tools: List[Dict[str, Any]], available_tools: Dict[str, callable], meta_data: Dict[str, Any]):
        super().__init__(agent_name, agent_description, parameter_description, tools, available_tools, meta_data)
        self.thought_history = []

    def send_prompt(self, goal: str) -> str:
        self.goal = goal
        self.messages = [
            {"role": "system",
             "content": f"{self.agent_description}\n\nRespond in the following format:\nThought: [Your reasoning about the current state and what to do next]\nAction: [The action to take, or 'Finish' if the task is complete]\nAction Input: [Input for the action, or the final answer if the action is 'Finish']"},
            {"role": "user",
             "content": f"Goal: {goal}\n\nUse the ReAct (Reasoning and Acting) approach to accomplish this goal. Think step-by-step, choose actions wisely, and observe the results."}
        ]
        return self._send_completion_request(plan=goal, depth=0)

    def _send_completion_request(self, plan: str, depth: int = 0) -> str:
        if depth >= 8:
            return "Maximum depth reached. Unable to complete the task."

        response = super()._send_completion_request(plan, depth)

        thought, action, action_input = self._parse_response(response)

        if not thought and not action and not action_input:
            # If parsing fails, treat the entire response as the final answer
            return f"Final Answer: {response}"

        self.thought_history.append(thought)

        if action.lower() == "finish":
            return action_input  # This is the final answer

        # Execute the action and get the observation
        observation = self._execute_action(action, action_input)

        # Add the thought, action, and observation to the message history
        self.messages.append({
            "role": "assistant",
            "content": f"Thought: {thought}\nAction: {action}\nAction Input: {action_input}\nObservation: {observation}"
        })

        # Continue the ReAct loop
        return self._send_completion_request(plan, depth + 1)

    def _parse_response(self, response: str) -> tuple:
        thought = action = action_input = ""
        lines = response.split('\n')
        current_section = ""

        for line in lines:
            line = line.strip()
            if line.startswith("Thought:"):
                current_section = "thought"
                thought = line.split("Thought:")[1].strip()
            elif line.startswith("Action:"):
                current_section = "action"
                action = line.split("Action:")[1].strip()
            elif line.startswith("Action Input:"):
                current_section = "action_input"
                action_input = line.split("Action Input:")[1].strip()
            elif current_section:
                # Append to the current section if it's a continuation
                if current_section == "thought":
                    thought += " " + line
                elif current_section == "action":
                    action += " " + line
                elif current_section == "action_input":
                    action_input += " " + line

        return thought, action, action_input

    def _execute_action(self, action: str, action_input: str) -> str:
        if action in self.available_tools:
            try:
                result = self.available_tools[action](action_input)
                return str(result)
            except Exception as e:
                return f"Error executing action {action}: {str(e)}"
        else:
            return f"Unknown action: {action}"

    def execute(self, task: str) -> str:
        return self.send_prompt(task)