from litemultiagent.core.agent_manager import AgentManager
from litemultiagent.tools.registry import ToolRegistry, Tool
import logging

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

    # ## (1) atomic agent: io agent
    io_agent_config = {
        "name": "io_agent",
        "type": "atomic",
        "meta_task_id": "io_subtask",
        "task_id": 1,
        "tools": ["read_file", "write_to_file", "generate_and_download_image"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Read or write content from/to a file, or generate and save an image using text input",
        "parameter_description": "The task description detailing what to read, write, or generate. This can include file operations or image generation requests."
    }
    # io_agent = agent_manager.get_agent(io_agent_config)
    #
    # # Example usage
    # task = "write aaa to 1.txt, bbb to 2.txt, ccc to 3.txt"
    # result = io_agent.execute(task)
    # print("IO Agent Result:", result)
    #
    #
    # task = "generate a image of a ginger cat and save it as ginger_cat.png"
    # result = io_agent.execute(task)
    # print("IO Agent Result:", result)
    #
    # (2) atomic agent: db retrieval agent
    # # Define a composite agent configuration with nested sub-agents and tools
    db_retrieval_agent_config = {
        "name": "db_retrieval_agent",
        "type": "atomic",
        "meta_task_id": "db_retrieval_subtask",
        "task_id": 2,
        "tools": ["retrieve_db"], # Changed from "write_file" to "write_to_file"
        "agent_description": "Use a database retrieval agent to fetch information based on a given query.",
        "parameter_description": "The query to be processed by the database retrieval agent."
    }
    # # Create the master agent
    # db_retrieval_agent = agent_manager.get_agent(db_retrieval_agent_config)
    #
    # # Example usage
    # task = "use supabase database, users table, look up the email (column name: email) for name is danqing2"
    # result = db_retrieval_agent.execute(task)
    # print("DB retrieval Agent Result:", result)

    ## (3) atomic agent: file retrieval agent
    file_retrieval_agent_config = {
        "name": "file_retrieval_agent",
        "type": "atomic",
        "meta_task_id": "file_retrieval_subtask",
        "task_id": 3,
        "tools": ["retrieve_file"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Retrieve information from local documents to answer questions or perform tasks.",
        "parameter_description": "The task description specifying the local file and the question to be answered. specify this in natural language"
    }
    # # Create the master agent
    # file_retrieval_agent = agent_manager.get_agent(file_retrieval_agent_config)
    #
    # # Example usage
    # task = "search information in /Users/danqingzhang/Desktop/LiteMultiAgent/files/attention.pdf and answer what is transformer?"
    # result = file_retrieval_agent.execute(task)
    # print("File retrieval Agent Result:", result)

    ## (4) atomic agent: web retrieval agent
    web_retrieval_agent_config = {
        "name": "web_retrieval_agent",
        "type": "atomic",
        "meta_task_id": "web_retrieval_subtask",
        "task_id": 4,
        "tools": ["bing_search", "scrape"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Perform a search using API and return the searched results.",
        "parameter_description": "The task description describing what to read or write."
    }
    # # Create the master agent
    # web_retrieval_agent = agent_manager.get_agent(web_retrieval_agent_config)
    #
    # # Example usage
    # task = "Fetch the UK's GDP over the past 5 years"
    # result = web_retrieval_agent.execute(task)
    # print("Web retrieval Agent Result:", result)

    ## (5) atomic agent: exec agent
    exec_agent_config = {
        "name": "exec_agent",
        "type": "atomic",
        "meta_task_id": "exec_subtask",
        "task_id": 5,
        "tools": ["execute_shell_command", "run_python_script"],  # Changed from "write_file" to "write_to_file"
        "agent_description": "Execute some script in a subprocess, either run a bash script, or run a python script ",
        "parameter_description": "The task description describing what to execute in the subprocess."
    }
    # # Create the master agent
    # exec_agent = agent_manager.get_agent(exec_agent_config)
    #
    # # Example usage
    # task = "pip list to show installed python environment"
    # result = exec_agent.execute(task)
    # print("Exec Agent Result:", result)

    ## (6) retrieval agent
    retrieval_agent_config = {
        "name": "retrieval_agent",
        "type": "composite",
        "meta_task_id": "retrieval_task",
        "task_id": 6,
        "tools": [],
        "sub_agents": [
            web_retrieval_agent_config,
            file_retrieval_agent_config,
            db_retrieval_agent_config
        ],
        "agent_description": "Use a smart research assistant to look up information using multiple sources including web search, database retrieval, and local file retrieval.",
        "parameter_description": "The task description specifying the information source (web search, database, local file) and the question to be answered. specify this in natural language"
    }
    # retrieval_agent = agent_manager.get_agent(retrieval_agent_config)
    # # # Example usage
    # task = "search information in /Users/danqingzhang/Desktop/LiteMultiAgent/files/attention.pdf and answer what is transformer?"
    # result = retrieval_agent.execute(task)
    # print("Retrieval Agent Result:", result)

    ## 7. main agent
    main_agent_config = {
        "name": "retrieval_agent",
        "type": "composite",
        "meta_task_id": "retrieval_task",
        "task_id": 6,
        "tools": ["scan_folder"],
        "sub_agents": [
            retrieval_agent_config,
            exec_agent_config,
            io_agent_config,
        ],
        "agent_description": None,
        "parameter_description": None
    }
    # Create the master agent
    main_agent = agent_manager.get_agent(main_agent_config)

    # # # Example usage
    task = "generate a image of a ginger cat and save it as ginger_cat.png"
    result = main_agent.execute(task)
    print("IO Agent Result:", result)

    task = "write python script to calculate the sum from 1 to 10, and run the python script to get result"
    result = main_agent.execute(task)
    print("IO Agent Result:", result)

    task = "browse web to search and check the brands of dining table, and summarize the results in a table, save the table into a markdown file called summary.md"
    result = main_agent.execute(task)
    print("IO Agent Result:", result)



if __name__ == "__main__":
    main()