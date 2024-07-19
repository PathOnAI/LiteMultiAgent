from dotenv import load_dotenv, find_dotenv
import os
from supabase import create_client, Client

# Load environment variables
load_dotenv(find_dotenv())

# Initialize Supabase client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

# Define the table name
table_name = "multiagent"

# Function to insert a sample row (for testing)
def insert_sample_data():
    try:
        data = supabase.table(table_name).insert({"agent": "test_agent", "depth": 1, "response": "test_response"}).execute()
        print("Sample data inserted successfully:", data)
    except Exception as e:
        print(f"An error occurred while inserting sample data: {str(e)}")

# Function to retrieve data (for testing)
def get_data():
    try:
        data = supabase.table(table_name).select("*").execute()
        print("Retrieved data:", data)
    except Exception as e:
        print(f"An error occurred while retrieving data: {str(e)}")

# Call the functions
insert_sample_data()
get_data()