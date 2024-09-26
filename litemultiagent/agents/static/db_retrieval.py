from litemultiagent.agents.core.DefaultAgent import DefaultAgent

from typing import Optional

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

tools = [{
  "type": "function",
  "function": {
    "name": "retrieve_db",
    "description": "Retrieve data from a specified database (currently supports Supabase) based on input parameters.",
    "parameters": {
      "type": "object",
      "properties": {
        "client": {
          "type": "string",
          "description": "The database client to use. Currently supports 'SUPABASE'."
        },
        "db": {
          "type": "string",
          "description": "The name of the database table to query."
        },
        "input_column": {
          "type": "string",
          "description": "The column name to search in."
        },
        "output_column": {
          "type": "string",
          "description": "The column name to retrieve data from."
        },
        "input_value": {
          "type": "string",
          "description": "The value to search for in the input column."
        }
      },
      "required": [
        "client",
        "db",
        "input_column",
        "output_column",
        "input_value"
      ]
    }
  }
}]

available_tools = {
    "retrieve_db": retrieve_db,
}

class DatabaseRetrievalAgent(DefaultAgent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        super().__init__("use_db_retrieval_agent", tools, available_tools, meta_task_id, task_id)

if __name__ == "__main__":
    def use_db_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
        agent = DatabaseRetrievalAgent(meta_task_id, task_id)
        agent.messages = [{"role":"system", "content":"You are a smart assistant, you retrieve information from database"}]
        return agent.send_prompt(query)
    
    def main():
        response = use_db_retrieval_agent("use supabase database, users table, look up the email (column name: email) for name is danqing2", 0, 0)
        print(response)

    main()
