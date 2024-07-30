from agents.exec import Exec_Agent

from typing import Optional

def use_exec_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = Exec_Agent(meta_task_id, task_id)
    agent.messages = [{"role": "system", "content":"You will exec some scripts. Either by shell or run python script"}]
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

if __name__ == "__main__":
    main()