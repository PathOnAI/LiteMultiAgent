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

    io_agent_config = {
        "name": "io_agent",
        "type": "atomic",
        "meta_task_id": "io_subtask",
        "task_id": 1,
        "tools": ["read_file", "write_to_file", "generate_and_download_image"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Read or write content from/to a file, or generate and save an image using text input",
        "parameter_description": "The task description detailing what to read, write, or generate. This can include file operations or image generation requests."
    }


    exec_agent_config = {
        "name": "exec_agent",
        "type": "atomic",
        "meta_task_id": "exec_subtask",
        "task_id": 5,
        "tools": ["execute_shell_command", "run_python_script"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Execute some script in a subprocess, either run a bash script, or run a python script ",
        "parameter_description": "The task description describing what to execute in the subprocess."
    }


    coding_agent_config = {
        "name": "retrieval_agent",
        "type": "composite",
        "meta_task_id": "retrieval_task",
        "task_id": 6,
        "tools": ["scan_folder"],
        "sub_agents": [
            exec_agent_config,
            io_agent_config,
        ],
        "agent_description": None,
        "parameter_description": None
    }

    coding_agent = agent_manager.get_agent(coding_agent_config)

    # # # Example usage
    task = "The coding problem is: the problem is Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice.You can return the answer in any order., you first write code per instruction, then write test case, and run the test, if there is bug, debug it"
    result = coding_agent.execute(task)
    print("IO Agent Result:", result)


if __name__ == "__main__":
    main()