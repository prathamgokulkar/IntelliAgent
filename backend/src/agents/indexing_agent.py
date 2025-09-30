from src.core import loader, splitter
# THE CHANGE: Import our new centralized Qdrant client function
from src.core.vector_store_client import get_vector_store_client

def process_and_store_pdf(pdf_path: str):
    """
    Manages the PDF indexing workflow by calling specialists and using the Qdrant client.
    """
    try:
        print(f"--- Indexing Agent: Managing workflow for '{pdf_path}' ---")
        
        # Steps 1 & 2: Delegate to specialists (no change here)
        extracted_text = loader.load_pdf_text(pdf_path)
        docs = splitter.split_text_into_chunks(extracted_text)
        
        # Step 3: Get the Qdrant client and add documents
        print("--- Indexing Agent: Getting Qdrant client and adding documents... ---")
        vector_store = get_vector_store_client()
        
        # LangChain's Qdrant client handles the embedding process automatically
        vector_store.add_documents(docs) 
        
        print("--- Indexing Agent: Workflow completed successfully! Documents added to Qdrant. ---")
        return True

    except Exception as e:
        print(f"!!!!!! ERROR in Indexing Agent workflow: {e} !!!!!!")
        raise e

