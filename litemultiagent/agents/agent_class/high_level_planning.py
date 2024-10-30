from .base import BaseAgent
from typing import List, Dict
from dotenv import load_dotenv
from litellm import completion
from datetime import datetime
import logging
from openai import OpenAI

_ = load_dotenv()

openai_client = OpenAI()
logger = logging.getLogger(__name__)


class HighLevelPlanningAgent(BaseAgent):

    def _send_completion_request(self, plan: str, depth: int = 0) -> str:
        if depth == 0:
            # make plan based goal
            plan = self.make_plan()
            logger.info('updated plan: %s', plan)

        if depth >= 8:
            return None

        if not self.tools:
            response = completion(
                model=self.model_name,
                messages=self.messages
            )
            self._log_response(response, depth)
            self._save_response(response, depth)

            message = response.choices[0].message
            self.messages.append(message.model_dump())
            return message.content

        logger.info('current plan: %s', plan)

        if depth > 0:
            from pydantic import BaseModel
            class Plan(BaseModel):
                goal_finished: bool

            prompt = f"""
                Goal: {self.goal}
                Current plan: {plan}

                Based on the progress made so far, you have access to the following tools: 
                {', '.join(tool['function']['name'] for tool in self.tools if 'function' in tool)}. 
                Please leverage these tools as needed and provide:

                1. An updated complete plan
                2. A list of tasks that have already been completed
                3. An explanation of changes and their rationale

                Format your response as follows:

                Updated Plan:
                - [Step 1]
                - [Step 2]
                - ...

                Completed Tasks:
                - [Task 1]
                - [Task 2]
                - ...

                Explanation of Changes:
                - [Explanation 1]
                - [Explanation 2]
                - ...
            """
            self.messages.append({"role": "user", "content": prompt})
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=self.messages
            )

            plan = response.choices[0].message.content
            new_response = openai_client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[{"role": "system", "content": "Is the overall goal finished?"},
                          {"role": "user", "content": plan}],
                response_format=Plan
            )
            message = new_response.choices[0].message.parsed
            goal_finished = message.goal_finished
            if goal_finished:
                logger.info("goal finished")
                return response.choices[0].message.content
            else:
                self.messages.append({"role": "user", "content": plan})

        logger.info('updated plan: %s', plan)
        response = completion(
            model=self.model_name,
            messages=self.messages,
            tools=self.tools,
            tool_choice=self.tool_choice
        )

        # whether it has tool call or not
        self._log_response(response, depth)
        self._save_response(response, depth)

        tool_calls = response.choices[0].message.tool_calls

        if tool_calls is None or len(tool_calls) == 0:
            message = response.choices[0].message
            self.messages.append(message.model_dump())
            return message.content

        tool_call_message = {
            "content": response.choices[0].message.content,
            "role": response.choices[0].message.role,
            "tool_calls": tool_calls
        }

        self.messages.append(tool_call_message)
        tool_responses = self._process_tool_calls(tool_calls)
        self.messages.extend(tool_responses)

        return self._send_completion_request(plan, depth + 1)