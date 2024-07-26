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
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log.txt", mode="w"),
        logging.StreamHandler()
    ]
)

# Create a logger
logger = logging.getLogger(__name__)

from langchain_community.tools.tavily_search import TavilySearchResults
from utils import *

from web_search_agent import use_web_search_agent
from db_retrieval_agent import use_db_retrieval_agent
from file_retrieval_agent import use_file_retrieve_agent


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

from config import agent_to_model
agent_name = "retrieval_agent"

available_tools = {
            "use_web_search_agent": use_web_search_agent,
            "use_db_retrieval_agent": use_db_retrieval_agent,
            "use_file_retrieve_agent": use_file_retrieve_agent,
        }



def use_retrieval_search_agent(task_description):
    messages = [{"role" :"system", "content":"You are a smart research assistant. Use the search engine to look up information."}]
    # send_prompt(messages, query)
    send_prompt("retrieval_agent", messages, task_description, tools, available_tools)
    return messages[-1]["content"]


def main():
    response = use_retrieval_search_agent("Fetch the UK's GDP over the past 5 years")
    print(response)
    response = use_retrieval_search_agent(
        "use supabase database, users table, look up the email (column name: email) for name is danqing")
    print(response)
    response = use_file_retrieve_agent("search information in /Users/danqingzhang/Desktop/MultiAgent/code/files/attention.pdf and answer what is transformer?")
    print(response)

if __name__ == "__main__":
    main()
