import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import agent_to_model, model_cost
from supabase import create_client, Client
import os
from dotenv import load_dotenv
_ = load_dotenv()
from litellm import completion

logger = logging.getLogger(__name__)

# Initialize Supabase client only if environment variables are set
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
supabase: Optional[Client] = None
if url and key:
    try:
        supabase = create_client(url, key)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")


class Agent:
    def __init__(self, agent_name: str, tools: List[Dict[str, Any]], available_tools: Dict[str, callable],
                 meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        self.agent_name = agent_name
        self.tools = tools
        self.available_tools = available_tools
        self.model_name = agent_to_model[agent_name]["model_name"]
        self.tool_choice = agent_to_model[agent_name]["tool_choice"]
        self.messages = []
        self.meta_task_id = meta_task_id
        self.task_id = task_id


    def send_prompt(self, content: str) -> str:
        self.messages.append({"role": "user", "content": content})
        return self._send_completion_request()

    def _send_completion_request(self, depth: int = 0) -> str:
        if depth >= 8:
            return None


        if self.tools is None:
            response = completion(
                model=self.model_name,
                messages=self.messages
            )
            self._log_response(response, depth)
            self._save_to_supabase(response, depth)
            message = response.choices[0].message
            self.messages.append(message)
            return message.content

        response = completion(
            model=self.model_name,
            messages=self.messages,
            tools=self.tools,
            tool_choice=self.tool_choice
        )

        self._log_response(response, depth)
        self._save_to_supabase(response, depth)

        tool_calls = response.choices[0].message.tool_calls

        if tool_calls is None or len(tool_calls) == 0:
            message = response.choices[0].message
            self.messages.append(message)
            return message.content

        tool_call_message = {
            "content": response.choices[0].message.content,
            "role": response.choices[0].message.role,
            "tool_calls": tool_calls
        }

        self.messages.append(tool_call_message)
        tool_responses = self._process_tool_calls(tool_calls)
        self.messages.extend(tool_responses)

        return self._send_completion_request(depth + 1)

    def _process_tool_calls(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        tool_call_responses = []
        logger.info(f"Number of function calls: {len(tool_calls)}")

        with ThreadPoolExecutor(max_workers=None) as executor:
            future_to_tool_call = {executor.submit(self._process_single_tool_call, tool_call): tool_call for tool_call
                                   in tool_calls}

            for future in as_completed(future_to_tool_call):
                result = future.result()
                if result:
                    tool_call_responses.append(result)

        return tool_call_responses

    def _process_single_tool_call(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        tool_call_id = tool_call["id"]
        function_name = tool_call["function"]["name"]
        function_args = json.loads(tool_call["function"]["arguments"])

        function_to_call = self.available_tools.get(function_name)

        try:
            function_response = function_to_call(**function_args)
            logger.info(f'Function name: {function_name}, function args: {function_args}')
            tool_response_message = {
                "tool_call_id": tool_call_id,
                "role": "tool",
                "name": function_name,
                "content": str(function_response)
            }
            logger.info(f'Function name: {function_name}, function response: {str(function_response)}')
            return tool_response_message
        except Exception as e:
            logger.error(f"Error while calling function <{function_name}>: {e}")
            return None

    def _log_response(self, response, depth):
        logger.info(
            f'Agent: {self.agent_name}, prompt tokens: {response.usage.prompt_tokens}, completion tokens: {response.usage.completion_tokens}')
        logger.info(f'Agent: {self.agent_name}, depth: {depth}, response: {response}')

    def _save_to_supabase(self, response, depth):
        if supabase is None:
            logger.warning("Supabase client is not initialized. Skipping database save.")
            return

        usage_dict = self._extract_cost(response)
        data = {
            "meta_task_id": self.meta_task_id,
            "task_id": self.task_id,
            "agent": self.agent_name,
            "depth": depth,
            "role": "assistant",
            "response": json.dumps(response.choices[0].message.model_dump()),
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "input_cost": usage_dict["input_cost"],
            "output_cost": usage_dict["output_cost"],
            "total_cost": usage_dict["total_cost"],
            "model_name": self.model_name,
        }

        try:
            supabase.table("multiagent").insert(data).execute()
        except Exception as e:
            logger.error(f"Failed to save data to Supabase: {e}")

    def _extract_cost(self, response):
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

        # Pricing for gpt-4-0314
        input_price_per_1m = model_cost[self.model_name]["input_price_per_1m"]
        output_price_per_1m = model_cost[self.model_name]["output_price_per_1m"]

        input_cost = (prompt_tokens / 1000) * input_price_per_1m
        output_cost = (completion_tokens / 1000) * output_price_per_1m
        total_cost = input_cost + output_cost

        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost
        }

