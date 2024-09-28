import logging
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any, Optional
from pydantic import BaseModel, validator
import requests
import os
from bs4 import BeautifulSoup
from litemultiagent.tools.registry import ToolRegistry, Tool
import json
_ = load_dotenv()

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


import requests
from bs4 import BeautifulSoup


def scrape(url: str):
    # scrape website. Url is the url of the website to be scraped
    print("Scraping website...")
    try:
        # Send a GET request to the URL with a timeout of 10 seconds
        response = requests.get(url, timeout=10)
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


def register_web_retrieval_tools():
    ToolRegistry.register(Tool(
        "bing_search",
        bing_search,
        "Bing search for relevant information given a query.",
        {
            "query": {
                "type": "string",
                "description": "Bing search query.",
                "required": True
            }
        }
    ))

    ToolRegistry.register(Tool(
        "scrape",
        scrape,
        "Scraping website content based on url from Bing search.",
        {
            "url": {
                "type": "string",
                "description": "Website url to scrape.",
                "required": True
            }
        }
    ))