import logging
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from typing import List
import os
import shutil
import json
_ = load_dotenv(find_dotenv()) 

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from utils import *


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

from config import agent_to_model
agent_name = "file_retrieve_agent"
model_name = agent_to_model[agent_name]["model_name"]
# if 'gpt' in model_name:
#     client = OpenAI()
# else:
#     client = OpenAI(
#         base_url="https://openrouter.ai/api/v1",
#         api_key=os.getenv("OPENROUTER_API_KEY"),
#     )
available_tools = {
    "retrieve_file": retrieve_file
}

def use_file_retrieve_agent(query):
    messages = [Message(role="system",
                        content="You are a smart assistant and you will retrieve information from local document to answer questions or perform tasks.")]
    send_prompt("file_retrieve_agent", messages, query, tools, available_tools)
    return messages[-1].content


def main():
    response = use_file_retrieve_agent("search information in ./files/attention.pdf and answer what is transformer?")
    print(response)
    

if __name__ == "__main__":
    main()
