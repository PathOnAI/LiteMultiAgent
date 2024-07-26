from typing import Any
from pydantic import BaseModel, validator
import logging
import logging
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any
from pydantic import BaseModel, validator
import requests
import os
import json
# Initialize logging
import logging
from litellm import completion
# Get a logger for this module
logger = logging.getLogger(__name__)


import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
from supabase import create_client, Client
from config import agent_to_model



url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(url, key)


class Function(BaseModel):
    arguments: str
    name: str


class ToolCall(BaseModel):
    id: str
    function: Function | dict
    type: str

    @validator("function", pre=True)
    @classmethod
    def ensure_function_dict(cls, v):
        return v if isinstance(v, dict) else v.dict()




def process_tool_calls(tool_calls, available_tools):
    tool_call_responses = []
    logger.info("Number of function calls: %i", len(tool_calls))
    for tool_call in tool_calls:
        tool_call_id = tool_call.id
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        function_to_call = available_tools.get(function_name)

        try:
            function_response = function_to_call(**function_args)
            logger.info('function name: %s, function args: %s', function_name, function_args)
            tool_response_message = {"tool_call_id": tool_call_id,
                                     "role": "tool",
                                     "name": function_name,
                                     "content": str(function_response)}
            logger.info('function name: %s, function response %s', function_name, str(function_response))
            tool_call_responses.append(tool_response_message)
        except Exception as e:
            logger.error(f"Error while calling function <{function_name}>: {e}")

    return tool_call_responses

def extract_cost(response):
    # Extract token usage
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    # Pricing for gpt-4o-mini
    input_price_per_1m = 0.150  # $0.150 per 1M tokens for input
    output_price_per_1m = 0.600  # $0.600 per 1M tokens for output

    # Calculate cost
    input_cost = (prompt_tokens / 1_000_000) * input_price_per_1m
    output_cost = (completion_tokens / 1_000_000) * output_price_per_1m
    total_cost = input_cost + output_cost

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost
    }

def send_completion_request(agent_name, messages: list, tools: list = None, available_tools: dict = None, depth: int = 0) -> dict:
    if depth >= 8:
        return None
    model_name = agent_to_model[agent_name]["model_name"]
    tool_choice = agent_to_model[agent_name]["tool_choice"]
    if tools is None:
        response = completion(
            model=model_name, messages=messages
        )
        logger.info('agent: %s, prompt tokens: %s, completion tokens: %s', agent_name,
                    str(response.usage.prompt_tokens), str(response.usage.completion_tokens))
        logger.info('agent: %s, depth: %s, response: %s', agent_name, depth, response)
        data = {
            "agent": agent_name,
            "depth": depth,
            "role": "assistant",
            "response": json.dumps(response.choices[0].message.model_dump()),
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "input_cost": usage_dict["input_cost"],
            "output_cost": usage_dict["output_cost"],
            "total_cost": usage_dict["total_cost"],
        }
        supabase.table("multiagent").insert(data).execute()
        message = AssistantMessage(**response.choices[0].message.model_dump())
        messages.append(message)
        return response

    response = completion(
        model=model_name, messages=messages, tools=tools, tool_choice=tool_choice
    )


    logger.info('agent: %s, prompt tokens: %s, completion tokens: %s', agent_name, str(response.usage.prompt_tokens), str(response.usage.completion_tokens))
    logger.info('agent: %s, depth: %s, response: %s', agent_name, depth, response)
    tool_calls = response.choices[0].message.tool_calls
    usage_dict = extract_cost(response)

    data = {
        "agent": agent_name,
        "depth": depth,
        "role": "assistant",
        "response": json.dumps(response.choices[0].message.model_dump()),
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "input_cost": usage_dict["input_cost"],
        "output_cost": usage_dict["output_cost"],
        "total_cost": usage_dict["total_cost"],
    }
    supabase.table("multiagent").insert(data).execute()

    if tool_calls is None or len(tool_calls) == 0:
        message = response.choices[0].message.model_dump()
        messages.append(message)
        return response

    tool_calls = [
        ToolCall(id=call.id, function=call.function, type=call.type)
        for call in response.choices[0].message.tool_calls
    ]

    tool_call_message = {"content": response.choices[0].message.content, "role": response.choices[0].message.role, "tool_calls": tool_calls}

    messages.append(tool_call_message)
    tool_responses = process_tool_calls(tool_calls, available_tools)
    messages.extend(tool_responses)

    return send_completion_request(agent_name, messages, tools, available_tools, depth + 1)

def send_prompt(agent_name, messages, content: str, tools, available_tools):
    messages.append({"role":"user", "content":content})
    return send_completion_request(agent_name,  messages, tools, available_tools, 0)