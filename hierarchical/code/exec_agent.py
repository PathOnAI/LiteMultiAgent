import logging
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any
from pydantic import BaseModel, validator
import requests
import os
from multion.client import MultiOn
import json
_ = load_dotenv()
# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from langchain_community.tools.tavily_search import TavilySearchResults
from utils import *
import subprocess


def execute_shell_command(command, wait=True):
    try:
        if wait:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip() if result.stdout else result.stderr.strip()
        else:
            subprocess.Popen(command, shell=True)
            return "Command executed in non-blocking mode."
    except subprocess.CalledProcessError as e:
        return f"Error executing command '{command}': {e.stderr.strip()}"

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
                    },
                    "wait": {
                        "type": "boolean",
                        "description": "Wait for the command to complete. Set to true for blocking execution and false for non-blocking."
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
            "run_python_script": run_python_script,
            "execute_shell_command": execute_shell_command,
        }

def use_exec_agent(description):
    messages = [Message(role="system",
                        content="You will exec some scripts. Either by shell or run python script")]
    send_prompt(client, messages, description, tools, available_tools)
    return messages[-1].content


def main():
    response = use_exec_agent("run /Users/danqingzhang/Desktop/MultiAgent/hierarchical/code/draw_gdp_line_graph.py file")
    print(response)

    response = use_exec_agent(
        "read file 3 lines of file /Users/danqingzhang/Desktop/MultiAgent/hierarchical/code/1.txt")
    print(response)

if __name__ == "__main__":
    main()