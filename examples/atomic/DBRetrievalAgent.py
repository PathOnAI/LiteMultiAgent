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
    db_retrieval_agent_config = {
        "name": "db_retrieval_agent",
        "type": "atomic",
        "agent_class": "FunctionCallingAgent",
        "meta_data":
            {
                "meta_task_id": "db_retrieval_subtask",
                "task_id": 2,
                "save_to": "csv",
                "log": "log",
                "model_name": "gpt-4o-mini",
                "tool_choice": "auto"
            },
        "tools": ["retrieve_db"], # Changed from "write_file" to "write_to_file"
        "agent_description": "Use a database retrieval agent to fetch information based on a given query.",
        "parameter_description": "The query to be processed by the database retrieval agent."
    }

    db_retrieval_agent = agent_manager.get_agent(db_retrieval_agent_config)

    task = "use supabase database, users table, look up the email (column name: email) for name is danqing2"
    result = db_retrieval_agent.execute(task)
    print("DB retrieval Agent Result:", result)



if __name__ == "__main__":
    main()