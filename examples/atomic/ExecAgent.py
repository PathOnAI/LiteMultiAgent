from litemultiagent.core.agent_manager import AgentManager
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
    exec_agent_config = {
        "name": "exec_agent",
        "type": "atomic",
        "meta_data":
            {
                "meta_task_id": "exec_subtask",
                "task_id": 5,
                "save_to": "csv",
                "log": "log",
                "model_name": "gpt-4o-mini",
                "tool_choice": "auto"
            },
        "tools": ["execute_shell_command", "run_python_script"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Execute some script in a subprocess, either run a bash script, or run a python script ",
        "parameter_description": "The task description describing what to execute in the subprocess."
    }
    # Create the master agent
    exec_agent = agent_manager.get_agent(exec_agent_config)

    # Example usage
    task = "pip list to show installed python environment"
    result = exec_agent.execute(task)
    print("Exec Agent Result:", result)



if __name__ == "__main__":
    main()