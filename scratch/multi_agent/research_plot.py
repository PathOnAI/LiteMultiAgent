import logging
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any
from pydantic import BaseModel, validator
import requests
import os
import json
_ = load_dotenv()
# Initialize logging
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

tools = [
    {
        "type": "function",
        "function": {
            "name": "write_to_file",
            "description": "Write string content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Full file name with path where the content will be written."
                    },
                    "text": {
                        "type": "string",
                        "description": "Text content to be written into the file."
                    },
                    "encoding": {
                        "type": "string",
                        "default": "utf-8",
                        "description": "Encoding to use for writing the file. Defaults to 'utf-8'."
                    }
                },
                "required": [
                    "file_path",
                    "text"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file and return its contents as a string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The full file name with path to read."
                    },
                    "encoding": {
                        "type": "string",
                        "default": "utf-8",
                        "description": "The encoding used to decode the file. Defaults to 'utf-8'."
                    }
                },
                "required": [
                    "file_path"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tavily_search",
            "description": "Perform a search using the TavilySearch API and return the results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to be sent to the TavilySearch API."
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scan_folder",
            "description": "Scan a directory recursively for files with path with depth 2. You can also use this function to understand the folder structure in a given folder path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_path": {
                        "type": "string",
                        "description": "The folder path to scan."
                    }
                },
                "required": [
                    "folder_path"
                ]
            },
            "return_type": "list: A list of file paths str with the given extension, or all files if no extension is specified."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_python_script",
            "description": "Execute a Python script in a subprocess.",
            "parameters": {
                "type": "object",
                "properties": {
                    "script_name": {
                        "type": "string",
                        "description": "The name with path of the script to be executed."
                    }
                },
                "required": [
                    "script_name"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_shell_command",
            "description": "Execute a shell command in a subprocess.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to be executed."
                    }
                },
                "required": [
                    "command"
                ]
            }
        }
    }
]

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


def send_prompt(messages, content: str):
    messages.append(Message(role="user", content=content))
    return send_completion_request(messages, tools, 0)


# inputs = [
#     "Hi",
#     "Can you check format.sh and run_coding_agent.sh of folder /Users/danqingzhang/Desktop/mini-agent?",
#     "What is the weather in sf and nyc?"
# ]
#
# messages = [Message(role="system", content="You are a smart research assistant. Use the search engine to look up information. \
# You are allowed to make multiple calls (either together or in sequence). \
# Only look up information when you are sure of what you want. \
# If you need to look up some information before asking a follow up question, you are allowed to do that!")]
# for input in inputs:
#     send_prompt(messages, input)
#
# for index, message in enumerate(messages):
#     print(index, message, type(message))


messages = [Message(role="system", content="You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!")]

send_prompt(messages, "Fetch the UK's GDP over the past 5 years, then write python script to draw a line graph of it and save the image to the current folder. And then run the python script.")

for index, message in enumerate(messages):
    print(index, message, type(message))