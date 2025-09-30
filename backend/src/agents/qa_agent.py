import os
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from src.core.vector_store_client import get_vector_store_client

load_dotenv()

GROQ_MODEL_NAME = "openai/gpt-oss-20b"

def answer_query(question: str) -> str:
    
    try:
        print(f"Q&A Agent: Answering question: '{question}'")
        llm = ChatGroq(model_name=GROQ_MODEL_NAME, temperature=0.3)
        
        # Get the Qdrant vector store client
        vector_store = get_vector_store_client()
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})

        template = """You are a helpful financial assistant. Answer the user's question based only on the provided context. If the answer is not in the context, state that clearly.

        CONTEXT:
        {context}
        
        QUESTION: {input}
        
        ANSWER:
        """
        prompt = ChatPromptTemplate.from_template(template)

        combine_docs_chain = create_stuff_documents_chain(llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

        response = retrieval_chain.invoke({"input": question})
        
        return response.get("answer", "Sorry, I couldn't find a relevant answer in the document.")

    except Exception as e:
        print(f"!!!!!! ERROR in Q&A Agent: {e} !!!!!!")
        raise e
