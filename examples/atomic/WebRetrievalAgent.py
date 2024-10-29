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
    web_retrieval_agent_config = {
        "name": "web_retrieval_agent",
        "type": "atomic",
        "agent_class": "HighLevelPlanningAgent",
        "meta_data":
            {
                "meta_task_id": "web_retrieval_subtask",
                "task_id": 4,
                "save_to": "csv",
                "log": "log",
                "model_name": "gpt-4o-mini",
                "tool_choice": "auto"
            },
        "tool_names": ["bing_search", "scrape"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Perform a search using API and return the searched results.",
        "parameter_description": "The task description describing what to read or write."
    }
    web_retrieval_agent = agent_manager.get_agent(web_retrieval_agent_config)

    task = "Fetch the UK's GDP over the past 5 years"
    result = web_retrieval_agent.execute(task)
    print("Web retrieval Agent Result:", result)



if __name__ == "__main__":
    main()