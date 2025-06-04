from langchain.agents import AgentType, initialize_agent
from langchain_community.chat_models import ChatOpenAI  # updated import
from tools import tools  # Import the tools defined in tools.py
from get_llm import llm  # Import the LLM instance from get_llm.py
from langchain.chains import RetrievalQA
from get_embeddings import get_retriever
# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.OPENAI_FUNCTIONS,  # Use with Gemini chat models
#     verbose=True
# )
agent= RetrievalQA.from_chain_type(
    llm=llm,
    retriever=get_retriever(),
    chain_type="stuff"  # or "map_reduce" if large
)

def invoke_agent(prompt: str) -> str:
    try:
        query = "You must always use the GitLabKnowledgeBase tool before answering. "
        "Refer to it even if you know the answer. "
        f"User question: {prompt}"
        response = agent.invoke(query)

        return response.content if hasattr(response, 'content') else "There is an error with the response format."

    except Exception as e:
        print(e)
        return "An error occurred while invoking the agent."