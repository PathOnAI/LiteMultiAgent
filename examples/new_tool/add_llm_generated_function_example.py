import logging
import json
import traceback
from dotenv import load_dotenv
from litemultiagent.tools.tool_creation_agent import ToolCreationAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log.txt", mode="w"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def main():
    """
    Demonstrates usage of the ToolCreationAgent class for tool creation and testing.
    Creates a calculator tool and tests it with basic arithmetic operations.
    """
    # Initialize the agent with specified model
    tool_creation_agent = ToolCreationAgent(model_name="anthropic/claude-3-5-sonnet-20240620")

    # Define tool specifications
    tool_specs = {
        "calculator": "Create a calculator tool that can perform basic operations (add, subtract, multiply, divide) between two numbers"
    }

    # Create tools based on specifications
    mapping = {}
    for description, spec in tool_specs.items():
        result = tool_creation_agent.send_prompt(spec)

        if result:
            name, func, description, parameters = result
            print(f"\nCreated tool: {name}")
            print(f"Description: {description}")
            print(f"Parameters: {json.dumps(parameters, indent=2)}")
            mapping[spec] = [name, func, description, parameters]

    # Cleanup resources
    tool_creation_agent.cleanup_cache()

    # Set up agent manager and tools
    from litemultiagent.core.agent_manager import AgentManager
    from litemultiagent.tools.registry import Tool

    agent_manager = AgentManager()
    new_tools = [
        Tool(name, func, description, parameters)
        for spec in mapping
        for name, func, description, parameters in [mapping[spec]]
    ]

    # Configure test agent
    test_agent_config = {
        "name": "test_agent",
        "type": "atomic",
        "agent_class": "FunctionCallingAgent",
        "meta_data": {
            "meta_task_id": "io_subtask",
            "task_id": 1,
            "save_to": "supabase",
            "log": "log",
            "model_name": "gpt-4o-mini",
            "tool_choice": "auto"
        },
        "tool_names": ["read_file", "write_to_file", "generate_and_download_image"],
        "self_defined_tools": new_tools,
        "agent_description": "test ai agent",
        "parameter_description": "test ai agent"
    }

    # Initialize and test the agent
    test_agent = agent_manager.get_agent(test_agent_config)

    # Test calculator functionality
    test_cases = [
        ("calculate 3+4", "Addition test"),
        ("calculate 3 times 4", "Multiplication test")
    ]

    for task, description in test_cases:
        result = test_agent.execute(task)
        print(f"{description} - Task: {task}")
        print(f"Result: {result}")



if __name__ == "__main__":
    main()