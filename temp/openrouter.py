from openai import OpenAI
import os
from dotenv import load_dotenv
import json
_ = load_dotenv()

_ = load_dotenv()


# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

models = ["openai/gpt-4o-mini", "google/gemini-flash-1.5", "meta-llama/llama-3.1-8b-instruct:free"]

for model in models:
    completion = client.chat.completions.create(
      model=model,
      messages=[
        {
          "role": "user",
          "content": "Say this is a test",
        },
      ],
    )
    print(model)
    print(completion.choices[0].message.content)

