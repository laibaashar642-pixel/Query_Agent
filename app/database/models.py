from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

from app.database.connection import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    code = Column(String, nullable=True)
    isactive = Column(Boolean, default=False)
    createdat = Column(DateTime(timezone=True), server_default=func.now())
    updatedat = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())