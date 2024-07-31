# from typing import Any, Optional

# from agents.base import Agent
# from agents.manager import use_db_retrieval_agent, use_file_retrieval_agent
# from agents.manager import use_web_retrieval_agent

# from utils.tools import Tools


# class Retrieval_Agent(Agent):
#     def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
#         # Create a wrapper for use_db_retrieval_agent that includes meta_task_id and task_id
#         def wrapped_use_db_retrieval_agent(query: str) -> str:
#             return use_db_retrieval_agent(query, meta_task_id=meta_task_id, task_id=task_id)

#         def wrapped_use_web_retrieval_agent(query: str) -> str:
#             return use_web_retrieval_agent(query, meta_task_id=meta_task_id, task_id=task_id)

#         def wrapped_use_file_retrieve_agent(query: str) -> str:
#             return use_file_retrieval_agent(query, meta_task_id=meta_task_id, task_id=task_id)

#         available_tools = {
#             "use_db_retrieval_agent": wrapped_use_db_retrieval_agent,
#             "use_web_retrieval_agent": wrapped_use_web_retrieval_agent,
#             "use_file_retrieve_agent": wrapped_use_file_retrieve_agent,
#         }

#         super().__init__("retrieval_agent", Tools._retrieve, available_tools, meta_task_id, task_id)
