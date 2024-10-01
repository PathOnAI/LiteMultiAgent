import os

from supabase import create_client, Client

from litemultiagent.tools.registry import Tool

def retrieve_db(client, db, input_column, output_column, input_value):
    if client == "SUPABASE":
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_ANON_KEY")

        if not url or not key:
            return "Error: SUPABASE_URL or SUPABASE_ANON_KEY environment variables are not set."

        try:
            supabase: Client = create_client(url, key)
            data = supabase.table(db).select(output_column).eq(
                input_column, input_value).execute()

            if data.data:
                return data.data[0][output_column]
            else:
                return f"No data found for {input_value} in {db}"

        except Exception as e:
            return f"Failed to retrieve data from Supabase: {str(e)}"
    else:
        return "not defined clients"

retrieve_db_tool = Tool(
    "retrieve_db",
    retrieve_db,
    "Retrieve data from a specified database (currently supports Supabase) based on input parameters.",
    {
        "client": {
            "type": "string",
            "description": "The database client to use. Currently supports 'SUPABASE'.",
            "required": True
        },
        "db": {
            "type": "string",
            "description": "The name of the database table to query.",
            "required": True
        },
        "input_column": {
            "type": "string",
            "description": "The column name to search in.",
            "required": True
        },
        "output_column": {
            "type": "string",
            "description": "The column name to retrieve data from.",
            "required": True
        },
        "input_value": {
            "type": "string",
            "description": "The value to search for in the input column.",
            "required": True
        }
    }
)
