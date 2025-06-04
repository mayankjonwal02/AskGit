from langchain_google_genai import GoogleGenerativeAIEmbeddings
from workflow.doc_loaders import embed_handbook_links, find_best_matching_link, load_additional_page, load_data, split_docs
from langchain.schema import Document
from workflow.doc_loaders import cosine_similarity
from workflow.chain import build_qa_chain
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")


def find_top_n_matching_links(query, embedded_links, embed_model, n=4):
    """
    Finds the top-N handbook links most similar to the query.
    """
    if not embedded_links:
        return []
    query_vector = embed_model.embed_query(query)

    similarities = [(item["link"], cosine_similarity(query_vector, item["vector"])) for item in embedded_links]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [link for link, _ in similarities[:n]]


def run_chatbot(query):
    """
    Runs the chatbot workflow for a given query and returns the answer.
    """
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    print("Loading GitLab Direction page...")
    my_data = load_data()
    direction_docs, handbook_links = my_data[0], my_data[1]
    if not direction_docs or not handbook_links:
        raise ValueError("Failed to load direction docs or handbook links.")

    embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=gemini_api_key)
    embedded_links = embed_handbook_links(handbook_links, embed_model)
    if not embedded_links:
        raise ValueError("No embedded handbook links found.")

    # Get top 3 relevant handbook links
    top_links = find_top_n_matching_links(query, embedded_links, embed_model, n=3)
    if not top_links:
        raise ValueError("No matching handbook links found for the query.")

    print(f"Selected handbook URLs: {top_links}")

    # Scrape and split all selected handbook pages
    selected_docs = []
    for url in top_links:
        doc = load_additional_page(url)
        if doc:
            selected_docs.extend(split_docs(doc))

    # Combine all context documents
    all_docs = direction_docs + selected_docs
    if not all_docs:
        raise ValueError("No documents available for QA chain.")

    print("Running LLM QA chain...")
    qa_chain = build_qa_chain(all_docs)
    response = qa_chain.invoke(query)
    
    return response

