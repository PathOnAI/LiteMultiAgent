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
    file_retrieval_agent_config = {
        "name": "file_retrieval_agent",
        "type": "atomic",
        "meta_data":
            {
                "meta_task_id": "file_retrieval_subtask",
                "task_id": 3,
                "save_to": "supabase",
                "log": "log",
                "model_name": "gpt-4o-mini",
                "tool_choice": "auto"
            },
        "tools": ["retrieve_file"],
        "agent_description": "Retrieve information from local documents to answer questions or perform tasks.",
        "parameter_description": "The task description specifying the local file and the question to be answered. specify this in natural language"
    }
    file_retrieval_agent = agent_manager.get_agent(file_retrieval_agent_config)
    task = "search information in /Users/danqingzhang/Desktop/LiteMultiAgent/files/attention.pdf and answer what is transformer?"
    result = file_retrieval_agent.execute(task)
    print("File retrieval Agent Result:", result)



if __name__ == "__main__":
    main()