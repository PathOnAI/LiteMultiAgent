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
    meta_task_id = "research_task"
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

    web_retrieval_agent_config = {
        "name": "web_retrieval_agent",
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
        "tool_names": ["bing_search", "scrape"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Perform a search using API and return the searched results.",
        "parameter_description": "The task description describing what to read or write."
    }

    exec_agent_config = {
        "name": "exec_agent",
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
        "tool_names": ["execute_shell_command", "run_python_script"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Execute some script in a subprocess, either run a bash script, or run a python script ",
        "parameter_description": "The task description describing what to execute in the subprocess."
    }


    research_agent_config = {
        "name": "retrieval_agent",
        "type": "composite",
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
        "tool_names": ["scan_folder"],
        "sub_agents": [
            web_retrieval_agent_config,
            exec_agent_config,
            io_agent_config,
        ],
        "agent_description": None,
        "parameter_description": None
    }

    research_agent = agent_manager.get_agent(research_agent_config)

    # # # Example usage
    task = "Fetch the UK's GDP over the past 5 years, then write python script to draw a line graph of it and save the image to the current folder. And then run the python script."
    result = research_agent.execute(task)
    print("Research Agent Result:", result)


if __name__ == "__main__":
    main()