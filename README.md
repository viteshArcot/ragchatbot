RAG-Powered AI Chatbot 🤖📚

A full-stack Retrieval-Augmented Generation (RAG) chatbot that ingests documents (PDFs), stores them in a vector database, and provides context-aware answers with source references — all in a modern chat UI.

✨ Overview

The RAG Chatbot is a complete application demonstrating document-based question answering. It supports PDF ingestion, semantic retrieval, and contextual LLM responses.

Built with a FastAPI backend and a React frontend, it’s production-ready with a polished glassmorphism UI, query history tracking, and system metrics dashboards.

🎯 Key Features

PDF Ingestion → Drag-and-drop upload with automatic text parsing.

Smart Chunking → Overlap-based splitting for high-quality embeddings.

Semantic Search → FAISS vector search retrieves most relevant context.

LLM-Powered Chat → OpenRouter (GPT-3.5) generates contextual answers.

Query Logging → Store all chats with timestamps and metrics in SQLite.

Modern UI → Glassmorphism chat interface with history + analytics modal.

Responsive Design → Mobile-first experience with smooth animations.

🛠️ Tech Stack

Backend: FastAPI, FAISS, SentenceTransformers, SQLite, PyPDF2, pdfplumber, OpenRouter API
Frontend: React, Axios, TailwindCSS (glassmorphism styling)
Architecture: Modular components, REST API with 6 endpoints

📊 System Architecture

Ingestion → PDFs parsed → chunked → embedded into vector DB.

Retrieval → Query embedded → similarity search with FAISS.

Generation → LLM (GPT-3.5) uses retrieved chunks for context.

Storage → Logs chats, metrics, and documents in SQLite.

🚀 API Endpoints

POST /api/v1/ingest → Upload PDFs

POST /api/v1/query → Ask a question

GET /api/v1/history → Retrieve chat history

GET /api/v1/documents → List uploaded PDFs

GET /api/v1/metrics → System analytics

GET /health → Health check

📁 Project Structure
rag-chatbot/
├── backend/
│   ├── main.py         # FastAPI entry point
│   ├── routes.py       # Endpoints
│   ├── embeddings.py   # Vector search logic
│   ├── ingestion.py    # PDF processing
│   ├── llm.py          # OpenRouter client
│   └── database.py     # SQLite setup
├── frontend/
│   ├── src/components/ # ChatBox, FileUpload, MetricsPanel
│   ├── src/api.js      # Axios client
│   ├── App.js          # Main entry
│   └── App.css         # Glassmorphism styling

🖼️ Screenshots

(Add later: PDF upload screen, Chat UI, Metrics dashboard)

🎨 Why This Project Matters

This chatbot proves applied AI engineering skills:

NLP + Information Retrieval → semantic embeddings, FAISS search.

LLM integration → grounding responses in context, avoiding hallucination.

Full-stack delivery → API design + polished frontend UI.

Production readiness → modularity, error handling, responsive design.

It shows ability to build real-world AI applications beyond toy demos.

🧑‍💻 Setup Instructions
Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Frontend
cd frontend
npm install
npm start


Access app at: http://localhost:3000

📌 Status

✅ Fully implemented RAG pipeline
✅ End-to-end PDF → Retrieval → AI Answer flow
✅ Polished UI with analytics
✅ Perfect portfolio project for AI Engineer / Full-Stack Developer roles
