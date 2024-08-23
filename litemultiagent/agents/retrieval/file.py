from litemultiagent.agents.base import Agent



from typing import List, Optional
import os
import shutil

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from litemultiagent.utils.tools import Tools



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

available_tools = {
    "retrieve_file": retrieve_file
}


class File_Retrieval_Agent(Agent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        super().__init__("file_retrieval_agent", Tools._file, available_tools, meta_task_id, task_id)


