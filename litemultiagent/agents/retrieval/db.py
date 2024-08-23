from typing import Optional
from litemultiagent.agents.base import Agent
from litemultiagent.utils.tools import Tools

import os

from supabase import create_client, Client




def retrieve_db(client, db, input_column, output_column, input_value):
    if client == "SUPABASE":
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_ANON_KEY")

        if not url or not key:
            return "Error: SUPABASE_URL or SUPABASE_ANON_KEY environment variables are not set."

        try:
            supabase: Client = create_client(url, key)
            data = supabase.table(db).select(output_column).eq(input_column, input_value).execute()

            if data.data:
                return data.data[0][output_column]
            else:
                return f"No data found for {input_value} in {db}"

        except Exception as e:
            return f"Failed to retrieve data from Supabase: {str(e)}"
    else:
        return "not defined clients"



available_tools = {
    "retrieve_db": retrieve_db,
}

class DB_Retrieval_Agent(Agent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        super().__init__("db_retrieval_agent", Tools._db, available_tools, meta_task_id, task_id)
