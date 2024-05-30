import re
from typing import Tuple, List
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from pypdf import PdfReader
import faiss
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)
def parse_pdf(file_path: str, filename: str) -> Tuple[List[str], str]:
    print("Parsing PDF")
    # Assuming the library used is PyPDF2
    with open(file_path, 'rb') as pdf_file:
        pdf = PdfReader(pdf_file)
        output = []
        for page in pdf.pages:
            text = page.extract_text()
            text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
            text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
            text = re.sub(r"\n\s*\n", "\n\n", text)
            output.append(text)
    return output, filename

def text_to_docs(text: List[str], filename: str) -> List[Document]:
    if isinstance(text, str):
        text = [text]
    page_docs = [Document(page_content=page) for page in text]
    for i, doc in enumerate(page_docs):
        doc.metadata["page"] = i + 1

    doc_chunks = []
    for doc in page_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            separators=["\n\n", "\n", "Scenario", "?"],
            chunk_overlap=50,
        )
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i}
            )
            doc.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc.metadata["filename"] = filename  # Add filename to metadata
            doc_chunks.append(doc)
    return doc_chunks

def docs_to_index(docs, openai_api_key):
    print("docs_to_index1")
    index = FAISS.from_documents(docs, OpenAIEmbeddings(openai_api_key=openai_api_key))
    print("docs_to_index2")
    return index



#Database creation

# Cached function to create a vectordb for the provided PDF files
def build_vectordb(folder_path, openai_api_key):
  """
  This function pre-processes PDFs in a folder and builds the vector database.

  Args:
      folder_path: Path to the folder containing PDFs.
      openai_api_key: Your OpenAI API key.
!pip install llama-index
  Returns:
      A FAISS index object representing the vector database.
  """
  
  documents = []
  for filename in os.listdir(folder_path):
      if filename.endswith(".pdf"):
          file_path = os.path.join(folder_path, filename)
          text, filename = parse_pdf(file_path, filename)
          documents = documents + text_to_docs(text, filename)
          print(file_path)
  index = docs_to_index(documents, openai_api_key)
  return index

pdf_folder_path = "Review_bassed_journalling\Docs2"  # Modify this path to your folder location

db = build_vectordb(pdf_folder_path, os.environ.get("OPENAI_API_KEY"))

db.save_local("faiss_index_ques_200_50")