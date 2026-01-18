# Current Limitations & What I'd Improve Next

## Known Limitations

### 1. No Re-ranking
The system uses simple cosine similarity for retrieval. In practice, I've noticed that sometimes the 3rd or 4th most similar chunk is actually more relevant to the specific question than the top result.

**Impact**: Users occasionally get responses that miss the most relevant information.

**What I'd add**: A cross-encoder re-ranking step that considers both the query and candidate chunks together.

### 2. No Evaluation Framework
I have no systematic way to measure if the system is getting better or worse over time.

**Impact**: Hard to know if changes actually improve performance.

**What I'd add**: A test set of question-answer pairs with automated evaluation metrics (BLEU, ROUGE, or human ratings).

### 3. Single Vector Retrieval Only
The system only uses semantic embeddings. Sometimes users ask questions that would benefit from keyword matching (like searching for specific names, dates, or technical terms).

**Impact**: Might miss exact matches that don't have high semantic similarity.

**What I'd add**: Hybrid search combining vector similarity with BM25 keyword search.

### 4. No Source Attribution
While I return the source chunks, there's no way to trace back to specific pages or sections in the original document.

**Impact**: Users can't easily verify information or find more context.

**What I'd add**: Page numbers, section headers, and direct links to source locations.

### 5. Fixed Chunk Strategy
The 500-word chunking works okay for most documents, but fails for:
- Tables and structured data
- Code snippets
- Documents with very short or very long paragraphs

**Impact**: Some document types don't work well with the system.

**What I'd add**: Adaptive chunking based on document structure, or multiple chunking strategies.

### 6. No Context Persistence
Each query is independent. The system doesn't remember previous questions in a conversation.

**Impact**: Users can't ask follow-up questions or build on previous answers.

**What I'd add**: Conversation memory and context-aware retrieval.

## If I Had More Time

### Short Term (1-2 weeks)
1. **Add evaluation metrics**: Build a test set and automated scoring
2. **Improve error handling**: Better feedback when PDFs fail to process
3. **Add document metadata**: Track page numbers, sections, upload dates

### Medium Term (1-2 months)
1. **Implement re-ranking**: Add a cross-encoder for better result ordering
2. **Hybrid search**: Combine vector and keyword search
3. **Better chunking**: Respect document structure (paragraphs, sections)
4. **Conversation memory**: Allow follow-up questions

### Long Term (3+ months)
1. **Multi-modal support**: Handle images, tables, charts in PDFs
2. **Query expansion**: Automatically rephrase questions for better retrieval
3. **Active learning**: Learn from user feedback to improve results
4. **Scalability**: Move to a proper vector database for production use

## What This Project Demonstrates

Despite these limitations, this system shows:
- **RAG fundamentals**: The core retrieve-then-generate pattern
- **End-to-end implementation**: From PDF upload to user response
- **Production considerations**: Error handling, logging, API design
- **Practical trade-offs**: Choosing simplicity over completeness

It's a solid foundation that could evolve into a more sophisticated system, but it's also useful as-is for many document Q&A scenarios.