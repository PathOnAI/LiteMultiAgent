import logging
from litemultiagent.core.agent_system import AgentSystem
import uuid

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
        "meta_data":{},
        "tool_names": ["read_file", "write_to_file", "generate_and_download_image"],
        "system_prompt": "You are an ai agent, Read or write content from/to a file, or generate and save an image using text input",
        "agent_description": None,
        "parameter_description": None,
    }

    system_config = {
        "system_name": "io_agent_system",
        "system_runtime_id": str(uuid.uuid4()),
        "save_to": "csv",
        "log_dir": "log",
        "model_name": "gpt-4o-mini",
        "tool_choice": "auto"
    }
    agent_system = AgentSystem(io_agent_config, system_config)

    # Example usage
    task = "write aaa to 1.txt, bbb to 2.txt, ccc to 3.txt"
    result = agent_system.execute(task)
    print("IO Agent Result:", result)


    task = "generate a image of a ginger cat and save it as ginger_cat.png"
    result = agent_system.execute(task)
    print("IO Agent Result:", result)



if __name__ == "__main__":
    main()