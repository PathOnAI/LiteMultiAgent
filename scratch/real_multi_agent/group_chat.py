# different LLM
# different agent framework
# for loop to start the chat
# https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat.ipynb
# user_proxy, code, pm

import logging
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any
from pydantic import BaseModel, validator
import requests
import os
import json
import json
from typing import List, Dict
_ = load_dotenv()
# Initialize logging

from utils import *


class GroupChat:
    def __init__(self, agents: List[Agent]):
        self.agents = {agent.name: agent for agent in agents}
        self.shared_messages = []

    def conduct_conversation(self, initial_prompt: str, num_rounds: int):
        # Initial prompt to the first agent
        first_agent = list(self.agents.values())[0]
        response = first_agent.get_response(initial_prompt)
        self._add_to_shared_messages(first_agent.name, response)

        # Conversation rounds
        for _ in range(num_rounds):
            for agent_name, agent in self.agents.items():
                if agent != first_agent:
                    prompt = "Response based on current conversations, provide suggestions or different opinion to facilitate the discussion"
                    if agent_name == "Software Engineer":
                        prompt += ", if possible, write script"
                    response = agent.get_response(prompt)
                    self._add_to_shared_messages(agent_name, response)

    def _add_to_shared_messages(self, agent_name: str, response):
        message = AssistantMessage(**response.choices[0].message.model_dump())
        for agent in self.agents.values():
            if agent.name != agent_name:
                agent.append_message(message)
        self.shared_messages.append({'job': agent_name, 'message': message})

    def save_messages(self, filename: str = "group_chat_messages.json"):
        formatted_messages = []
        for index, message in enumerate(self.shared_messages):
            formatted_message = {
                "index": index,
                "job": message['job'],
                "role": message['message'].role,
                "content": message['message'].model_dump()
            }
            formatted_messages.append(formatted_message)

        with open(filename, 'w') as f:
            json.dump(formatted_messages, f, indent=2)
        print(f"Group chat messages saved to {filename}")

    def save_individual_messages(self):
        for agent_name, agent in self.agents.items():
            filename = f"{agent_name.lower()}_messages.json"
            self._save_agent_messages(agent, filename)

    def _save_agent_messages(self, agent: Agent, filename: str):
        formatted_messages = [
            {
                "index": index,
                "role": message.role,
                "type": str(type(message)),  # Convert type to string for JSON serialization
                "content": message.model_dump()
            }
            for index, message in enumerate(agent.messages)
        ]

        with open(filename, 'w') as f:
            json.dump(formatted_messages, f, indent=2)
        print(f"{agent.name}'s messages saved to {filename}")


# Find a latest paper about gpt-4 on arxiv and find its potential applications in software.

# Example usage:
if __name__ == "__main__":
    pm_tools = [
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
    ]
    swe_tools = [
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
    pm_agent = Agent(name="Product_manager", system_prompt="Creative in software product ideas.", tools=pm_tools)
    swe_agent = Agent(name="Software Engineer", system_prompt="Tend to write some code to facilitate discussion.", tools=swe_tools)

    # Find a latest paper about gpt-4 on arxiv and find its potential applications in software.
    group_chat = GroupChat([pm_agent, swe_agent])
    group_chat.conduct_conversation(
        initial_prompt="I want to know how retrieval augmented generation works, and show me some python code, and save the code. ",
        num_rounds=2
    )
    group_chat.save_messages()
    group_chat.save_individual_messages()



