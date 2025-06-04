from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

gemini_api_key = os.getenv("GEMINI_API_KEY")

def build_qa_chain(all_docs):
    """
    Builds a QA chain using the provided documents.
    """
    if not all_docs:
        raise ValueError("No documents provided to build QA chain.")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        google_api_key=gemini_api_key,
        temperature=0.7,
    )
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=gemini_api_key)
    db = FAISS.from_documents(all_docs, embeddings)
    retriever = db.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
    return qa_chain