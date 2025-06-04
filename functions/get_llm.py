import os 
from langchain_google_genai import ChatGoogleGenerativeAI

gemini_api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    google_api_key=gemini_api_key,
    temperature=0.7,
    # top_p=1,
    # top_k=40,
    # max_output_tokens=256,
    # min_output_tokens=1,
    # stop_sequences=["\n\nHuman:"],
    # verbose=True,
)