# RAG Chatbot Backend

A FastAPI backend for a Retrieval-Augmented Generation (RAG) chatbot using OpenRouter API for inference.

## Features

- **RAG Pipeline**: Uses sentence-transformers for embeddings and FAISS for vector search
- **OpenRouter Integration**: Leverages free-tier models for response generation
- **SQLite Logging**: Tracks queries, responses, and similarity metrics
- **REST API**: Clean endpoints for querying, history, and metrics

## Setup

1. **Install Dependencies**
```bash
cd rag-chatbot-backend
pip install -r requirements.txt
```

2. **Configure Environment**
Edit `.env` file:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
DATABASE_URL=sqlite:///./chatbot.db
```

Get your OpenRouter API key from: https://openrouter.ai/

3. **Run the Server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /api/v1/query
Submit a question to the RAG chatbot.

**Request:**
```json
{
  "question": "What is FastAPI?"
}
```

**Response:**
```json
{
  "answer": "FastAPI is a modern web framework...",
  "similarity_score": 0.85,
  "sources": ["FastAPI is a modern web framework..."]
}
```

### POST /api/v1/ingest
Ingest PDF files into the vector database.

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/ingest \
     -F "file=@sample.pdf"
```

**Response:**
```json
{
  "message": "PDF ingested successfully",
  "filename": "sample.pdf",
  "doc_id": "uuid-string",
  "num_chunks": 25,
  "total_text_length": 12500
}
```

### GET /api/v1/history
Get the last 10 queries and responses.

### GET /api/v1/documents
Get list of all ingested documents.

### GET /api/v1/metrics
Get cosine similarity and clustering metrics.

## Project Structure

```
rag-chatbot-backend/
├── app/
│   ├── main.py         # FastAPI entry point
│   ├── routes.py       # API routes
│   ├── embeddings.py   # sentence-transformers + FAISS logic
│   ├── llm.py          # OpenRouter API client wrapper
│   ├── database.py     # SQLite + SQLAlchemy setup
├── requirements.txt
├── README.md
└── .env
```

## OpenRouter Configuration

The backend uses OpenRouter's free-tier models. To switch models, modify the `model` parameter in `app/llm.py`:

```python
self.model = "openai/gpt-3.5-turbo"  # Current free tier model
```

Available free models: https://openrouter.ai/docs#models

## Development

- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Database is automatically created on first run