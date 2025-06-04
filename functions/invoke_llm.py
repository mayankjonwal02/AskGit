from get_llm import llm

def invoke_llm(prompt: str | list) -> str:
    
    try:
        response = llm.invoke(prompt)

        return response.content if hasattr(response, 'content') else "There is an error with the response format."

    except Exception as e:
        print(e)
        return "An error occurred while invoking the LLM."