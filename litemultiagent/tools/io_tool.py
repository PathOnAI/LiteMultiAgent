#from litemultiagent.agents.BaseAgent import BaseAgent
#import logging
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any, Optional
from pydantic import BaseModel, validator
import requests
import os
import json
_ = load_dotenv()
from litemultiagent.tools.registry import ToolRegistry, Tool

client = OpenAI()

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


# Register tools with specific parameter descriptions
def register_io_tools():
    ToolRegistry.register(Tool(
        "read_file",
        read_file,
        "Read a file and return its contents as a string.",
        {
            "file_path": {
                "type": "string",
                "description": "The full file name with path to read.",
                "required": True
            },
            "encoding": {
                "type": "string",
                "description": "The encoding used to decode the file. Defaults to 'utf-8'.",
                "default": "utf-8"
            }
        }
    ))

    ToolRegistry.register(Tool(
        "write_to_file",
        write_to_file,
        "Write string content to a file.",
        {
            "file_path": {
                "type": "string",
                "description": "Full file name with path where the content will be written.",
                "required": True
            },
            "text": {
                "type": "string",
                "description": "Text content to be written into the file.",
                "required": True
            },
            "encoding": {
                "type": "string",
                "description": "Encoding to use for writing the file. Defaults to 'utf-8'.",
                "default": "utf-8"
            }
        }
    ))
    ToolRegistry.register(Tool(
        "generate_and_download_image",
        generate_and_download_image,
        "Generate an image using DALL-E 2 based on a prompt and download it.",
        {
            "prompt": {
                "type": "string",
                "description": "The text prompt to generate the image from.",
                "required": True
            },
            "filename": {
                "type": "string",
                "description": "The filename (including path) to save the downloaded image.",
                "required": True
            }
        }
    ))