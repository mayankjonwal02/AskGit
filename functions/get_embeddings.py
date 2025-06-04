from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS  # updated import
from get_web_data import load_cached_docs

def get_retriever():
    """
    Get a retriever from cached documents.
    If the cache is not available, it will fetch and split the documents.
    """
    documents = load_cached_docs()

    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(documents, embedding)
    retriever = vectorstore.as_retriever()
    return retriever
