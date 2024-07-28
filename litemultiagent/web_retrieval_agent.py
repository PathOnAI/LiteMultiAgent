from agent import Agent
import logging
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any, Optional
from pydantic import BaseModel, validator
import requests
import os
from bs4 import BeautifulSoup
import json
_ = load_dotenv()
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


def bing_search(query:str):
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {
        "Ocp-Apim-Subscription-Key": os.getenv('BING_API_KEY')
    }
    params = {
        "q": query,
        "textDecorations": True, 
        "textFormat": "HTML"
    }
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
    except Exception as ex:
        raise ex
    # limit web page 
    pages = search_results["webPages"]["value"]
    n_web = min(5, len(pages))
    search_results["webPages"]["value"] = pages[:n_web]
    urls = [x['url'] for x in search_results["webPages"]["value"]]

    formatted_string = f"the related urls of the search are {', '.join(urls)}"

    print(formatted_string)
    return formatted_string

def scrape(url: str):
    # scrape website. Url is the url of the website to be scraped
    print("Scraping website...")
    try:
        # Send a GET request to the URL
        response = requests.get(url)        
        # Check if the request was successful
        response.raise_for_status()        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')        
        # Extract the text from the parsed HTML
        text = soup.get_text(separator=' ', strip=True)                
        return text
                
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return ""


tools = [    
    {
        "type": "function",
        "function": {
            "name": "bing_search",
            "description": "Bing search for relevant information given a query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Bing search query."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scrape",
            "description": "Scraping website content based on url from Bing search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Website url to scrape."
                    }
                },
                "required": ["url"]
            }
        }
    },
]

from config import agent_to_model
agent_name = "web_search_agent"

available_tools = {           
            "bing_search": bing_search,
            "scrape" : scrape
        }


class Web_Retrieval_Agent(Agent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        super().__init__("web_retrieval_agent", tools, available_tools, meta_task_id, task_id)

def use_web_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = Web_Retrieval_Agent(meta_task_id, task_id)
    agent.messages = [{"role":"system", "content" :"You are a smart research assistant. Use the search engine to look up information."}]
    return agent.send_prompt(query)


def main():
    response = use_web_retrieval_agent("Fetch the UK's GDP over the past 5 years", 0, 0)
    print(response)


if __name__ == "__main__":
    main()

