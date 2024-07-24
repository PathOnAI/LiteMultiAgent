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
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("log.txt", mode="w"),
#         logging.StreamHandler()
#     ]
# )

# Create a logger
logger = logging.getLogger(__name__)

from langchain_community.tools.tavily_search import TavilySearchResults
from utils import *

from web_search_agent import use_web_search_agent
from db_retrieval_agent import use_db_retrieval_agent


tools = [
    {
        "type": "function",
        "function": {
            "name": "use_web_search_agent",
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
    }
]

client = OpenAI()

available_tools = {
            "use_web_search_agent": use_web_search_agent,
            "use_db_retrieval_agent": use_db_retrieval_agent,
        }



def use_retrieval_search_agent(query):
    messages = [Message(role="system",
                        content="You are a smart research assistant. Use the search engine to look up information.")]
    # send_prompt(messages, query)
    send_prompt("retrieval_agent", client, messages, query, tools, available_tools)
    return messages[-1].content


def main():
    messages = use_retrieval_search_agent("Fetch the UK's GDP over the past 5 years")
    print(messages)
    messages = use_retrieval_search_agent(
        "use supabase database, users table, look up the email (column name: email) for name is danqing")
    print(messages)

if __name__ == "__main__":
    main()