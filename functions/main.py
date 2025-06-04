from invoke_llm import invoke_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from agent import invoke_agent

response = invoke_llm("What is GitLab's approach to DevOps?")
print(response)