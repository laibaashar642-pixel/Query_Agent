from app.database.connection import SessionLocal
from app.database.models import Document
from app.embeddings import get_embeddings
def search(query:str,top_k:int=3):
    session=SessionLocal()
    query_embeddings=get_embeddings(query)
    results=(
        session.query(Document)
        .order_by(Document.embedding.cosine_distance(query_embeddings))
         .limit(top_k)
         .all()
         )
    session.close()
    return results
if __name__=="__main__":
    query="What is pgvector used for?"
    matches=search(query)
    for doc in matches:
        print(f"-{doc.content}")