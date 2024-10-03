from typing import List, Dict, Any, Tuple
from .base import BaseAgent
from litellm import completion
import json


class ReActAgent(BaseAgent):
    def __init__(self, agent_name: str, agent_description: str, parameter_description: str,
                 tools: List[Dict[str, Any]], available_tools: Dict[str, callable], meta_data: Dict[str, Any]):
        super().__init__(agent_name, agent_description, parameter_description, tools, available_tools, meta_data)
        self.thought_history = []

    def send_prompt(self, goal: str) -> str:
        self.goal = goal

        def get_tool_descriptions(tools):
            return "\n".join(f"- {tool['function']['name']}: {tool['function']['description']}"
                             for tool in tools if 'function' in tool)

        self.messages = [
            {"role": "system",
             "content": f"""
        {self.agent_description}

        You have access to the following tools:
        {', '.join(tool['function']['name'] for tool in self.tools if 'function' in tool)}

        When responding, you must choose an action from the available tools listed above, or 'Finish' if the task is complete.

        Respond in the following format:
        Thought: [Your reasoning about the current state and what to do next]
        Action: [The name of the tool to use from the list above, or 'Finish' if the task is complete]
        Action Input: [Input for the chosen tool, or the final answer if the action is 'Finish']

        Remember to always use one of the provided tools for your actions, unless you're finishing the task.

        Here are brief descriptions of each tool:
        {get_tool_descriptions(self.tools)}

        When using a tool, ensure that you provide the necessary parameters as described.
             """}
        ]
        return self._send_completion_request(prompt=goal, depth=0)

    def _send_completion_request(self, prompt: str, depth: int = 0) -> str:
        if depth >= 8:
            return "Maximum depth reached. Unable to complete the task."

        self.messages.append({"role": "user",
                              "content": f"Goal: {prompt}\n\nUse the ReAct (Reasoning and Acting) approach to accomplish this goal. Think step-by-step, choose actions wisely, and provide a response after each observation. Action: [The name of the tool to use from the list above, or 'Finish' if the task is complete]"})

        response = completion(
            model=self.model_name,
            messages=self.messages,
        )

        thought, action, action_input = self._parse_response(response.choices[0].message.content)
        if not thought and not action and not action_input:
            return f"Final Answer: {response.choices[0].message.content}"

        self.thought_history.append(thought)

        next_prompt = f"Thought: {thought}\nAction: {action}\nAction Input: {action_input}\n"
        self.messages.append({"role": "assistant",
                              "content": next_prompt})

        if action.lower() == "finish":
            # Generate a final response even when finishing
            final_response_prompt = f"The task is complete. Provide a final response summarizing the outcome:\nResponse: [Your final response]"
            self.messages.append({"role": "user", "content": final_response_prompt})

            final_response = completion(
                model=self.model_name,
                messages=self.messages,
            )

            final_content = final_response.choices[0].message.content
            if final_content.startswith("Response:"):
                final_content = final_content.split("Response:")[1].strip()

            return f"Final Answer: {final_content}"

        response = completion(
            model=self.model_name,
            messages=self.messages,
            tools=self.tools,
            tool_choice=self.tool_choice
        )

        self._log_response(response, depth)
        if self.save_to == "supabase":
            self._save_to_supabase(response, depth)
        elif self.save_to == "csv":
            self._save_to_csv(response, depth)

        message = response.choices[0].message
        tool_calls = message.tool_calls

        # Process tool calls and get observation
        observation = ""
        if tool_calls:
            tool_call_message = {
                "content": message.content,
                "role": message.role,
                "tool_calls": tool_calls
            }
            self.messages.append(tool_call_message)
            tool_responses = self._process_tool_calls(tool_calls)
            self.messages.extend(tool_responses)
            observation = "\n".join([resp["content"] for resp in tool_responses])

        # Get response to the observation
        response_prompt = f"Thought: {thought}\nAction: {action}\nAction Input: {action_input}\nObservation: {observation}\n\nBased on this observation, provide a response and determine your next step. Use the following format:\nResponse: [Your interpretation of the observation]\nThought: [Your reasoning about what to do next]\nAction: [The name of the tool to use from the list above, or 'Finish' if the task is complete]\nAction Input: [Input for the chosen tool, or the final answer if the action is 'Finish']"

        self.messages.append({"role": "user", "content": response_prompt})

        response = completion(
            model=self.model_name,
            messages=self.messages,
        )

        response_content, next_thought, next_action, next_action_input = self._parse_full_response(
            response.choices[0].message.content)

        # Prepare the next prompt
        next_prompt = f"Response: {response_content}\nThought: {next_thought}\nAction: {next_action}\nAction Input: {next_action_input}\n\nContinue with the next step. Respond in the same format."

        # Continue the ReAct loop
        return self._send_completion_request(next_prompt, depth + 1)

    def _parse_full_response(self, content: str) -> Tuple[str, str, str, str]:
        # Parse the response into response, thought, action, and action input
        lines = content.split('\n')
        response = thought = action = action_input = ""
        for line in lines:
            if line.startswith("Response:"):
                response = line.split("Response:")[1].strip()
            elif line.startswith("Thought:"):
                thought = line.split("Thought:")[1].strip()
            elif line.startswith("Action:"):
                action = line.split("Action:")[1].strip()
            elif line.startswith("Action Input:"):
                action_input = line.split("Action Input:")[1].strip()
        return response, thought, action, action_input

    def _parse_response(self, content: str) -> Tuple[str, str, str]:
        # Parse the response into thought, action, and action input
        lines = content.split('\n')
        thought = action = action_input = ""
        for line in lines:
            if line.startswith("Thought:"):
                thought = line.split("Thought:")[1].strip()
            elif line.startswith("Action:"):
                action = line.split("Action:")[1].strip()
            elif line.startswith("Action Input:"):
                action_input = line.split("Action Input:")[1].strip()
        return thought, action, action_input
