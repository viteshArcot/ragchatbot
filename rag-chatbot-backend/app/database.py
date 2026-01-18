from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chatbot.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class QueryLog(Base):
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(String, nullable=False)
    response_text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    cosine_similarity = Column(Float, nullable=True)

class DocumentLog(Base):
    __tablename__ = "document_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(String, nullable=False, unique=True)
    filename = Column(String, nullable=False)
    num_chunks = Column(Integer, nullable=False)
    total_text_length = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()