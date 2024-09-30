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
    meta_task_id = "retrieval_task"
    task_id = 1
    db_retrieval_agent_config = {
        "name": "db_retrieval_agent",
        "type": "atomic",
        "meta_data":
            {
                "meta_task_id": meta_task_id,
                "task_id": task_id,
                "save_to": "csv",
                "log": "log"
            },
        "tools": ["retrieve_db"], # Changed from "write_file" to "write_to_file"
        "agent_description": "Use a database retrieval agent to fetch information based on a given query.",
        "parameter_description": "The query to be processed by the database retrieval agent."
    }

    file_retrieval_agent_config = {
        "name": "file_retrieval_agent",
        "type": "atomic",
        "meta_data":
            {
                "meta_task_id": meta_task_id,
                "task_id": task_id,
                "save_to": "csv",
                "log": "log"
            },
        "tools": ["retrieve_file"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Retrieve information from local documents to answer questions or perform tasks.",
        "parameter_description": "The task description specifying the local file and the question to be answered. specify this in natural language"
    }

    web_retrieval_agent_config = {
        "name": "web_retrieval_agent",
        "type": "atomic",
        "meta_data":
            {
                "meta_task_id": meta_task_id,
                "task_id": task_id,
                "save_to": "csv",
                "log": "log"
            },
        "tools": ["bing_search", "scrape"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Perform a search using API and return the searched results.",
        "parameter_description": "The task description describing what to read or write."
    }

    retrieval_agent_config = {
        "name": "retrieval_agent",
        "type": "composite",
        "meta_data":
            {
                "meta_task_id": meta_task_id,
                "task_id": task_id,
                "save_to": "csv",
                "log": "log"
            },
        "tools": [],
        "sub_agents": [
            web_retrieval_agent_config,
            file_retrieval_agent_config,
            db_retrieval_agent_config
        ],
        "agent_description": "Use a smart research assistant to look up information using multiple sources including web search, database retrieval, and local file retrieval.",
        "parameter_description": "The task description specifying the information source (web search, database, local file) and the question to be answered. specify this in natural language"
    }
    retrieval_agent = agent_manager.get_agent(retrieval_agent_config)
    # # # Example usage
    task = "Fetch the UK's GDP over the past 5 years"
    result = retrieval_agent.execute(task)
    print("Retrieval Agent Result:", result)



if __name__ == "__main__":
    main()