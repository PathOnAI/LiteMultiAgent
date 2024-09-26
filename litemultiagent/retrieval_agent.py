import logging
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any, Optional
from pydantic import BaseModel, validator
import requests
import os
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

from litemultiagent.agents.BaseAgent import Agent
from db_retrieval_agent import use_db_retrieval_agent
from file_retrieval_agent import use_file_retrieval_agent
from web_retrieval_agent import use_web_retrieval_agent



tools = [
    {
        "type": "function",
        "function": {
            "name": "use_web_retrieval_agent",
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
          "required": [
            "query"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "use_file_retrieve_agent",
        "description": "Retrieve information from local documents to answer questions or perform tasks.",
        "parameters": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "The task description specifying the local file and the question to be answered. specify this in natural language"
            }
          },
          "required": [
            "query"
          ]
        }
      }
    }
]

agent_name = "retrieval_agent"


class Retrieval_Agent(Agent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        # Create a wrapper for use_db_retrieval_agent that includes meta_task_id and task_id
        def wrapped_use_db_retrieval_agent(query: str) -> str:
            return use_db_retrieval_agent(query, meta_task_id=meta_task_id, task_id=task_id)

        def wrapped_use_web_retrieval_agent(query: str) -> str:
            return use_web_retrieval_agent(query, meta_task_id=meta_task_id, task_id=task_id)

        def wrapped_use_file_retrieve_agent(query: str) -> str:
            return use_file_retrieve_agent(query, meta_task_id=meta_task_id, task_id=task_id)

        available_tools = {
            "use_db_retrieval_agent": wrapped_use_db_retrieval_agent,
            "use_web_retrieval_agent": wrapped_use_web_retrieval_agent,
            "use_file_retrieve_agent": wrapped_use_file_retrieve_agent,
        }

        super().__init__("use_retrieval_agent", tools, available_tools, meta_task_id, task_id)


def use_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = Retrieval_Agent(meta_task_id, task_id)
    agent.messages = [{"role" :"system", "content": "You are a smart research assistant. Use the search engine to look up information."}]
    return agent.send_prompt(query)


def main():
    response = use_retrieval_agent(
        "use supabase database, users table, look up the email (column name: email) for name is danqing2", "test", 0)
    print(response)
    response = use_web_retrieval_agent("Fetch the UK's GDP over the past 5 years", 0, 0)
    print(response)


if __name__ == "__main__":
    main()