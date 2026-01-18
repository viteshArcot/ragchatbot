# RAG Architecture Overview

## What This System Does

This is a straightforward RAG (Retrieval-Augmented Generation) chatbot that lets users upload PDFs and ask questions about them. The core idea is simple: instead of relying on the LLM's training data alone, we first retrieve relevant document chunks and use them as context.

## The Pipeline (Step by Step)

### 1. Document Ingestion
When a user uploads a PDF:
- Extract text using PyPDF2 (with pdfplumber as fallback)
- Split the text into overlapping chunks of ~500 words
- Generate embeddings for each chunk using sentence-transformers
- Store everything in a FAISS vector index

### 2. Query Processing
When a user asks a question:
- Convert the question into an embedding (same model as documents)
- Search the FAISS index for the 5 most similar chunks
- Pass the question + retrieved chunks to the LLM
- Return the generated response along with source chunks

### 3. Why This Design Works

**Retrieval First**: We search for relevant context before generating. This grounds the response in actual document content rather than just the LLM's training data.

**Semantic Search**: Embeddings capture meaning better than keyword matching. A question about "machine learning algorithms" will match chunks about "neural networks" or "classification methods."

**Chunk Overlap**: I use 50-word overlaps between chunks to avoid cutting sentences in half and losing context at boundaries.

## Where Things Can Break

**Poor Text Extraction**: PDFs with complex layouts, images, or tables often produce garbled text. The chunking strategy assumes clean, readable text.

**Embedding Limitations**: The sentence-transformer model was trained on general text. Domain-specific jargon or very technical content might not embed well.

**Context Window**: I only retrieve the top 5 chunks. If relevant information is spread across many sections, the LLM might miss important context.

**No Re-ranking**: The initial similarity search is the final ranking. More sophisticated systems would re-rank results based on the specific query.

## Why I Chose This Approach

I wanted to build something that demonstrates RAG fundamentals without over-engineering. This system:
- Uses proven, stable libraries (FAISS, sentence-transformers)
- Has minimal dependencies and complexity
- Can be understood and modified easily
- Works well for most document Q&A use cases

The trade-off is that it's not optimized for edge cases or specialized domains, but it's a solid foundation that could be extended.