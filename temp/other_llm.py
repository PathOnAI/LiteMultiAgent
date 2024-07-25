from openai import OpenAI
import os
from dotenv import load_dotenv
import json
_ = load_dotenv()

api_key = os.getenv("MOONSHOT_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.moonshot.cn/v1",
)

response = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": "编程判断 3214567 是否是素数。"}
    ],
    tools=[{
        "type": "function",
        "function": {
            "name": "CodeRunner",
            "description": "代码执行器，支持运行 python 和 javascript 代码",
            "parameters": {
                "properties": {
                    "language": {
                        "type": "string",
                        "enum": ["python", "javascript"]
                    },
                    "code": {
                        "type": "string",
                        "description": "代码写在这里"
                    }
                },
                "type": "object"
            }
        }
    }],
    temperature=0.3,
    tool_choice="auto"
)

print(response.choices[0].message)
print(response)
print(json.dumps(response.choices[0].message.model_dump()))
print(response.usage.prompt_tokens)
print(response.usage.completion_tokens)