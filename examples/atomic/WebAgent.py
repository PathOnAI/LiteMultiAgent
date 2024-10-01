from litemultiagent.core.agent_manager import AgentManager
from litemultiagent.tools.registry import ToolRegistry, Tool
import logging

from litemultiagent.tools.web_agent import call_webagent_tool

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

    ToolRegistry.register(
        call_webagent_tool
    )

    web_agent_config = {
        "name": "web_agent",
        "type": "atomic",
        "meta_data": {
            "meta_task_id": "webagent_task",
            "task_id": 1,
            "save_to": "csv",
            "log": "log",
            "model_name": "gpt-4o-mini",
            "tool_choice": "auto"
        },
        "tools": ["call_webagent"],
        "agent_description": "Use a web agent to perform tasks and fetch information from web pages based on a given instruction.",
        "parameter_description": "A natural language instruction describing the task to be performed by the web agent, including the starting URL and the goal."
    }

    web_agent = agent_manager.get_agent(web_agent_config)

    task = "search dining table on google"
    result = web_agent.execute(task)
    print("Web Agent Result:", result)



if __name__ == "__main__":
    main()