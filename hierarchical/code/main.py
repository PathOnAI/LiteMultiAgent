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





from web_search_agent import use_search_agent
from io_agent import use_io_agent
from exec_agent import use_exec_agent

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



tools = [
    {
        "type": "function",
        "function": {
            "name": "use_search_agent",
            "description": "Perform a search using API and return the searched results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The task description describing what to read or write."
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
            "name": "use_io_agent",
            "description": "read or write some content from or to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "The task description describing what to read or write."
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
            "name": "use_exec_agent",
            "description": "Execute some script in a subprocess, either run a bash script, or run a python script ",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "The task description describing what to execute in the subprocess.",
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
]

client = OpenAI()

available_tools = {
            "scan_folder": scan_folder,
            "use_search_agent": use_search_agent,
            "use_io_agent": use_io_agent,
            "use_exec_agent": use_exec_agent,
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

# query = "Fetch the UK's GDP over the past 5 years, then write python script to draw a line graph of it and save the image to the current folder. And then run the python script."
# send_prompt(client, messages, query, tools, available_tools)
# save_messages_to_json(messages, filename="research_plot_messages.json")

# messages = [Message(role="system", content="You are a smart research assistant. Use the search engine to look up information. \
# You are allowed to make multiple calls (either together or in sequence). \
# Only look up information when you are sure of what you want. \
# If you need to look up some information before asking a follow up question, you are allowed to do that!")]
#
query = "browse google.com to check the brands of dining table and summarize the results in a table, save the table as a readme file"
send_prompt(client, messages, query, tools, available_tools)
save_messages_to_json(messages, filename="google_search_messages.json")
