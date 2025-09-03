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

<img width="1361" height="691" alt="rag1" src="https://github.com/user-attachments/assets/6e381ef0-25bc-4ff2-8002-a3c01caa4ea2" />
<img width="1128" height="416" alt="rag2" src="https://github.com/user-attachments/assets/c9db2d08-d85e-48e8-8f68-841f849d8436" />
<img width="1362" height="686" alt="rag3" src="https://github.com/user-attachments/assets/b5d28191-b30e-4b8b-a298-d9191693cf57" />
<img width="1364" height="687" alt="rag4" src="https://github.com/user-attachments/assets/076fdceb-1c90-4930-b39a-14a3e79e58b4" />
<img width="1364" height="687" alt="rag5" src="https://github.com/user-attachments/assets/86969412-2d68-42c0-9709-81761ecb6429" />





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
