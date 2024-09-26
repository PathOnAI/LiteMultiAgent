from litemultiagent.agents.core.DefaultAgent import DefaultAgent
from openai import OpenAI
from typing import Any, Optional
import requests
import os

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



available_tools = {
    "write_to_file": write_to_file,
    "read_file": read_file,
    "generate_and_download_image": generate_and_download_image,
}

class IOAgent(DefaultAgent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        super().__init__("use_io_agent", tools, available_tools, meta_task_id, task_id)




if __name__ == "__main__":
    def use_io_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
        agent = IOAgent(meta_task_id, task_id)
        agent.messages = [{"role": "system", "content":"You are an ai agent that read and write files"}]
        return agent.send_prompt(query)
    
    def main():
        response = use_io_agent("write aaa to 1.txt, bbb to 2.txt, ccc to 3.txt")
        print(response)
        response = use_io_agent("generate a image of a ginger cat and save it as ginger_cat.png")
        print(response)

    main()