from langchain_qdrant import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.models import UpdateStatus

QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION_NAME = "intelliagent-collection"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384 

# Initializes and returns a LangChain Qdrant vector store client.
def get_vector_store_client() -> Qdrant:
   
    client = QdrantClient(url=QDRANT_URL)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    vector_store = Qdrant(
        client=client, 
        collection_name=QDRANT_COLLECTION_NAME, 
        embeddings=embeddings
    )
    return vector_store

# Clears all data from the Qdrant collection by recreating it.
def clear_vector_store():
  
    print(f"--- Qdrant Client: Deleting and recreating collection '{QDRANT_COLLECTION_NAME}'... ---")
    try:
        client = QdrantClient(url=QDRANT_URL)
        result = client.recreate_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIMENSION, distance=Distance.COSINE)
        )
        if result:
             print("--- Qdrant Client: Collection cleared and recreated successfully. ---")
        else:
            print("--- Qdrant Client: Collection may not have been recreated, but clear was attempted. ---")

    except Exception as e:
        print(f"--- Qdrant Client: Info during clear (this is usually okay): {e} ---")
        try:
            client = QdrantClient(url=QDRANT_URL)
            client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        except Exception:
             pass

