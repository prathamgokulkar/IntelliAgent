# Will contain a function that takes a user's question, embeds it, and retrieves relevant document chunks from the database.
import os
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

from src.agents import validation_agent

from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

DB_PATH = "vector_store"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1" )

def answer_query(question: str) -> str:
    try:
        db =Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        retriever = db.as_retriever()

        prompt_template = """You are a helpful financial assistant. Answer the user's question based only on the following context:
        <context>
        {context}
        </context>
        Question: {input}
        """

        prompt = ChatPromptTemplate.from_template(prompt_template)

        llm = ChatGroq(model= "openai/gpt-oss-20b", api_key=groq_api_key)

        combine_doc_chain = create_stuff_documents_chain(llm, prompt=prompt)
        retriever_chain = create_retrieval_chain(retriever, combine_doc_chain)

        response = retriever_chain.invoke({"input": question})
        source_documents = response.get("context", [])

        initial_answer = response.get("answer", "Sorry, I couldn't find an answer.")

        if not initial_answer or not source_documents:
            return "Could not generate an answer or find relevant context."

        validation_result = validation_agent.validate_answer_with_llm(initial_answer, source_documents)

        # Construct the final response
        if validation_result["is_supported"]:
            final_answer = initial_answer + "\n\n*Verified from document.*"
        else:
            final_answer = initial_answer + f"\n\n*Caution: Could not fully verify this answer from the document. Reason: {validation_result['reasoning']}*"
            
            return final_answer

    except Exception as e:
        print(f"!!!!!! ERROR in Q&A Agent: {e} !!!!!!")
        raise e