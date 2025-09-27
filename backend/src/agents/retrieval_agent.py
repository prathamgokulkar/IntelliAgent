# Will contain a function that takes a user's question, embeds it, and retrieves relevant document chunks from the database.
import os
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

DB_PATH = "vector_store"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1" )

def answer_query(question: str) -> str:
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
    return response.get("answer")