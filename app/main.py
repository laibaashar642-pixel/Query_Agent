from fastapi import FastAPI
from pydantic import BaseModel

from app.rag_chain import ask
from app.routers.users import router as users_router

app = FastAPI(title="Query Agent")

app.include_router(users_router)


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Query Agent is running"}


@app.post("/ask")
def ask_question(request: QueryRequest):
    answer = ask(request.question)
    return {"question": request.question, "answer": answer}