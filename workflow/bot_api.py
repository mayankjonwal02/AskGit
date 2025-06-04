from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bot import run_chatbot

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/bot")
async def bot_endpoint(request: QueryRequest):
    try:
        response = run_chatbot(request.query)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}
