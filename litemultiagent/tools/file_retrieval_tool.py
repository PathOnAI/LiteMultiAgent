import logging
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from typing import List, Optional
import os
import shutil
import json
_ = load_dotenv(find_dotenv())

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from litemultiagent.tools.registry import ToolRegistry, Tool

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


def register_file_retrieval_tools():
    ToolRegistry.register(Tool(
        "retrieve_file",
        retrieve_file,
        "Processes a list of PDFs based on a query and saves the results in the specified directory.",
        {
            "query": {
                "type": "string",
                "description": "The query string to use for processing.",
                "required": True
            },
            "pdf_list": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of paths to PDF files.",
                "required": True
            },
        }
    ))