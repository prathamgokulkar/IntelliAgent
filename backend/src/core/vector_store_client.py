from langchain_qdrant import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.models import UpdateStatus

# --- CONFIGURATION ---
QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION_NAME = "intelliagent-collection"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384 # Dimension of the 'all-MiniLM-L6-v2' model

def get_vector_store_client() -> Qdrant:
    """
    Initializes and returns a LangChain Qdrant vector store client.
    This is now the single point of interaction with our vector database.
    """
    client = QdrantClient(url=QDRANT_URL)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    vector_store = Qdrant(
        client=client, 
        collection_name=QDRANT_COLLECTION_NAME, 
        embeddings=embeddings
    )
    return vector_store

def clear_vector_store():
    """
    Clears all data from the Qdrant collection by recreating it.
    This is a clean, reliable API call that avoids all file lock issues.
    """
    print(f"--- Qdrant Client: Deleting and recreating collection '{QDRANT_COLLECTION_NAME}'... ---")
    try:
        client = QdrantClient(url=QDRANT_URL)
        # This command deletes all vectors and metadata and recreates the collection
        # with the correct configuration. It is the most robust way to clear data.
        result = client.recreate_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIMENSION, distance=Distance.COSINE)
        )
        if result:
             print("--- Qdrant Client: Collection cleared and recreated successfully. ---")
        else:
            print("--- Qdrant Client: Collection may not have been recreated, but clear was attempted. ---")

    except Exception as e:
        # This might happen on the very first run if the collection doesn't exist yet, which is fine.
        print(f"--- Qdrant Client: Info during clear (this is usually okay): {e} ---")
        # In case of error (e.g., collection not found), we ensure it exists for the next step.
        try:
            client = QdrantClient(url=QDRANT_URL)
            client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        except Exception:
             # If get_collection fails, it likely means the collection needs to be created, 
             # which will happen automatically when the first document is added.
             pass

