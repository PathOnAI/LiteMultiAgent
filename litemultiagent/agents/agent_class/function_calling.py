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


class FunctionCallingAgent(BaseAgent):
    def _send_completion_request(self, plan: str, depth: int = 0) -> str:
        if depth >= 8:
            return None

        if self.tools is None:
            response = completion(
                model=self.model_name,
                messages=self.messages
            )
            self._log_response(response, depth)
            self._save_response(response, depth)
            message = response.choices[0].message
            self.messages.append(message.model_dump())
            return message.content

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