from litemultiagent.agents.base import Agent
from litemultiagent.agents.exec import Exec_Agent
from litemultiagent.agents.io import IO_Agent
from litemultiagent.agents.retrieval.db import DB_Retrieval_Agent
from litemultiagent.agents.retrieval.file import File_Retrieval_Agent
# from agents.retrieval import Retrieval_Agent
from litemultiagent.agents.retrieval.web import Web_Retrieval_Agent

from typing import Optional
from enum import Enum

class AgentType(Enum):
    EXEC = 'exec'
    IO = 'io'
    RETRIEVE = 'retrieve'
    RETRIEVE_WEB = 'retrieve_web'
    RETRIEVE_FILE = 'retrieve_file'
    RETRIEVE_DB = 'retrieve_db'


class AgentManager:
    def __init__(self):
        self.agents = {}
        self.current_agent: Agent | None = None

    def use_agent(self, type_: AgentType, query: str,  meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
        if type_ == AgentType.EXEC:
            agent = Exec_Agent(meta_task_id, task_id)
            agent.messages = [{"role": "system", "content":"You will exec some scripts. Either by shell or run python script"}]
        elif type_ == AgentType.IO:
            agent = IO_Agent(meta_task_id, task_id)
            agent.messages = [{"role": "system", "content":"You are an ai agent that read and write files"}]
        # elif type_ == AgentType.RETRIEVE:
        #     agent = Retrieval_Agent(meta_task_id, task_id)
        #     agent.messages = [{"role":"system", "content" :"You are a smart research assistant. Use the search engine to look up information."}]
        elif type_ == AgentType.RETRIEVE_DB:
            agent = DB_Retrieval_Agent(meta_task_id, task_id)
            agent.messages = [{"role":"system", "content":"You are a smart assistant, you retrieve information from database"}]
        elif type_ == AgentType.RETRIEVE_FILE:
            agent = File_Retrieval_Agent(meta_task_id, task_id)
            agent.messages = [{"role":"system", "content": "You are a smart assistant and you will retrieve information from local document to answer questions or perform tasks."}]
        elif type_ == AgentType.RETRIEVE_WEB:
            agent = Web_Retrieval_Agent(meta_task_id, task_id)
            agent.messages = [{"role" :"system", "content": "You are a smart research assistant. Use the search engine to look up information."}]

        self.current_agent = agent

        res = agent.send_prompt(query)
        print(res)

        return res



def main():
    manager = AgentManager()

    response = manager.use_agent(
        AgentType.EXEC,
        "read file 3 lines of file agent.py in the current folder")
    print(response)

    response = manager.use_agent(
        AgentType.EXEC,
        "pip list to show installed python environment")
    print(response)

    response = manager.use_agent(
        AgentType.EXEC,
        "show me the python path of this virtual environment")
    print(response)

    response = manager.use_agent(AgentType.IO, "write aaa to 1.txt, bbb to 2.txt, ccc to 3.txt")
    print(response)

    response = manager.use_agent(AgentType.IO, "generate a image of a ginger cat and save it as ginger_cat.png")
    print(response)

    response = manager.use_agent(AgentType.RETRIEVE_DB, "use supabase database, users table, look up the email (column name: email) for name is danqing2", 0, 0)
    print(response)


    response = manager.use_agent(AgentType.RETRIEVE_FILE, "search information in ./files/attention.pdf and answer what is transformer?", 0, 0)
    print(response)
    print(manager.current_agent.messages)

    response = manager.use_agent(
        AgentType.RETRIEVE_DB,
        "use supabase database, users table, look up the email (column name: email) for name is danqing2", "test", 0)
    print(response)

    response = manager.use_agent(AgentType.RETRIEVE_WEB, "Fetch the UK's GDP over the past 5 years", 0, 0)
    print(response)

if __name__ == "__main__":
    main()