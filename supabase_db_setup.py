import os
import sys
from sqlalchemy import create_engine, Column, Text, BigInteger, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()

# Get Supabase credentials from environment variables
SUPABASE_DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL")

if not SUPABASE_DATABASE_URL:
    print("Error: Supabase credentials not found in environment variables. Please set SUPABASE_DATABASE_URL")
    sys.exit(1)

# Check if table name is provided as a command-line argument
if len(sys.argv) != 2:
    table_name = "multiagent"
else:
    table_name = sys.argv[1]


# Create SQLAlchemy engine
engine = create_engine(f"{SUPABASE_DATABASE_URL}")

# Create a base class for declarative models
Base = declarative_base()

# Define the table model
class DynamicTable(Base):
    __tablename__ = table_name

    # Add the 'id' column as the primary key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # Add the 'created_at' column with automatic timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

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
    system_name = Column(Text)
    system_runtime_id = Column(Text)
    task_id = Column(BigInteger)

# Create the table
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Add a test entry
new_entry = DynamicTable(
    agent="Test Agent",
    depth=1,
    response="Sample response",
    role="Test Role",
    prompt_tokens=10,
    completion_tokens=5,
    input_cost=0.5,
    output_cost=0.3,
    total_cost=0.8,
    model_name="Test Model",
    system_name="ai system",
    system_runtime_id="12345",
    task_id=1
)

# Add and commit the new entry to the database
session.add(new_entry)
session.commit()

print(f"Table '{table_name}' created successfully and test entry added.")