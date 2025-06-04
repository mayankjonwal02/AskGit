from langchain.tools import Tool
from get_embeddings import get_retriever



def gitlab_search_tool(query: str) -> str:
    retriever = get_retriever()
    results = retriever.get_relevant_documents(query)
    return "\n\n".join([doc.page_content for doc in results])

tools = [
    Tool(
        name="GitLabKnowledgeBase",
        func=gitlab_search_tool,
        description="Search GitLab Handbook and Direction pages for relevant information about GitLab's practices, policies, and strategies."
    )
]
