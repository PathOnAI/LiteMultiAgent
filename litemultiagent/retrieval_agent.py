import logging
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any, Optional
from pydantic import BaseModel, validator
import requests
import os
from multion.client import MultiOn
import json

_ = load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log.txt", mode="w"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

from agent import Agent
from db_retrieval_agent import DB_Retrieval_Agent


# Modify the use_db_retrieval_agent function to accept meta_task_id and task_id
def use_db_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = DB_Retrieval_Agent(meta_task_id, task_id)
    return agent.send_prompt(query)


tools = [
    {
        "type": "function",
        "function": {
            "name": "use_db_retrieval_agent",
            "description": "Use a database retrieval agent to fetch information based on a given query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to be processed by the database retrieval agent."
                    }
                },
                "required": ["query"]
            }
        }
    },
]

agent_name = "retrieval_agent"


class Retrieval_Agent(Agent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        # Create a wrapper for use_db_retrieval_agent that includes meta_task_id and task_id
        def wrapped_use_db_retrieval_agent(query: str) -> str:
            return use_db_retrieval_agent(query, meta_task_id=meta_task_id, task_id=task_id)

        available_tools = {
            "use_db_retrieval_agent": wrapped_use_db_retrieval_agent,
        }

        super().__init__("retrieval_agent", tools, available_tools, meta_task_id, task_id)


# Example usage
agent = Retrieval_Agent(meta_task_id="example_meta_task", task_id=124)
response = agent.send_prompt(
    "use supabase database, users table, look up the email (column name: email) for name is danqing2")
print(response)
print(agent.messages)

for index, message in enumerate(agent.messages):
    print(f"Message {index}: {message}")


def use_retrieval_search_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = Retrieval_Agent(meta_task_id, task_id)
    return agent.send_prompt(query)


def main():
    response = use_retrieval_search_agent(
        "use supabase database, users table, look up the email (column name: email) for name is danqing2", "test", 0)
    print(response)


if __name__ == "__main__":
    main()