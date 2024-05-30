import re
from typing import Tuple, List

from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
import faiss
import streamlit as st
from openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)
embeddings = OpenAIEmbeddings()
question="Why I no longer feel motivated to work"
db = FAISS.load_local("faiss_index_ques_200_50", embeddings,allow_dangerous_deserialization =True)
print(db.similarity_search(question, k=4))