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

# Configure logging
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

def read_file(file_path: str, encoding: str = "utf-8") -> str:
    if not os.path.isfile(file_path):
        return f"Error: The file {file_path} does not exist."
    try:
        with open(file_path, encoding=encoding) as f:
            return f.read()
    except Exception as error:
        return f"Error: {error}"

def write_to_file(file_path: str, text: str, encoding: str = "utf-8") -> str:
    try:
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(file_path, "w", encoding=encoding) as f:
            f.write(text)
        return "File written successfully."
    except Exception as error:
        return f"Error: {error}"


def generate_and_download_image(prompt, filename):
    model="dall-e-2"
    size="1024x1024"
    quality="standard"
    # Generate image
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        n=1,
    )

    # Get image URL
    image_url = response.data[0].url
    print("Image generation response:", response)
    print("Generated image URL:", image_url)

    # Download image
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(image_response.content)
        return f"Image downloaded successfully: {filename}"
    else:
        return f"Failed to download image. Status code: {image_response.status_code}"




tools = [
    {
        "type": "function",
        "function": {
            "name": "write_to_file",
            "description": "Write string content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Full file name with path where the content will be written."
                    },
                    "text": {
                        "type": "string",
                        "description": "Text content to be written into the file."
                    },
                    "encoding": {
                        "type": "string",
                        "default": "utf-8",
                        "description": "Encoding to use for writing the file. Defaults to 'utf-8'."
                    }
                },
                "required": [
                    "file_path",
                    "text"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file and return its contents as a string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The full file name with path to read."
                    },
                    "encoding": {
                        "type": "string",
                        "default": "utf-8",
                        "description": "The encoding used to decode the file. Defaults to 'utf-8'."
                    }
                },
                "required": [
                    "file_path"
                ]
            }
        }
    },
    {
      "type": "function",
      "function": {
        "name": "generate_and_download_image",
        "description": "Generate an image using DALL-E 2 based on a prompt and download it.",
        "parameters": {
          "type": "object",
          "properties": {
            "prompt": {
              "type": "string",
              "description": "The text prompt to generate the image from."
            },
            "filename": {
              "type": "string",
              "description": "The filename (including path) to save the downloaded image."
            }
          },
          "required": [
            "prompt",
            "filename"
          ]
        }
      }
    }
]

# client = OpenAI()
from config import agent_to_model
agent_name = "io_agent"
model_name = agent_to_model[agent_name]["model_name"]
# if 'gpt' in model_name:
#     client = OpenAI()
# else:
#     client = OpenAI(
#         base_url="https://openrouter.ai/api/v1",
#         api_key=os.getenv("OPENROUTER_API_KEY"),
#     )

client = OpenAI()
available_tools = {
            "write_to_file": write_to_file,
            "read_file": read_file,
            "generate_and_download_image": generate_and_download_image,
        }

def use_io_agent(description):
    messages = [Message(role="system",
                        content="You are an ai agent that read and write files")]
    # send_prompt(messages, query)
    send_prompt("io_agent", messages, description, tools, available_tools)
    return messages[-1].content


def main():
    response = use_io_agent("write aaa to file /Users/danqingzhang/Desktop/MultiAgent/hierarchical/code/2.txt")
    print(response)
    response = use_io_agent("generate a image of a ginger cat and save it as ginger_cat.png")
    print(response)

if __name__ == "__main__":
    main()