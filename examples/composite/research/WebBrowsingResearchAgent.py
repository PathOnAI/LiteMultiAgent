from litemultiagent.core.agent_manager import AgentManager
from litemultiagent.tools.registry import ToolRegistry, Tool
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
def main():
    agent_manager = AgentManager()
    meta_task_id = "web_browsing_task"
    task_id = 1
    io_agent_config = {
        "name": "io_agent",
        "type": "atomic",
        "agent_class": "FunctionCallingAgent",
        "meta_data":
            {
                "meta_task_id": meta_task_id,
                "task_id": task_id,
                "save_to": "csv",
                "log": "log",
                "model_name": "gpt-4o-mini",
                "tool_choice": "auto"
            },
        "tool_names": ["read_file", "write_to_file", "generate_and_download_image"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Read or write content from/to a file, or generate and save an image using text input",
        "parameter_description": "The task description detailing what to read, write, or generate. This can include file operations or image generation requests."
    }

    web_agent_config = {
        "name": "web_agent",
        "type": "atomic",
        "agent_class": "FunctionCallingAgent",
        "meta_data": {
            "meta_task_id": "webagent_task",
            "task_id": 1,
            "save_to": "csv",
            "log": "log",
            "model_name": "gpt-4o-mini",
            "tool_choice": "auto"
        },
        "tool_names": ["call_webagent"],
        "agent_description": "Use a web agent to perform tasks and fetch information from web pages based on a given instruction.",
        "parameter_description": "A natural language instruction describing the task to be performed by the web agent, including the starting URL and the goal."
    }

    agent_config = {
        "name": "web_browsing_research_agent",
        "type": "composite",
        "agent_class": "FunctionCallingAgent",
        "meta_data":
            {
                "meta_task_id": meta_task_id,
                "task_id": task_id,
                "save_to": "supabase",
                "log": "log",
                "model_name": "gpt-4o-mini",
                "tool_choice": "auto"
            },
        "tool_names": ["scan_folder"],
        "sub_agents": [
            web_agent_config,
            io_agent_config,
        ],
        "agent_description": None,
        "parameter_description": None
    }

    agent = agent_manager.get_agent(agent_config)

    # # # Example usage
    task = "first search dining table from google home page, then summarize the search result into summary.md"
    result = agent.execute(task)
    print("Agent Result:", result)


if __name__ == "__main__":
    main()