from agent import Agent
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any, Optional
from pydantic import BaseModel, validator
import sys
from logging.handlers import RotatingFileHandler
import requests
import os
import json
_ = load_dotenv()
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from supabase import create_client, Client
import logging
# Create a logger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log.txt", mode="w"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
from litellm import completion

def retrieve_db(client, db, input_column, output_column, input_value):
    if client == "SUPABASE":
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_ANON_KEY")

        if not url or not key:
            return "Error: SUPABASE_URL or SUPABASE_ANON_KEY environment variables are not set."

        try:
            supabase: Client = create_client(url, key)
            data = supabase.table(db).select(output_column).eq(input_column, input_value).execute()

            if data.data:
                return data.data[0][output_column]
            else:
                return f"No data found for {input_value} in {db}"

        except Exception as e:
            return f"Failed to retrieve data from Supabase: {str(e)}"
    else:
        return "not defined clients"

tools = [{
  "type": "function",
  "function": {
    "name": "retrieve_db",
    "description": "Retrieve data from a specified database (currently supports Supabase) based on input parameters.",
    "parameters": {
      "type": "object",
      "properties": {
        "client": {
          "type": "string",
          "description": "The database client to use. Currently supports 'SUPABASE'."
        },
        "db": {
          "type": "string",
          "description": "The name of the database table to query."
        },
        "input_column": {
          "type": "string",
          "description": "The column name to search in."
        },
        "output_column": {
          "type": "string",
          "description": "The column name to retrieve data from."
        },
        "input_value": {
          "type": "string",
          "description": "The value to search for in the input column."
        }
      },
      "required": [
        "client",
        "db",
        "input_column",
        "output_column",
        "input_value"
      ]
    }
  }
}]

from config import agent_to_model
agent_name = "db_retrieval_agent"

available_tools = {
            "retrieve_db": retrieve_db,
        }

class DB_Retrieval_Agent(Agent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        super().__init__("retrieval_agent", tools, available_tools, meta_task_id, task_id)


agent = DB_Retrieval_Agent(0, 0)
response = agent.send_prompt("use supabase database, users table, look up the email (column name: email) for name is danqing2")
print(response)
print(agent.messages)


def use_db_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = DB_Retrieval_Agent(meta_task_id, task_id)
    return agent.send_prompt(query)

# Example usage:
response = use_db_retrieval_agent("use supabase database, users table, look up the email (column name: email) for name is danqing2", 0, 0)
print(response)