import os
from langchain_chroma import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

from src.core import loader, splitter

DB_PATH = "vector_store"
MODEL_NAME = "all-MiniLM-L6-v2"

def get_embedding_function():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1" )

def process_and_store_pdf(pdf_path: str):
    
    try:
        print(f"Indexing Agent: Managing workflow for '{pdf_path}'")
        
       
        extracted_text = loader.load_pdf_text(pdf_path)
        
        docs = splitter.split_text_into_chunks(extracted_text)
        
        print("Performing core task of embedding and storing...")
        embeddings = get_embedding_function()
        Chroma.from_documents(docs, embeddings, persist_directory=DB_PATH)
        
        print("--- Indexing Agent: Workflow completed successfully! ---")
        return True

    except Exception as e:
        print(f"!!!!!! ERROR in Indexing Agent workflow: {e} !!!!!!")
        raise e

