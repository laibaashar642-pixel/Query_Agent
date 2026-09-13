import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker,declarative_base
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
Base=declarative_base()
SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
def test_connection():
    with engine.connect() as connection:
        result=connection.execute(text("SELECT version();"))
        print("Database connected successfully!")
        print(result.fetchone())
        