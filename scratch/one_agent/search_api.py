from dotenv import load_dotenv
_ = load_dotenv()

import requests
import os
import json


def tavily_search(query):
    max_results = 1
    search_depth = "basic"
    api_key = os.getenv('TAVILY_API_KEY')
    if api_key is None:
        raise ValueError(
            "No API key provided. Set the TAVILY_API_KEY environment variable or pass the key as an argument.")

    url = "https://api.tavily.com/search"
    headers = {
        "content-type": "application/json"
    }
    payload = {
        "api_key": api_key,  # Add API key to the payload
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth
    }

    print(
        f"Sending payload: {json.dumps({k: v if k != 'api_key' else '[REDACTED]' for k, v in payload.items()}, indent=2)}")

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Response status code: {response.status_code}")

        if response.status_code != 200:
            print(f"Error response content: {response.text}")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Error response content: {e.response.text}")
        return None


# Example usage:
if __name__ == "__main__":
    search_query = "weather in New York City"
    results = tavily_search(search_query)

    if results:
        print(f"Search results for: '{search_query}'")
        for i, result in enumerate(results.get('results', []), 1):
            print(i, result)
            # print(f"\n{i}. {result['title']}")
            # print(f"   URL: {result['url']}")
            # print(f"   Snippet: {result['snippet']}")
    else:
        print("No results found or an error occurred.")