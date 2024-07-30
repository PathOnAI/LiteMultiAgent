from agents.exec import Exec_Agent
from agents.io import IO_Agent
from agents.db_retrieval import DB_Retrieval_Agent
from agents.file_retrieval import File_Retrieval_Agent
from agents.retrieval import Retrieval_Agent
from agents.web_retrieval import Web_Retrieval_Agent

from typing import Optional


def use_exec_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = Exec_Agent(meta_task_id, task_id)
    agent.messages = [{"role": "system", "content":"You will exec some scripts. Either by shell or run python script"}]
    return agent.send_prompt(query)

def use_io_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = IO_Agent(meta_task_id, task_id)
    agent.messages = [{"role": "system", "content":"You are an ai agent that read and write files"}]
    return agent.send_prompt(query)

def use_db_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = DB_Retrieval_Agent(meta_task_id, task_id)
    agent.messages = [{"role":"system", "content":"You are a smart assistant, you retrieve information from database"}]
    return agent.send_prompt(query)


def use_file_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = File_Retrieval_Agent(meta_task_id, task_id)
    agent.messages = [{"role":"system", "content": "You are a smart assistant and you will retrieve information from local document to answer questions or perform tasks."}]
    return agent.send_prompt(query)

def use_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = Retrieval_Agent(meta_task_id, task_id)
    agent.messages = [{"role" :"system", "content": "You are a smart research assistant. Use the search engine to look up information."}]
    return agent.send_prompt(query)

def use_web_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = Web_Retrieval_Agent(meta_task_id, task_id)
    agent.messages = [{"role":"system", "content" :"You are a smart research assistant. Use the search engine to look up information."}]
    return agent.send_prompt(query)

def main():
    response = use_exec_agent(
        "read file 3 lines of file agent.py in the current folder")
    print(response)
    response = use_exec_agent(
        "pip list to show installed python environment")
    print(response)
    response = use_exec_agent(
        "show me the python path of this virtual environment")
    print(response)

    response = use_io_agent("write aaa to 1.txt, bbb to 2.txt, ccc to 3.txt")
    print(response)
    response = use_io_agent("generate a image of a ginger cat and save it as ginger_cat.png")
    print(response)

    response = use_db_retrieval_agent("use supabase database, users table, look up the email (column name: email) for name is danqing2", 0, 0)
    print(response)

    agent = File_Retrieval_Agent(0, 0)
    response = agent.send_prompt("search information in ./files/attention.pdf and answer what is transformer?")
    print(response)
    print(agent.messages)

    response = use_retrieval_agent(
        "use supabase database, users table, look up the email (column name: email) for name is danqing2", "test", 0)
    print(response)

    response = use_web_retrieval_agent("Fetch the UK's GDP over the past 5 years", 0, 0)
    print(response)

if __name__ == "__main__":
    main()