import logging

MODEL_COST = {
    "gpt-4o-mini": {
        "input_price_per_1m": 0.15,
        "output_price_per_1m": 0.6,
    },
    "gemini/gemini-pro": {
        "input_price_per_1m": 0,
        "output_price_per_1m": 0,
    },
    "claude-3-5-sonnet-20240620": {
        "input_price_per_1m": 3,
        "output_price_per_1m": 15,
    },
    "groq/llama3-8b-8192": {
        "input_price_per_1m": 0.05,
        "output_price_per_1m": 0.08,
    },
}

AGENT_TO_MODEL = {
    "main_agent":
        {
            "model_name": "gpt-4o-mini",
            "tool_choice": "auto",
        },
    "io_agent": {
        "model_name": "claude-3-5-sonnet-20240620",
        "tool_choice": "auto",
    },
    "retrieval_agent": {
        "model_name": "gpt-4o-mini",
        "tool_choice": "auto",
    },
    "web_retrieval_agent": {
        "model_name": "gpt-4o-mini",
        "tool_choice": "auto",
    },
    "db_retrieval_agent": {
        "model_name": "gpt-4o-mini",
        "tool_choice": "auto",
    },
    "exec_agent": {
        "model_name": "claude-3-5-sonnet-20240620",
        "tool_choice": "auto",
    },
    "file_retrieval_agent": {
        "model_name": "gpt-4o-mini",
        "tool_choice": "auto",
    },
}


class Config:
    def __init__(self):
        self.use_parallel = True
        self.max_workers = None


# Create a global configuration object
function_calling_config = Config()

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
LiteMultiAgentLogger = logging.getLogger(__name__)
AgentLogger = logging.getLogger('BaseAgent')
