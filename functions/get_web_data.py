import os
import pickle
from langchain_community.document_loaders import WebBaseLoader  # updated import
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


CACHE_FILE = "cached_gitlab_docs.pkl"
URLS = [
    "https://handbook.gitlab.com/",
    "https://about.gitlab.com/direction/"
]

def get_all_links(url: str) -> list:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    links = set()

    for a_tag in soup.find_all("a", href=True):
        full_url = urljoin(url, a_tag["href"])  # resolves relative URLs
        links.add(full_url)

    return list(links)
def fetch_and_split():
    print("Fetching fresh content from GitLab...")
    all_links = [url for url in URLS]
    for url in URLS:
        all_links.extend(get_all_links(url))
    
    loader = WebBaseLoader(all_links)
    raw_docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = splitter.split_documents(raw_docs)

    with open(CACHE_FILE, "wb") as f:
        pickle.dump(docs, f)

    return docs

def load_cached_docs():
    if os.path.exists(CACHE_FILE):
        print("Loading cached documents...")
        with open(CACHE_FILE, "rb") as f:
            return pickle.load(f)
    else:
        return fetch_and_split()

