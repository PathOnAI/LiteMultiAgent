import logging
from datetime import datetime
import os
import csv
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from dotenv import load_dotenv
from litemultiagent.core.agent_manager import AgentManager

_ = load_dotenv()
logger = logging.getLogger(__name__)

# Initialize Supabase client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
supabase: Optional[Client] = None
if url and key:
    try:
        supabase = create_client(url, key)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")

class AgentSystem:
    def __init__(self, main_agent_config, system_config: Dict[str, Any]) -> None:

        # TODO: add shared_memory
        # TODO: add shared_context
        # set up agent hierarchy
        agent_manager = AgentManager()
        self.main_agent = agent_manager.get_agent(main_agent_config)

        # set up agent system shared config
        # create shared_config for agents to share
        self.shared_config = {
            "task_id": 0,
            "system_name": system_config["system_name"],
            "log_dir": system_config["log_dir"],
            "save_to": system_config["save_to"],
            "system_runtime_id": system_config["system_runtime_id"],
            "model_name": system_config["model_name"],
            "tool_choice": system_config["tool_choice"]
        }
        self.main_agent.set_shared_config(self.shared_config)

    def execute(self, task: str):
        self.shared_config["task_id"] += 1
        return self.main_agent.execute(task)
