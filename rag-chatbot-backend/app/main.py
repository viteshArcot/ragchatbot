from fastapi import FastAPI
from .routes import router
from .database import create_tables

app = FastAPI(
    title="RAG Chatbot Backend",
    description="A FastAPI backend for Retrieval-Augmented Generation chatbot",
    version="1.0.0"
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "RAG Chatbot Backend is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}