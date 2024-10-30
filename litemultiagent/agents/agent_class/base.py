import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from litellm import completion
from dotenv import load_dotenv
from litellm import completion
from datetime import datetime
from supabase import create_client, Client
import os
import csv

_ = load_dotenv()

from openai import OpenAI

_ = load_dotenv()

openai_client = OpenAI()

logger = logging.getLogger(__name__)

MODEL_COST = {
    "gpt-4o-mini": {
        "input_price_per_1m": 0.15,
        "output_price_per_1m": 0.6,
    },
    "gemini/gemini-pro": {
        "input_price_per_1m": 0,
        "output_price_per_1m": 0,
    },
    "claude-3-5-sonnet-20240620": {
        "input_price_per_1m": 3,
        "output_price_per_1m": 15,
    },
    "groq/llama3-8b-8192": {
        "input_price_per_1m": 0.05,
        "output_price_per_1m": 0.08,
    },
}

# Initialize Supabase client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
supabase: Optional[Client] = None
if url and key:
    try:
        supabase = create_client(url, key)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")

class BaseAgent:
    def __init__(self, agent_name: str, agent_description, parameter_description, tools: List[Dict[str, Any]],
                 available_tools: Dict[str, callable],
                 meta_data):
        self.agent_name = agent_name
        self.tools = tools
        self.available_tools = available_tools
        self.messages = []
        self.model_name = meta_data.get("model_name", None)
        self.tool_choice = meta_data.get("tool_choice", None)
        self.agent_description = agent_description
        self.parameter_description = parameter_description
        self.goal = None

    def make_plan(self):
        # Initial message to guide the assistant
        messages = [
            {"role": "system",
             "content": "You are a helpful assistant tasked with making a plan for a given goal or user request. Please provide a detailed plan in the next few sentences."},
            {"role": "assistant", "content": "The goal is: {}".format(self.goal)},
            {
                "role": "assistant",
                "content": "You have access to the following tools: {}. Please leverage these tools as needed while formulating the plan.".format(
                    ', '.join(tool['function']['name'] for tool in self.tools if 'function' in tool)
                )
            }
        ]

        # Generate the chat completion
        chat_completion = openai_client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )

        # Extract and return the plan
        plan = chat_completion.choices[0].message.content
        return plan

    def send_prompt(self, goal: str) -> str:
        self.messages.append({"role": "user", "content": goal})
        self.goal = goal
        return self._send_completion_request(plan=goal, depth=0)

    def set_shared_config(self, shared_config):
        self.shared_config = shared_config
        self.model_name = self.model_name or self.shared_config["model_name"]
        self.tool_choice = self.tool_choice or self.shared_config["tool_choice"]

    def _send_completion_request(self, plan, depth: int = 0) -> str:
        pass

    def _process_tool_calls(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        tool_call_responses = []
        logger.info(f"Number of function calls: {len(tool_calls)}")

        for tool_call in tool_calls:
            result = self._process_single_tool_call(tool_call)
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

    def _save_response(self, response, depth):
        if self.shared_config["save_to"] == "supabase":
            self._save_to_supabase(response, depth)
        if self.shared_config["save_to"] == "csv":
            self._save_to_csv(response, depth)

    def _save_to_csv(self, response, depth):
        usage_dict = self._extract_cost(response)
        data = {
            "system_name": self.shared_config["system_name"],
            "system_runtime_id": self.shared_config["system_runtime_id"],
            "task_id": self.shared_config["task_id"],
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
            "timestamp": datetime.now().isoformat()
        }
        filename = os.path.join(self.shared_config["log_dir"], f"multiagent_data_{datetime.now().strftime('%Y%m%d')}.csv")
        file_exists = os.path.isfile(filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # If file doesn't exist, create it with header
        if not file_exists:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = list(data.keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            logger.info(f"Created new CSV file with header: {filename}")

        # Append data to the file
        with open(filename, 'a', newline='') as csvfile:
            fieldnames = list(data.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data)

        logger.info(f"Data saved to CSV: {filename}")

    def _save_to_supabase(self, response, depth):
        usage_dict = self._extract_cost(response)
        data = {
            "system_name": self.shared_config["system_name"],
            "system_runtime_id": self.shared_config["system_runtime_id"],
            "task_id": self.shared_config["task_id"],
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
        if supabase is None:
            logger.warning("Supabase client is not initialized. Skipping database save.")
            return
        try:
            supabase.table("multiagent").insert(data).execute()
        except Exception as e:
            logger.error(f"Failed to save data to Supabase: {e}")

    def _extract_cost(self, response):
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

        # Pricing for gpt-4-0314
        input_price_per_1m = MODEL_COST[self.model_name]["input_price_per_1m"]
        output_price_per_1m = MODEL_COST[self.model_name]["output_price_per_1m"]

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
