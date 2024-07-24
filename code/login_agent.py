from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any
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
from utils import *


def connect_local_postgresql():
    # Retrieve connection details from environment variables
    host = os.getenv('POSTGRES_HOST')
    db = os.getenv('POSTGRES_DB')
    port = os.getenv('POSTGRES_PORT')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')

    # Construct the connection string
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    try:
        # Create the engine
        engine = create_engine(connection_string)

        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return "Successfully connected to PostgreSQL"

    except SQLAlchemyError as e:
        return f"Failed to connect to PostgreSQL: {str(e)}"


## example, supbase
## return credentials, SUPABASE_URL & SUPABASE_ANON_KEY
## example, HF
def connect_api(client):
    if client == "SUPABASE":
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_ANON_KEY")

        if not url or not key:
            return "Error: SUPABASE_URL or SUPABASE_ANON_KEY environment variables are not set."

        try:
            supabase: Client = create_client(url, key)
            table_name = "multiagent"
            data = supabase.table(table_name).select("*").execute()
            return "Successfully connected to Supabase"

        except Exception as e:
            return f"Failed to connect to Supabase: {str(e)}"
    else:
        return "client not defined"




tools = [
  {
    "type": "function",
    "function": {
      "name": "connect_local_postgresql",
      "description": "Connect to a local PostgreSQL database using environment variables for credentials.",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "connect_api",
      "description": "Connect to various API clients, currently supporting Supabase.",
      "parameters": {
        "type": "object",
        "properties": {
          "client": {
            "type": "string",
            "description": "The API client to connect to. Currently supports 'SUPABASE'."
          }
        },
        "required": [
          "client"
        ]
      }
    }
  }
]

client = OpenAI()
available_tools = {
            "connect_local_postgresql": connect_local_postgresql,
            "connect_api": connect_api
        }

def use_login_agent(query):
    messages = [Message(role="system",
                        content="You are a smart assistant, you check whether login is successful")]
    send_prompt("login_agent", client, messages, query, tools, available_tools)
    return messages[-1].content


def main():
    messages = use_login_agent(
        "check whether connected to supabase")
    print(messages)
    messages = use_login_agent(
        "write query to query supabase table, multiagent")
    print(messages)
    messages = use_login_agent(
        "check whether connected to local postgresql db")
    print(messages)

if __name__ == "__main__":
    main()