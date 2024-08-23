from litemultiagent.agents.base import Agent

from typing import Optional

import requests
import os
from bs4 import BeautifulSoup

from litemultiagent.utils.tools import Tools

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



available_tools = {           
    "bing_search": bing_search,
    "scrape" : scrape
}


class Web_Retrieval_Agent(Agent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        super().__init__("web_retrieval_agent", Tools._web, available_tools, meta_task_id, task_id)
