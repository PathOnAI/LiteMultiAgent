import logging
from datetime import datetime
import os
import csv
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from dotenv import load_dotenv

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
        self.task_id = 0
        self.log_dir = system_config["log_dir"]
        self.save_to = system_config["save_to"]
        self.meta_task_id = system_config["meta_task_id"]
        self.model_name = system_config["model_name"]
        self.tool_choice = system_config["tool_choice"]

        # Move import here to avoid cirecular import
        from litemultiagent.core.agent_manager import AgentManager
        agent_manager = AgentManager()
        self.main_agent = agent_manager.get_agent(main_agent_config)
        self.main_agent.set_system(self)

    def execute(self, task: str):
        self.task_id += 1
        self.main_agent.execute(task)

    def save_to_csv(self, data):
        filename = os.path.join(self.log_dir, f"multiagent_data_{datetime.now().strftime('%Y%m%d')}.csv")
        file_exists = os.path.isfile(filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # If file doesn't exist, create it with header
        if not file_exists:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = list(data.keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            logger.info(f"Created new CSV file with header: {filename}")

        # Append data to the file
        with open(filename, 'a', newline='') as csvfile:
            fieldnames = list(data.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data)

        logger.info(f"Data saved to CSV: {filename}")

    def save_to_supabase(self, data):
        if supabase is None:
            logger.warning("Supabase client is not initialized. Skipping database save.")
            return
        try:
            supabase.table("multiagent").insert(data).execute()
        except Exception as e:
            logger.error(f"Failed to save data to Supabase: {e}")