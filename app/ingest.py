#This file helps usto take data then embeeded it and stores in database
from app.database.connection import SessionLocal
from app.database.models import Document
from app.embeddings import get_embeddings
sample_texts=[
     "LangChain is a framework for building LLM applications.",
    "pgvector allows storing vector embeddings in PostgreSQL.",
    "FastAPI is a modern Python web framework for building APIs.",
]
#Helps usto make datbase session
session=SessionLocal()
for text in sample_texts:
    embeddings=get_embeddings(text)
    doc=Document(content=text,embedding=embeddings)
    session.add(doc)

session.commit()
session.close()
print("Documents inserted Successfully!")