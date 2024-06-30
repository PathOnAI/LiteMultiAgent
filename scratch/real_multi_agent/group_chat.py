# different LLM
# different agent framework
# for loop to start the chat
# https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat.ipynb
# user_proxy, code, pm

import logging
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from typing import Any
from pydantic import BaseModel, validator
import requests
import os
import json
_ = load_dotenv()
# Initialize logging

from utils import *



pm_agent = Agent(name="Product_manager", system_prompt="Creative in software product ideas.",)
# response = pm_agent.get_response("Find a latest paper about gpt-4 on arxiv and find its potential applications in software.")
# print(response)
# print(pm_agent.messages)

swe_agent = Agent(name="Software Engineer", system_prompt="Tend to write some code to facilitate discussion.",)
# response = pm_agent.get_response("Find a latest paper about gpt-4 on arxiv and find its potential applications in software.")
# print(response)
# print(pm_agent.messages)

shared_messages = []

response = pm_agent.get_response("Find a latest paper about gpt-4 on arxiv and find its potential applications in software.")
message = AssistantMessage(**response.choices[0].message.model_dump())
swe_agent.append_message(message)
shared_messages.append({'job': 'pm', 'message': message})
response = swe_agent.get_response("response based on current conversations, provide suggestions or different opinion to facilitate the discussion, if possible, write script")
message = AssistantMessage(**response.choices[0].message.model_dump())
pm_agent.append_message(message)
shared_messages.append({'job': 'swe', 'message': message})


for i in range(2):
    response = pm_agent.get_response(
        "response based on current conversations, provide suggestions or different opinion to facilitate the discussion")
    message = AssistantMessage(**response.choices[0].message.model_dump())
    swe_agent.append_message(message)
    shared_messages.append({'job': 'pm', 'message': message})
    response = swe_agent.get_response(
        "response based on current conversations, provide suggestions or different opinion to facilitate the discussion, if possible, write script")
    message = AssistantMessage(**response.choices[0].message.model_dump())
    pm_agent.append_message(message)
    shared_messages.append({'job': 'swe', 'message': message})


def save_messages_to_json(messages, filename="group_chat_messages.json"):
    # Create a list to store the formatted messages
    formatted_messages = []

    for index, message in enumerate(messages):
        # Print the message info
        print(index, message)

        # Format the message for JSON
        if 'job' in message:
            formatted_message = {
                "index": index,
                "job": message['job'],
                "role": message['message'].role,
                "message": str(message),  # Convert message to string in case it's not serializable
            }
        else:
            formatted_message = {
                "index": index,
                "role": message.role,
                "message": str(message),  # Convert message to string in case it's not serializable
            }
        formatted_messages.append(formatted_message)

    # Save the formatted messages to a JSON file
    with open(filename, 'w') as f:
        json.dump(formatted_messages, f, indent=2)

    print(f"Messages saved to {filename}")

save_messages_to_json(shared_messages, filename="group_chat_messages.json")
save_messages_to_json(pm_agent.messages, filename="pm_messages.json")
save_messages_to_json(swe_agent.messages, filename="swe_messages.json")



