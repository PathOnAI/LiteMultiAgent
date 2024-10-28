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
    io_agent_config = {
        "name": "io_agent",
        "type": "atomic",
        "agent_class": "FunctionCallingAgent",
        "meta_data":
            {
                "meta_task_id": "io_subtask",
                "task_id": 1,
                "save_to": "supabase",
                "log": "log",
                "model_name": "gpt-4o-mini",
                "tool_choice": "auto"
            },
        "tools": ["read_file", "write_to_file", "generate_and_download_image"],  
        "agent_description": "Read or write content from/to a file, or generate and save an image using text input",
        "parameter_description": "The task description detailing what to read, write, or generate. This can include file operations or image generation requests."
    }
    io_agent = agent_manager.get_agent(io_agent_config)

    # Example usage
    task = "write aaa to 1.txt, bbb to 2.txt, ccc to 3.txt"
    result = io_agent.execute(task)
    print("IO Agent Result:", result)


    task = "generate a image of a ginger cat and save it as ginger_cat.png"
    result = io_agent.execute(task)
    print("IO Agent Result:", result)



if __name__ == "__main__":
    main()