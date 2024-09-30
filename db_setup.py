import os
import sys
from sqlalchemy import create_engine, Column, Text, BigInteger, Float
from sqlalchemy.orm import declarative_base

from dotenv import load_dotenv

load_dotenv()

# Get Supabase credentials from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: Supabase credentials not found in environment variables. Please set DATABASE_URL")
    sys.exit(1)

# Check if table name is provided as a command-line argument
if len(sys.argv) != 2:
    table_name = "multiagent"
else:
    table_name = sys.argv[1]


# Create SQLAlchemy engine
# engine = create_engine(f"postgresql://{SUPABASE_URL}?apikey={SUPABASE_KEY}")
engine = create_engine(f"{DATABASE_URL}")

# Create a base class for declarative models
Base = declarative_base()

# Define the table model
class DynamicTable(Base):
    __tablename__ = table_name

    agent = Column(Text)
    depth = Column(BigInteger)
    response = Column(Text)
    role = Column(Text)
    prompt_tokens = Column(BigInteger)
    completion_tokens = Column(BigInteger)
    input_cost = Column(Float)
    output_cost = Column(Float)
    total_cost = Column(Float)
    model_name = Column(Text)
    meta_task_id = Column(Text)
    task_id = Column(BigInteger, primary_key=True)

# Create the table
Base.metadata.create_all(engine)

print(f"Table '{table_name}' created successfully.")