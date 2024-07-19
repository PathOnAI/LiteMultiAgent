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

def tavily_search(query):
    tool = TavilySearchResults(max_results=4)
    results = tool.invoke({"query": query})
    return results


def multion_search(query, url):
    multion = MultiOn(api_key=os.getenv('MULTION_API_KEY'))
    browse = multion.browse(
        cmd=query,
        url=url
    )
    print("Browse response:", browse)
    print(browse.message)
    return browse.message



tools = [
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
            "name": "multion_search",
            "description": "For complicated search that require browsing/ scrolling down behavior, use multion api and return the results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to be sent to the multion API."
                    },
                    "url":{
                        "type": "string",
                        "description": "The website where multion api starts the browsing activity."
                    }
                },
                "required": [
                    "query",
                    "url"
                ]
            }
        }
    },
]

client = OpenAI()
available_tools = {
            "tavily_search": tavily_search,
            "multion_search": multion_search
        }

def use_search_agent(query):
    messages = [Message(role="system",
                        content="You are a smart research assistant. Use the search engine to look up information.")]
    # send_prompt(messages, query)
    send_prompt(client, messages, query, tools, available_tools)
    return messages[-1].content




def main():
    messages = use_search_agent("Fetch the UK's GDP over the past 5 years")
    print(messages)

    # messages = use_search_agent(
    #     "browse amazon.com to check the brands of dining table and summarize the results in a table")
    # print(messages)

    messages = use_search_agent(
        "browse google.com to check the brands of dining table and summarize the results in a table")
    print(messages)

if __name__ == "__main__":
    main()
