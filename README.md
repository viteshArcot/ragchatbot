<div align="center">

# 🤖 RAG Chatbot: Document Q&A System

*A practical implementation of Retrieval-Augmented Generation (RAG)*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.0-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Upload PDFs → Ask Questions → Get Answers with Sources**

*Built to demonstrate core RAG concepts with clean, understandable code*

</div>

---\n\n## 🎯 What I Built & Why

This started as a way to understand how RAG (Retrieval-Augmented Generation) actually works beyond the hype. Instead of using frameworks like LangChain, I built it from scratch to really get the fundamentals.

The core problem: LLMs are great at general knowledge but can't answer questions about your specific documents. This system lets you upload PDFs and ask questions about their content, with the AI grounding its responses in your actual documents rather than just making things up.

It's not perfect (more on that below), but it demonstrates the key concepts and trade-offs involved in building document Q&A systems.\n\n## ⚙️ How RAG Works in This Project

### The Three-Stage Pipeline

**Stage 1: Retrieval** 🔍
- Convert user question to 384-dimensional embedding
- Search FAISS index for semantically similar document chunks
- Return top 3 chunks with similarity scores
- **Key insight**: This is pure similarity search - no understanding of whether chunks actually answer the question

**Stage 2: Context Assembly** 📋
- Format retrieved chunks into structured prompt
- Add clear instructions for LLM behavior
- Include fallback handling for insufficient context
- **Critical decision**: Order matters (most relevant first due to primacy bias)

**Stage 3: Augmented Generation** 🤖
- LLM generates response using both training knowledge and provided context
- Temperature 0.7 balances creativity with staying grounded
- **Failure mode**: LLM can still hallucinate even with good context\n\n### Why Embeddings Over Keyword Search?

**Semantic Understanding**: Embeddings capture meaning, not just words
- "car maintenance" matches "automotive repair" semantically
- Handles synonyms, paraphrasing, and context naturally
- Same word in different contexts embeds differently

**Trade-off**: Miss exact matches (model numbers, dates) that keyword search would catch

### Why FAISS for Vector Search?

**Scalability**: Optimized C++ implementation for similarity search
- Current: O(n) exact search with IndexFlatIP
- Future: Can upgrade to approximate methods (IVF, HNSW) for O(log n)
- **Choice**: Exact search for demo scale, no approximation errors

### Chunking Strategy Impact

**500 words with 50-word overlap** based on testing:
- **Too small (100-200 words)**: Fragmented concepts, poor embeddings
- **Too large (1000+ words)**: Multiple topics per chunk, poor retrieval precision
- **Overlap prevents boundary issues**: Key information split across chunks\n\n## 🏢 Technical Architecture\n\n<table>\n<tr>\n<td width="50%">\n\n### 🔧 Backend (FastAPI)\n- 📄 **Document Processing**: PyPDF2 + pdfplumber for reliable text extraction\n- ✂️ **Text Chunking**: Smart splitting with overlap to preserve context\n- 🧠 **Embeddings**: sentence-transformers (all-MiniLM-L6-v2) for semantic understanding\n- 🔍 **Vector Search**: FAISS for fast similarity search\n- 🤖 **LLM Integration**: OpenRouter API for response generation\n- 💾 **Storage**: SQLite for query logging and document metadata\n\n</td>\n<td width="50%">\n\n### ⚙️ Frontend (React)\n- 🎨 **Modern UI**: Clean, responsive interface with glassmorphism design\n- 📤 **File Upload**: Drag-and-drop PDF ingestion with progress tracking\n- 💬 **Chat Interface**: Real-time Q&A with source attribution\n- 📈 **History & Metrics**: Track conversations and system performance\n\n</td>\n</tr>\n</table>\n\n## 🧠 Key Design Decisions (And What I Learned)

### Why 500-Word Chunks?
This took more experimentation than I expected. Started with 200 words because it seemed reasonable, but kept getting fragments without context. Tried 1000+ words next - that was worse because embeddings averaged out multiple topics per chunk.

500 words hit the sweet spot for most business documents I tested. Usually captures complete concepts with enough context for good embeddings.

### Why sentence-transformers?
Went with all-MiniLM-L6-v2 because:
- Runs locally (no API calls during search)
- Fast enough for real-time responses  
- Works well on general business documents
- 384 dimensions balance quality vs speed

Trade-off: Specialized models would probably work better for technical domains, but this handles most use cases.

### Why FAISS over Database Search?
For this scale, FAISS is simpler than setting up a proper vector database. No network calls, no complex configuration, full control over indexing.

Using exact search (IndexFlatIP) because the dataset is small enough that approximate methods don't provide meaningful speedup. Could upgrade later if needed.

### Why OpenRouter?
Pragmatic choice:
- Often better pricing than direct OpenAI API
- Easy to switch between different models
- More generous rate limits for experimentation

Downside is another dependency, but the flexibility is worth it for a learning project.\n\n## ⚠️ Known Limitations & Failure Cases

### When This System Fails

**Retrieval Failures** 🔍
- **Out-of-scope questions**: Low similarity scores (<0.3) but LLM still generates confident answers
- **Information spread**: Complete answers require combining 5+ chunks, but we only retrieve 3
- **Embedding bias**: Technical jargon embeds poorly with general-purpose model

**Generation Failures** 🤖
- **Confident hallucination**: LLM sounds authoritative but invents facts not in context
- **Context confusion**: Mixes information from different chunks incorrectly
- **Over-extrapolation**: Goes beyond what context actually says

