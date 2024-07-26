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