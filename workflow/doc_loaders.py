import json
import os
import pickle
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import numpy as np
import requests
from langchain.schema import Document


def split_docs(documents):
    """Splits documents into chunks for processing."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_documents(documents)

def load_direction_page():
    """Loads and splits the GitLab direction page."""
    loader = WebBaseLoader("https://about.gitlab.com/direction/")
    docs = loader.load()
    return split_docs(docs)

def extract_handbook_links(base_url="https://handbook.gitlab.com/"):
    """Extracts unique, valid handbook links from the base URL."""
    try:
        res = requests.get(base_url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"Error fetching handbook links: {e}")
        return []
    soup = BeautifulSoup(res.text, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith("/") or href.startswith(base_url):
            full_link = href if href.startswith("http") else f"{base_url.rstrip('/')}/{href.lstrip('/')}"
            if full_link.startswith("http"):
                links.add(full_link)
    return list(links)

def cache_data():
    # Cache data from load_direction_page
    data1 = load_direction_page()
    with open("data1.pkl", "wb") as f:
        pickle.dump(data1, f)
    # Cache data from extract_handbook_links
    data2 = extract_handbook_links()
    with open("data2.pkl", "wb") as f:
        pickle.dump(data2, f)
    print("Data cached to data1.pkl and data2.pkl")
    
def load_data():
    """
    Loads direction page docs and handbook links from cache if available.
    Returns:
        data1: list of split Document objects from direction page
        data2: list of handbook links (strings)
    """
    data1_path = "data1.pkl"
    data2_path = "data2.pkl"

    # Check if both cache files exist
    if os.path.exists(data1_path) and os.path.exists(data2_path):
        with open(data1_path, "rb") as f1, open(data2_path, "rb") as f2:
            data1 = pickle.load(f1)
            data2 = pickle.load(f2)
        return data1, data2

    # If not cached, fetch and cache
    data1 = load_direction_page()
    with open(data1_path, "wb") as f1:
        pickle.dump(data1, f1)

    data2 = extract_handbook_links()
    with open(data2_path, "wb") as f2:
        pickle.dump(data2, f2)

    return data1, data2

def embed_handbook_links(links, embed_model, cache_path="link_embeddings.pkl"):
    """
    Embeds handbook links using the provided embedding model.
    """
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            return pickle.load(f)
    docs = [Document(page_content=link, metadata={"source": link}) for link in links]
    vectors = embed_model.embed_documents([d.page_content for d in docs])
    embedded = [{"link": doc.page_content, "vector": vec} for doc, vec in zip(docs, vectors)]
    with open(cache_path, "wb") as f:
        pickle.dump(embedded, f)
    return embedded

def cosine_similarity(a, b):
    """Computes cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_best_matching_link(query, embedded_links, embed_model):
    """
    Finds the handbook link most similar to the query.
    """
    if not embedded_links:
        return None
    query_vector = embed_model.embed_query(query)
    similarities = [(item["link"], cosine_similarity(query_vector, item["vector"])) for item in embedded_links]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[0][0] if similarities else None

def load_additional_page(url):
    """Loads a web page and returns its documents."""
    try:
        loader = WebBaseLoader(url)
        return loader.load()
    except Exception as e:
        print(f"Error loading additional page: {e}")
        return []