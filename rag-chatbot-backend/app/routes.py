from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
from .database import get_db, QueryLog, DocumentLog
from .embeddings import document_retriever
from .llm import llm_client
from .ingestion import pdf_processor
import numpy as np

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    similarity_score: float
    sources: List[str]

@router.post("/query", response_model=QueryResponse)
async def ask_question(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Main RAG endpoint: retrieve relevant chunks, then generate response.
    
    This implements the core RAG pattern:
    1. Take user's question
    2. Find relevant document chunks (retrieval)
    3. Send question + chunks to LLM (augmented generation)
    4. Return response with sources
    
    I retrieve 3 chunks as a balance between context and prompt length.
    More chunks = more context but longer prompts and higher costs.
    """
    try:
        # Step 1: Find the most relevant document chunks for this question
        # This is the "retrieval" part of RAG
        retrieved_chunks, similarity_scores = document_retriever.find_relevant_chunks(
            request.question, num_results=3
        )
        
        # Step 2: Generate response using the LLM with retrieved context
        # This is the "augmented generation" part of RAG
        llm_response = await llm_client.generate_answer(request.question, retrieved_chunks)
        
        # Step 3: Calculate average similarity for quality tracking
        # Lower scores might indicate the question is outside our knowledge base
        avg_similarity = np.mean(similarity_scores) if similarity_scores else 0.0
        
        # Step 4: Log this interaction for analytics and debugging
        query_log = QueryLog(
            query_text=request.question,
            response_text=llm_response,
            cosine_similarity=float(avg_similarity)
        )
        db.add(query_log)
        db.commit()
        
        return QueryResponse(
            answer=llm_response,
            similarity_score=float(avg_similarity),
            sources=retrieved_chunks
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history(db: Session = Depends(get_db)):
    """Get last 10 queries and responses"""
    logs = db.query(QueryLog).order_by(QueryLog.timestamp.desc()).limit(10).all()
    return [
        {
            "id": log.id,
            "query": log.query_text,
            "response": log.response_text,
            "timestamp": log.timestamp,
            "similarity": log.cosine_similarity
        }
        for log in logs
    ]

@router.get("/metrics")
async def get_system_metrics(db: Session = Depends(get_db)):
    """
    Get system performance metrics for monitoring and debugging.
    
    Similarity scores help understand system performance:
    - High avg similarity (>0.7): Questions match documents well
    - Low avg similarity (<0.3): Questions outside knowledge base
    - High std deviation: Inconsistent document relevance
    
    These metrics help identify when to add more documents or
    improve the chunking strategy.
    """
    query_logs = db.query(QueryLog).all()
    
    if not query_logs:
        return {"message": "No queries logged yet - upload some documents and ask questions!"}
    
    # Extract similarity scores, filtering out None values
    similarity_scores = [
        log.cosine_similarity for log in query_logs 
        if log.cosine_similarity is not None
    ]
    
    if not similarity_scores:
        return {"message": "No similarity scores available yet"}
    
    # Calculate statistics that help understand system performance
    return {
        "total_queries": len(query_logs),
        "avg_similarity": float(np.mean(similarity_scores)),
        "min_similarity": float(np.min(similarity_scores)),
        "max_similarity": float(np.max(similarity_scores)),
        "similarity_std": float(np.std(similarity_scores)),
        # Add interpretation hints
        "performance_hint": (
            "Good performance" if np.mean(similarity_scores) > 0.5 
            else "Consider adding more relevant documents"
        )
    }

@router.post("/ingest")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload and process a PDF document into the RAG system.
    
    This endpoint handles the document ingestion pipeline:
    1. Validate the uploaded file
    2. Extract text from PDF
    3. Split into chunks
    4. Generate embeddings
    5. Add to searchable index
    6. Log metadata to database
    
    After this completes, users can ask questions about the document content.
    """
    # Basic validation - only accept PDF files
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are supported. Please upload a .pdf file."
        )
    
    try:
        # Read the uploaded file into memory
        pdf_bytes = await file.read()
        
        # Run the complete PDF processing pipeline
        # This extracts text, chunks it, creates embeddings, and adds to index
        processing_result = pdf_processor.process_uploaded_pdf(pdf_bytes, file.filename)
        
        # Store metadata about this document for tracking
        document_record = DocumentLog(
            doc_id=processing_result['doc_id'],
            filename=processing_result['filename'],
            num_chunks=processing_result['num_chunks'],
            total_text_length=processing_result.get('total_text_length')
        )
        db.add(document_record)
        db.commit()
        
        # Return success response with processing details
        return {
            "message": "PDF processed and added to knowledge base successfully",
            "filename": processing_result['filename'],
            "doc_id": processing_result['doc_id'],
            "num_chunks": processing_result['num_chunks'],
            "total_text_length": processing_result.get('total_text_length'),
            "avg_chunk_length": processing_result.get('avg_chunk_length')
        }
        
    except Exception as e:
        # Provide helpful error messages for common failure cases
        error_message = str(e)
        if "No text could be extracted" in error_message:
            error_message += " This might be a scanned PDF that requires OCR."
        
        raise HTTPException(status_code=500, detail=f"Document processing failed: {error_message}")

@router.get("/documents")
async def list_uploaded_documents(db: Session = Depends(get_db)):
    """
    Get a list of all documents that have been uploaded and processed.
    
    This helps users see what's in their knowledge base and track
    which documents might need to be re-uploaded or updated.
    """
    document_records = db.query(DocumentLog).order_by(DocumentLog.timestamp.desc()).all()
    
    return [
        {
            "doc_id": doc.doc_id,
            "filename": doc.filename,
            "num_chunks": doc.num_chunks,
            "timestamp": doc.timestamp,
            "total_text_length": doc.total_text_length,
            # Add helpful derived information
            "avg_chunk_size": (
                doc.total_text_length // doc.num_chunks 
                if doc.num_chunks > 0 else 0
            )
        }
        for doc in document_records
    ]