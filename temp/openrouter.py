from openai import OpenAI
import os
from dotenv import load_dotenv
import json
_ = load_dotenv()

import logging
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


# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

# "anthropic/claude-3.5-sonnet",
# "meta-llama/llama-3.1-8b-instruct:free"
models = ["openai/gpt-4o-mini", "google/gemini-flash-1.5"]

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
    print(completion)
    print(completion.choices[0].message.content)