**Document Processing Failures** 📄
- **Scanned PDFs**: No OCR capability, fails on image-based text
- **Complex layouts**: Tables and multi-column text produce garbled chunks
- **Boundary issues**: Key information split across chunk boundaries

### Why RAG Systems Sound Confident But Are Wrong

The most dangerous failure mode:
- LLMs trained to sound helpful and authoritative
- High similarity scores make system "think" it found good context
- No built-in uncertainty quantification
- Users trust confident-sounding responses

**Real example**: Context mentions "Q3 revenue was strong" → LLM responds "Q4 revenue was $2.3M" (hallucinated number)

### Evaluation Without Ground Truth

**The RAG Evaluation Challenge**:
Unlike supervised ML, RAG systems are hard to evaluate automatically:
- No ground truth labels for most documents
- "Correct" answers often have multiple valid formulations
- Context relevance is subjective

**What I Actually Do**:
1. **Manual spot checks**: Sample random queries, assess answer quality
2. **Similarity score monitoring**: Track average scores over time
3. **Failure case collection**: Keep examples of bad outputs
4. **User feedback**: When available, track satisfaction

**Red flags I watch for**:
- Dropping average similarity scores (knowledge base drift)
- Confident answers to out-of-scope questions (hallucination)
- Repetitive or template-like responses (prompt issues)\n\n## What This Project Demonstrates\n\nDespite its limitations, this system shows:\n\n✅ **RAG Fundamentals**: The core retrieve-then-generate pattern\n✅ **End-to-End Implementation**: From PDF upload to user response\n✅ **Production Considerations**: Error handling, logging, API design\n✅ **Practical Trade-offs**: Choosing simplicity over completeness\n✅ **Clean Architecture**: Modular, testable, extensible code\n\n## 🚀 Running Locally\n\n### 📝 Prerequisites\n- 🐍 Python 3.8+ and Node.js 16+\n- 🔑 OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai))\n\n### 🔧 Backend Setup\n```bash\ncd rag-chatbot-backend\npip install -r requirements.txt\n\n# Add your API key to .env\necho \"OPENROUTER_API_KEY=your_key_here\" > .env\n\n# Start the server\nuvicorn app.main:app --host 0.0.0.0 --port 8000\n```\n\n### ⚙️ Frontend Setup\n```bash\ncd rag-chatbot-frontend\nnpm install\nnpm start\n```\n\nAccess the application at `http://localhost:3000`\n\n## 📝 Usage\n\n1. **Upload Documents**: Use the \"Upload PDF\" tab to add documents to your knowledge base\n2. **Ask Questions**: Switch to the \"Chat\" tab and ask questions about your documents\n3. **Review History**: Check the \"History\" tab to see previous conversations\n4. **Monitor Performance**: Click the \"Metrics\" button to see system statistics\n\n## 🔮 What I'd Improve Next (With Reasoning)

### Short Term Improvements
- **Re-ranking with cross-encoder**: Address the "3rd result more relevant than 1st" problem
- **Hybrid search**: Combine vector similarity with keyword matching for exact matches
- **Confidence scoring**: Use similarity scores + generation uncertainty to flag low-confidence answers
- **Better error messages**: Help users understand when/why the system fails

### Medium Term Architecture Changes
- **Conversation memory**: Track context across multiple questions in a session
- **Adaptive chunking**: Respect document structure (tables, sections, code blocks)
- **Evaluation framework**: Automated quality assessment with test question sets
- **Source attribution**: Track which specific chunks contributed to each answer

### Long Term Research Directions
- **Multi-modal RAG**: Handle images, charts, and tables in PDFs
- **Active learning**: Improve system based on user feedback and corrections
- **Query expansion**: Automatically rephrase questions for better retrieval
- **Uncertainty quantification**: Reliable confidence estimates for answers\n\n## 💡 What I Learned Building This

Started this project to understand RAG beyond the marketing hype. Wanted to build something from scratch rather than using frameworks like LangChain, so I could really understand the fundamentals and trade-offs.

Key insights:
- **Chunking matters more than I expected** - spent way more time on this than anticipated
- **Embeddings aren't magic** - they miss exact matches that keyword search would catch
- **Evaluation is genuinely hard** - no ground truth for most real documents
- **LLMs hallucinate even with good context** - confidence doesn't equal correctness
- **Simple approaches often work better** - resisted the urge to over-engineer

The goal was building something that works well for the common case and demonstrates core RAG concepts clearly. It's a solid foundation that could be extended, but it's also useful as-is for many document Q&A scenarios.

<img width="1361" height="691" alt="rag 1" src="https://github.com/user-attachments/assets/109afa01-8829-4e6d-ad6f-0619af20c7a1" />
<img width="1128" height="416" alt="rag2" src="https://github.com/user-attachments/assets/5856a2cc-ebc1-4270-ac83-fb06dcdbb5ef" />
<img width="1362" height="686" alt="rag 3" src="https://github.com/user-attachments/assets/4259b04b-4a5a-4567-9f7f-ad9d1627b096" />
<img width="1364" height="687" alt="rag 4" src="https://github.com/user-attachments/assets/4ee601c1-3254-427d-92f5-f9c3763fb5cf" />
<img width="1364" height="687" alt="rag 5" src="https://github.com/user-attachments/assets/4c3542f1-77b5-4c17-bfd6-33c07ba59fe6" />




