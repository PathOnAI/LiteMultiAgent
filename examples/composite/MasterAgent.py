from litemultiagent.core.agent_manager import AgentManager
from litemultiagent.core.agent_system import AgentSystem
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
    io_agent_config = {
        "name": "io_agent",
        "type": "atomic",
        "agent_class": "FunctionCallingAgent",
        "meta_data":
        {
            "model_name": "gpt-4o-mini",
            "tool_choice": "auto"
        },
        "tool_names": ["read_file", "write_to_file", "generate_and_download_image"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Read or write content from/to a file, or generate and save an image using text input",
        "parameter_description": "The task description detailing what to read, write, or generate. This can include file operations or image generation requests."
    }

    db_retrieval_agent_config = {
        "name": "db_retrieval_agent",
        "type": "atomic",
        "agent_class": "FunctionCallingAgent",
        "meta_data": {},
        "tool_names": ["retrieve_db"], # Changed from "write_file" to "write_to_file"
        "agent_description": "Use a database retrieval agent to fetch information based on a given query.",
        "parameter_description": "The query to be processed by the database retrieval agent."
    }

    file_retrieval_agent_config = {
        "name": "file_retrieval_agent",
        "type": "atomic",
        "agent_class": "FunctionCallingAgent",
        "meta_data": {},
        "tool_names": ["retrieve_file"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Retrieve information from local documents to answer questions or perform tasks.",
        "parameter_description": "The task description specifying the local file and the question to be answered. specify this in natural language"
    }

    web_retrieval_agent_config = {
        "name": "web_retrieval_agent",
        "type": "atomic",
        "agent_class": "FunctionCallingAgent",
        "meta_data": {},
        "tool_names": ["bing_search", "scrape"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Perform a search using API and return the searched results.",
        "parameter_description": "The task description describing what to read or write."
    }

    exec_agent_config = {
        "name": "exec_agent",
        "type": "atomic",
        "agent_class": "FunctionCallingAgent",
        "meta_data": {},
        "tool_names": ["execute_shell_command", "run_python_script"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Execute some script in a subprocess, either run a bash script, or run a python script ",
        "parameter_description": "The task description describing what to execute in the subprocess."
    }

    retrieval_agent_config = {
        "name": "retrieval_agent",
        "type": "composite",
        "agent_class": "FunctionCallingAgent",
        "meta_data": {},
        "tool_names": [],
        "sub_agents": [
            web_retrieval_agent_config,
            file_retrieval_agent_config,
            db_retrieval_agent_config
        ],
        "agent_description": "Use a smart research assistant to look up information using multiple sources including web search, database retrieval, and local file retrieval.",
        "parameter_description": "The task description specifying the information source (web search, database, local file) and the question to be answered. specify this in natural language"
    }

    main_agent_config = {
        "name": "main_agent",
        "type": "composite",
        "agent_class": "FunctionCallingAgent",
        "meta_data": {},
        "tool_names": ["scan_folder"],
        "sub_agents": [
            retrieval_agent_config,
            exec_agent_config,
            io_agent_config,
        ],
        "agent_description": None,
        "parameter_description": None
    }

    system_config = {
        "meta_task_id": "master_agent_task",
        "save_to": "csv",
        "log_dir": "log",
        "model_name": "gpt-4o-mini",
        "tool_choice": "auto"
    }
    agent_system = AgentSystem(main_agent_config, system_config)

    # # Example usage
    task = "generate a image of a ginger cat and save it as ginger_cat.png"
    result = agent_system.execute(task)
    print("IO Agent Result:", result)

    task = "write python script to calculate the sum from 1 to 10, and run the python script to get result"
    result = agent_system.execute(task)
    print("Exec Agent Result:", result)

    task = "browse web to search and check the brands of dining table, and summarize the results in a table, save the table into a markdown file called summary.md"
    result = agent_system.execute(task)
    print("Agent Result:", result)



if __name__ == "__main__":
    main()