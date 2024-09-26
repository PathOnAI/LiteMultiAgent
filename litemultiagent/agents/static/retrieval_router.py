from typing import Optional

from litemultiagent.agents.core.DefaultAgent import DefaultAgent

from litemultiagent.agents.static.db_retrieval import DatabaseRetrievalAgent
from litemultiagent.agents.static.file_retrieval import FileRetrievalAgent
from litemultiagent.agents.static.web_retrieval import WebRetrievalAgent

def use_web_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = WebRetrievalAgent(meta_task_id, task_id)
    agent.messages = [{"role":"system", "content" :"You are a smart research assistant. Use the search engine to look up information."}]
    return agent.send_prompt(query)

def use_file_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = FileRetrievalAgent(meta_task_id, task_id)
    agent.messages = [{"role":"system", "content": "You are a smart assistant and you will retrieve information from local document to answer questions or perform tasks."}]
    return agent.send_prompt(query)

def use_db_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
    agent = DatabaseRetrievalAgent(meta_task_id, task_id)
    agent.messages = [{"role":"system", "content":"You are a smart assistant, you retrieve information from database"}]
    return agent.send_prompt(query)

tools = [
    {
        "type": "function",
        "function": {
            "name": "use_web_retrieval_agent",
            "description": "Perform a search using API and return the searched results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The task description describing what to read or write."
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    },
    {
      "type": "function",
      "function": {
        "name": "use_db_retrieval_agent",
        "description": "Use a database retrieval agent to fetch information based on a given query.",
        "parameters": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "The query to be processed by the database retrieval agent."
            }
          },
          "required": [
            "query"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "use_file_retrieval_agent",
        "description": "Retrieve information from local documents to answer questions or perform tasks.",
        "parameters": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "The task description specifying the local file and the question to be answered. specify this in natural language"
            }
          },
          "required": [
            "query"
          ]
        }
      }
    }
]

class RetrievalRouterAgent(DefaultAgent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        # Create a wrapper for use_db_retrieval_agent that includes meta_task_id and task_id
        def wrapped_use_db_retrieval_agent(query: str) -> str:
            return use_db_retrieval_agent(query, meta_task_id=meta_task_id, task_id=task_id)

        def wrapped_use_web_retrieval_agent(query: str) -> str:
            return use_web_retrieval_agent(query, meta_task_id=meta_task_id, task_id=task_id)

        def wrapped_use_file_retrieval_agent(query: str) -> str:
            return use_file_retrieval_agent(query, meta_task_id=meta_task_id, task_id=task_id)

        available_tools = {
            "use_db_retrieval_agent": wrapped_use_db_retrieval_agent,
            "use_web_retrieval_agent": wrapped_use_web_retrieval_agent,
            "use_file_retrieval_agent": wrapped_use_file_retrieval_agent,
        }

        super().__init__("use_retrieval_router_agent", tools, available_tools, meta_task_id, task_id)


if __name__ == "__main__":
    def use_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
        agent = RetrievalRouterAgent(meta_task_id, task_id)
        agent.messages = [{"role" :"system", "content": "You are a smart research assistant. Use the search engine to look up information."}]
        return agent.send_prompt(query)

    def main():
        response = use_retrieval_agent(
            "use supabase database, users table, look up the email (column name: email) for name is danqing2", "test", 0)
        print(response)
        response = use_web_retrieval_agent("Fetch the UK's GDP over the past 5 years", 0, 0)
        print(response)
        
    main()