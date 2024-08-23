from litemultiagent.agents.base import Agent
from litemultiagent.utils.tools import Tools

from openai import OpenAI

from typing import Any, Optional

import requests
import os


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








client = OpenAI()
available_tools = {
    "write_to_file": write_to_file,
    "read_file": read_file,
    "generate_and_download_image": generate_and_download_image,
}

class IO_Agent(Agent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        super().__init__("io_agent", Tools._io, available_tools, meta_task_id, task_id)

