import logging
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any
from pydantic import BaseModel, validator
import requests
import os
import json
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def execute_shell_command(command):
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, check=True
        )
        output = result.stdout.strip() if result.stdout else result.stderr.strip()
        tokens = output.split()
        print(len(tokens))
        if len(tokens) > 500:
            final_result = " ".join(tokens[:100]) + "truncated...truncated" + " ".join(tokens[-100:])
        else:
            final_result = " ".join(tokens)
        return final_result
    except subprocess.CalledProcessError as e:
        return f"Error executing command '{command}': {e.stderr.strip()}"

def read_file(file_path: str, encoding: str = "utf-8") -> str:
    if not os.path.isfile(file_path):
        return f"Error: The file {file_path} does not exist."
    try:
        with open(file_path, encoding=encoding) as f:
            return f.read()
    except Exception as error:
        return f"Error: {error}"

def write_to_file(file_path: str, text: str, encoding: str = "utf-8") -> str:
    try:
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(file_path, "w", encoding=encoding) as f:
            f.write(text)
        return "File written successfully."
    except Exception as error:
        return f"Error: {error}"
from langchain_community.tools.tavily_search import TavilySearchResults

def tavily_search(query):
    tool = TavilySearchResults(max_results=4)
    results = tool.invoke({"query": query})
    return results
    # max_results = 1
    # search_depth = "basic"
    # api_key = os.getenv('TAVILY_API_KEY')
    # if api_key is None:
    #     raise ValueError(
    #         "No API key provided. Set the TAVILY_API_KEY environment variable or pass the key as an argument.")
    #
    # url = "https://api.tavily.com/search"
    # headers = {
    #     "content-type": "application/json"
    # }
    # payload = {
    #     "api_key": api_key,  # Add API key to the payload
    #     "query": query,
    #     "max_results": max_results,
    #     "search_depth": search_depth,
    #     "include_answer": True,  # To get the AI-generated answer
    #     "include_raw_content": True  # To get the raw content of the pages
    # }
    #
    # print(
    #     f"Sending payload: {json.dumps({k: v if k != 'api_key' else '[REDACTED]' for k, v in payload.items()}, indent=2)}")
    #
    # try:
    #     response = requests.post(url, json=payload, headers=headers)
    #     print(f"Response status code: {response.status_code}")
    #
    #     if response.status_code != 200:
    #         print(f"Error response content: {response.text}")
    #
    #     response.raise_for_status()
    #     return response.json()
    # except requests.exceptions.RequestException as e:
    #     print(f"An error occurred: {e}")
    #     if hasattr(e, 'response') and e.response is not None:
    #         print(f"Error response content: {e.response.text}")
    #     return f"Error response content: {e.response.text}"

def scan_folder(folder_path, depth=2):
    ignore_patterns = [".*", "__pycache__"]
    file_paths = []
    for subdir, dirs, files in os.walk(folder_path):
        dirs[:] = [
            d for d in dirs
            if not any(
                d.startswith(pattern) or d == pattern for pattern in ignore_patterns
            )
        ]
        if subdir.count(os.sep) - folder_path.count(os.sep) >= depth:
            del dirs[:]
            continue
        for file in files:
            file_paths.append(os.path.join(subdir, file))
    return file_paths

def run_python_script(script_name):
    try:
        result = subprocess.run(
            ["python", script_name], capture_output=True, text=True, check=True
        )
        logger.info(f"Run script output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Run script error: {e}")


client = OpenAI()




class Message(BaseModel):
    role: str
    content: str
    tool_calls: list[Any] | None = None




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


class ToolCallMessage(BaseModel):
    content: str | None = None
    role: str
    tool_calls: list[ToolCall]


class ToolResponseMessage(BaseModel):
    tool_call_id: str
    role: str
    name: str
    content: str

from typing import Optional
from pydantic import BaseModel, field_validator
class AssistantMessage(BaseModel):
    role: str
    content: str | None = None
    name: str | None = None
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """
    tool_calls: Optional[list[ToolCall]] = []  # if it's None, assign empty list
    """The tool calls generated by the model, such as function calls."""

    @field_validator("role", mode="before")
    def check_role(cls, value):
        if value not in ["assistant"]:
            raise ValueError('Role must be "assistant"')
        return value

available_tools = {
            "write_to_file": write_to_file,
            "read_file": read_file,
            "scan_folder": scan_folder,
            "run_python_script": run_python_script,
            "execute_shell_command": execute_shell_command,
            "tavily_search": tavily_search,
        }
def process_tool_calls(tool_calls):
    tool_call_responses: list[str] = []
    for _index, tool_call in enumerate(tool_calls):
        tool_call_id = tool_call.id
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        function_to_call = available_tools.get(function_name)

        function_response: str | None = None
        try:
            function_response = function_to_call(**function_args)
            tool_response_message = ToolResponseMessage(
                tool_call_id=tool_call_id,
                role="tool",
                name=function_name,
                content=str(function_response),
            )
            #print(_index, tool_response_message)
            tool_call_responses.append(tool_response_message)
        except Exception as e:
            function_response = f"Error while calling function <{function_name}>: {e}"

    return tool_call_responses


def send_completion_request(messages: list = None, tools: list = None, depth = 0) -> dict:
    if depth >= 8:
        return None

    if tools is None:
        response = client.chat.completions.create(
            model="gpt-4o", messages=messages
        )
        logger.info('depth: %s, response: %s', depth, response)
        # message = AssistantMessage(**response.choices[0].message.model_dump())
        message = AssistantMessage(**response.choices[0].message.model_dump())
        messages.append(message)
        return response

    response = client.chat.completions.create(
        model="gpt-4o", messages=messages, tools=tools, tool_choice="auto"
    )
    ##
    # import pdb; pdb.set_trace()


    tool_calls = response.choices[0].message.tool_calls
    if tool_calls is None:
        logger.info('depth: %s, response: %s', depth, response)
        message = AssistantMessage(**response.choices[0].message.model_dump())
        messages.append(message)
        return response

    logger.info('depth: %s, response: %s', depth, response)
    tool_calls = [
        ToolCall(id=call.id, function=call.function, type=call.type)
        for call in response.choices[0].message.tool_calls
    ]
    tool_call_message = ToolCallMessage(
        content=response.choices[0].message.content, role=response.choices[0].message.role, tool_calls=tool_calls
    )

    messages.append(tool_call_message)
    tool_responses = process_tool_calls(tool_calls)
    messages.extend(tool_responses)
    return send_completion_request(messages, tools, depth + 1)


def send_prompt(messages, content: str, tools):
    messages.append(Message(role="user", content=content))
    return send_completion_request(messages, tools, 0)


class Agent:
    def __init__(self, name, system_prompt, tools):
        self.name = name
        self.messages = [Message(role="system", content='You are: ' + name + system_prompt)]
        self.tools = tools


    def get_response(self, prompt):
        """
        Send a prompt and return a response.
        In a real implementation, this method would interact with an AI model or API.
        """
        return send_prompt(self.messages, prompt, self.tools)

    def append_message(self, message):
        """
        Append a message to the agent's message history.
        """
        self.messages.append(message)