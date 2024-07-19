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
from utils import *

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

from web_search import use_search_agent

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
        result = subprocess.run(["python", script_name], capture_output=True, text=True, check=True)
        res = f"stdout:{result.stdout}"
        if result.stderr:
            res += f"stderr:{result.stderr}"
        return res
    except subprocess.CalledProcessError as e:
        return f"Error:{e}"

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
            "name": "use_search_agent",
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

available_tools = {
            "write_to_file": write_to_file,
            "read_file": read_file,
            "scan_folder": scan_folder,
            "run_python_script": run_python_script,
            "execute_shell_command": execute_shell_command,
            "use_search_agent": use_search_agent,
        }

def save_messages_to_json(messages, filename="research_plot_messages.json"):
    # Create a list to store the formatted messages
    formatted_messages = []

    for index, message in enumerate(messages):
        # Print the message info
        print(index, message, type(message))

        # Format the message for JSON
        formatted_message = {
            "index": index,
            "message": str(message),  # Convert message to string in case it's not serializable
            "type": str(type(message))  # Convert type to string for JSON serialization
        }
        formatted_messages.append(formatted_message)

    # Save the formatted messages to a JSON file
    with open(filename, 'w') as f:
        json.dump(formatted_messages, f, indent=2)

    print(f"Messages saved to {filename}")


messages = [Message(role="system", content="You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!")]

query = "Fetch the UK's GDP over the past 5 years, then write python script to draw a line graph of it and save the image to the current folder. And then run the python script."
send_prompt(client, messages, query, tools, available_tools)
save_messages_to_json(messages, filename="research_plot_messages.json")

messages = [Message(role="system", content="You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!")]

query = "browse google.com to check the brands of dining table and summarize the results in a table, save the table as a readme file"
send_prompt(client, messages, query, tools, available_tools)
save_messages_to_json(messages, filename="google_search_messages.json")
