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


def retrieve(query:str, pdf_list: List[str], persist_directory: str = 'files/chroma/', db_overwrite: bool = True) -> List[str]:
    # Load PDF
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

tools = [
    {
        "type": "function",
        "function": {
            "name": "retrieve",
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
                    "persist_directory": {
                        "type": "string",
                        "default": "files/chroma/",
                        "description": "Directory where results will be saved. Defaults to 'files/chroma/'."
                    },
                    "db_overwrite": {
                        "type": "boolean",
                        "default": True,
                        "description": "Whether to overwrite the existing database. Defaults to True."
                    }
                },
                "required": [
                    "query",
                    "pdf_list"
                ]
            }
        }
    }
]

client = OpenAI()
available_tools = {
    "retrieve": retrieve
}

def use_retrieve_agent(query):
    messages = [Message(role="system",
                        content="You are a smart assistant and you will retrieve information from local document in ./files/attention.pdf to answer questions or perform tasks.")]
    send_prompt("rag_agent", client, messages, query, tools, available_tools)
    return messages[-1].content


def main():
    response = use_retrieve_agent("what is transformer?")
    print(response)
    

if __name__ == "__main__":
    main()
