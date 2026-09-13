import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.retrieve import search

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-20b",
)

prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context below.

Context:
{context}

Question: {question}

Answer:"""
)


def ask(question: str):
    docs = search(question, top_k=3)
    context = "\n".join(doc.content for doc in docs)

    chain = prompt | llm
    response = chain.invoke({"context": context, "question": question})

    return response.content


if __name__ == "__main__":
    question = "What is pgvector used for?"
    answer = ask(question)
    print("Answer:", answer)