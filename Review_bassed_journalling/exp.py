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

'''import pkg_resources

def get_installed_version(package_name):
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return None

def main():
    try:
        with open('requirements.txt', 'r') as file:
            packages = file.readlines()
    except FileNotFoundError:
        print("The requirements.txt file was not found.")
        return

    for package in packages:
        package_name = package.strip().split('==')[0]  # Remove any version specifier
        version = get_installed_version(package_name)
        if version:
            print(f"{package_name}: {version}")
        else:
            print(f"{package_name}: Not installed")

if __name__ == "__main__":
    main()
'''