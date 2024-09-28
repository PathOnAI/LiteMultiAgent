import subprocess
import logging
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any, Optional
from pydantic import BaseModel, validator
import requests
import os
import json
from litemultiagent.tools.registry import ToolRegistry, Tool


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


def register_exec_tools():
    ToolRegistry.register(Tool(
        "run_python_script",
        run_python_script,
        "Execute a Python script in a subprocess.",
        {
            "script_name": {
                "type": "string",
                "description": "The name with path of the script to be executed.",
                "required": True
            }
        }
    ))

    ToolRegistry.register(Tool(
        "execute_shell_command",
        execute_shell_command,
        "Execute a shell command in a subprocess.",
        {
            "command": {
                "type": "string",
                "description": "The shell command to be executed.",
                "required": True
            },
            "wait": {
                "type": "boolean",
                "description": "Wait for the command to complete. Set to true for blocking execution and false for non-blocking.",
                "required": True
            }
        }
    ))
