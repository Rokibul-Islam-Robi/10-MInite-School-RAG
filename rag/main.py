# REST API using Gemini for LLM and embeddings
from fastapi import FastAPI, Request
from pydantic import BaseModel
from .retriever import retrieve_relevant_chunks
from .generator import generate_answer
from .memory import ShortTermMemory

app = FastAPI()
memory = ShortTermMemory(max_length=10)

class QueryRequest(BaseModel):
    user: str
    query: str

@app.post("/ask")
def ask(request: QueryRequest):
    memory.add(request.user, request.query)
    retrieved = retrieve_relevant_chunks(request.query, top_k=4)
    answer = generate_answer(request.query, retrieved)
    return {
        "answer": answer,
        "retrieved_chunks": [c[1] for c in retrieved],
        "chat_history": memory.get_history()
    }

# Add evaluation endpoint as needed