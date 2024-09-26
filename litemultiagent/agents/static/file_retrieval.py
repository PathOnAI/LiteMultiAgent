from litemultiagent.agents.core.DefaultAgent import DefaultAgent
from typing import List, Optional
import os
import shutil


from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


def retrieve_file(query:str, pdf_list: List[str]) -> List[str]:
    # Load PDF
    persist_directory = 'files/chroma/'
    db_overwrite = True
    try:
        loaders = [PyPDFLoader(pdf) for pdf in pdf_list]
        docs = []
        for loader in loaders:
            docs.extend(loader.load())
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n","\n"],
            chunk_size = 200, chunk_overlap = 150
            )
        splits = text_splitter.split_documents(docs)
        embedding = OpenAIEmbeddings()
        if db_overwrite and os.path.exists("./" + persist_directory):
            shutil.rmtree("./" + persist_directory)
        vectordb = Chroma.from_documents(
            documents=splits,
            embedding=embedding,
            persist_directory=persist_directory
            )
        search_results = vectordb.similarity_search(query,k=3)
        return [r.page_content for r in search_results]
    except Exception as e:
        return f"An error occurred while retrieving information from file: {str(e)}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "retrieve_file",
            "description": "Processes a list of PDFs based on a query and saves the results in the specified directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query string to use for processing."
                    },
                    "pdf_list": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of paths to PDF files."
                    },
                },
                "required": [
                    "query",
                    "pdf_list"
                ]
            }
        }
    }
]

available_tools = {
    "retrieve_file": retrieve_file
}

class FileRetrievalAgent(DefaultAgent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        super().__init__("use_file_retrieval_agent", tools, available_tools, meta_task_id, task_id)

if __name__ == "__main__":
    def use_file_retrieval_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
        agent = FileRetrievalAgent(meta_task_id, task_id)
        agent.messages = [{"role":"system", "content": "You are a smart assistant and you will retrieve information from local document to answer questions or perform tasks."}]
        return agent.send_prompt(query)
    
    def main():
        agent = FileRetrievalAgent(0, 0)
        response = agent.send_prompt("search information in ./files/attention.pdf and answer what is transformer?")
        print(response)
        print(agent.messages)

    main()
