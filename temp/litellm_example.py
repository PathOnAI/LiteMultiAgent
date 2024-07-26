from litellm import completion
import os
from dotenv import load_dotenv
_ = load_dotenv()


## set ENV variables
# os.environ["OPENAI_API_KEY"] = "your-openai-key"

# os.environ["COHERE_API_KEY"] = "your-cohere-key"


messages = [{ "content": "Hello, how are you?", "role": "user"}]

# openai call
response = completion(model="claude-3-5-sonnet-20240620", messages=messages)
print(response)

# # cohere call
# response = completion(model="command-nightly", messages=messages)
# print(response)


messages = [
    {"role": "user", "content": "What is the weather like in Boston?"}
]

def get_current_weather(location):
  if location == "Boston, MA":
    return "The weather is 12F"

functions = [
    {
      "name": "get_current_weather",
      "description": "Get the current weather in a given location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA"
          },
          "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"]
          }
        },
        "required": ["location"]
      }
    }
  ]

response = completion(model="gpt-4o-mini", messages=messages, functions=functions)
print(response)
print(type(response))
function_call_data = response["choices"][0]["message"]["function_call"]
print(function_call_data)
print(type(function_call_data))
# import json
# function_name = function_call_data['name']
# function_args = function_call_data['arguments']
# function_args = json.loads(function_args)
# print(function_name, function_args)
#
#
# messages = [
#     {"role": "user", "content": "What is the weather like in Boston?"},
#     {"role": "assistant", "content": None, "function_call": {"name": "get_current_weather", "arguments": "{ \"location\": \"Boston, MA\"}"}},
#     {"role": "function", "name": "get_current_weather", "content": result}
# ]
# response = completion(model="gpt-4o-mini", messages=messages, functions=functions)
# print(response)

