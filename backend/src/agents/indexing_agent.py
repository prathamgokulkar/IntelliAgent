# Will contain a function that takes a PDF path, uses the services from core/ to load, split, and embed the text, and then stores it in the vector database.
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

DB_PATH = "vector_store"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1" )

def process_and_store_pdf(pdf):
    loader = PyPDFLoader(pdf)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents=documents)

    print(f"Creating vector embeddings for {len(docs)} chunks...")
    db = Chroma.from_documents(docs, embeddings, persist_directory=DB_PATH)
    print("Vector store created!!")
