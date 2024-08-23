from litemultiagent.agents.base import Agent
from typing import Any, Optional
import os

from supabase import create_client, Client
import time
import argparse
import concurrent.futures
import uuid
from litemultiagent.core.config import AGENT_TO_MODEL
from litemultiagent.utils.tools import Tools



from litemultiagent.agents.manager import AgentManager, AgentType

def scan_folder(folder_path, depth=2):
    ignore_patterns = [".*", "__pycache__"]
    file_paths = []
    for subdir, dirs, files in os.walk(folder_path):
        dirs[:] = [
            d for d in dirs
            if not any(
                d.startswith(pattern) or d == pattern for pattern in ignore_patterns
            )
        ]
        if subdir.count(os.sep) - folder_path.count(os.sep) >= depth:
            del dirs[:]
            continue
        for file in files:
            file_paths.append(os.path.join(subdir, file))
    return file_paths






model_name = AGENT_TO_MODEL["main_agent"]["model_name"]

class Main_Agent(Agent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        self.manager = AgentManager()

        available_tools = {
            "scan_folder": scan_folder,
            "use_retrieval_agent": lambda description: self.manager.use_agent(AgentType.RETRIEVE_DB, description, meta_task_id=meta_task_id, task_id=task_id),
            "use_io_agent": lambda description: self.manager.use_agent(AgentType.IO, description, meta_task_id=meta_task_id, task_id=task_id),
            "use_exec_agent": lambda description: self.manager.use_agent(AgentType.EXEC, description, meta_task_id=meta_task_id, task_id=task_id),
        }

        super().__init__("main_agent", Tools._demo, available_tools, meta_task_id, task_id)


def execute_task(query: str, meta_task_id, task_id: int) -> dict[str, Any]:
    agent = Main_Agent(meta_task_id, task_id)
    agent.messages = [{"role": "system", "content": "You are a smart research assistant. Use the search engine to look up information. \
    You are allowed to make multiple calls (either together or in sequence). \
    Only look up information when you are sure of what you want. \
    If you need to look up some information before asking a follow up question, you are allowed to do that!"}]

    start_time = time.time()
    print(query)

    # Execute the function
    response = agent.send_prompt(query)

    end_time = time.time()
    elapsed_time = end_time - start_time

    return {
        "task_id": task_id,
        "query": query,
        "elapsed_time": elapsed_time
    }

# TODO: pass use_sub_workers_parallel: bool, write_to_db: bool to agent
def execute_task(query: str, meta_task_id: str, task_id: int, use_sub_workers_parallel: bool,
                 write_to_db: bool) -> None:
    agent = Main_Agent(meta_task_id, task_id)
    agent.messages = [{"role": "system", "content": "You are a smart research assistant. Use the search engine to look up information. \
    You are allowed to make multiple calls (either together or in sequence). \
    Only look up information when you are sure of what you want. \
    If you need to look up some information before asking a follow up question, you are allowed to do that!"}]
    start_time = time.time()
    # Execute the function
    response = agent.send_prompt(query)
    end_time = time.time()
    elapsed_time = end_time - start_time


def main(queries: list[str], use_main_workers_parallel: bool, use_sub_workers_parallel: bool,
         write_to_db: bool) -> None:
    total_start_time = time.time()
    meta_task_id = str(uuid.uuid4())

    if use_main_workers_parallel:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(execute_task, query, meta_task_id, idx, use_sub_workers_parallel, write_to_db)
                for idx, query in enumerate(queries)
            ]
            concurrent.futures.wait(futures)
    else:
        for idx, query in enumerate(queries):
            execute_task(query, meta_task_id, idx, use_sub_workers_parallel, write_to_db)

    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time
    print(f"Total execution time for all tasks: {total_elapsed_time:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run agent tasks with configurable parallelism.")
    parser.add_argument("--main-workers-parallel", action="store_true", help="Enable parallel execution for main workers")
    parser.add_argument("--sub-workers-parallel", action="store_true", help="Enable parallel execution for sub-workers")
    parser.add_argument("--write-to-db", action="store_true", help="Write results to Supabase")
    args = parser.parse_args()

    queries = [
        "write aaa to 1.txt, bbb to 2.txt, ccc to 3.txt",
        "browse web to search and check the brands of dining table, and summarize the results in a table, save the table as a markdown file called summary.md",
        "generate a image of a ginger cat and save it as ginger_cat.png",
    ]

    main(queries, args.main_workers_parallel, args.sub_workers_parallel, args.write_to_db)