# Interview Prep Notes - RAG Project

Stuff I should be able to explain about this project if it comes up in interviews.

## The "explain how RAG works" question

RAG is basically smart prompt engineering. Instead of just asking a language model a question cold, you first grab some relevant context from your documents, then ask the model to answer based on that context.

The key thing I learned is that it's really three separate steps: retrieval (find potentially relevant stuff), context assembly (format it nicely), and generation (LLM does its thing). Each step can fail in different ways.

In my version, I use sentence-transformers to turn both documents and questions into vectors, then FAISS finds the most similar chunks. The LLM gets the question plus the top 3 chunks as context.

## Why embeddings instead of keyword search?

I actually tried both. Keyword search kept missing obvious matches - like "car repair" wouldn't find "automotive maintenance" even though they're basically the same thing. Embeddings handle that semantic similarity naturally.

Downside is embeddings can completely whiff on exact matches. If someone asks for "Model XYZ-123", keyword search would nail it, but embeddings might not if that model number doesn't show up in similar contexts.

For document Q&A, semantic search usually works better, but hybrid approaches are probably the way to go long-term.

## The evaluation question (this one's tricky)

This is honestly one of the hardest parts. Unlike normal ML where you have labeled data, RAG systems are tough to evaluate automatically. Most real documents don't come with ground truth Q&A pairs.

What I actually do:
- Manual spot checks on random queries
- Watch similarity scores over time (dropping averages usually mean something's wrong)
- Collect examples when things go wrong
- Track user feedback when I can get it

I look for red flags like confident answers to questions that are clearly outside the knowledge base, or very repetitive responses that suggest prompt issues.

Honest truth: most production RAG systems I've read about rely heavily on human evaluation and user complaints. The automated evaluation stuff is still being figured out.

## Main failure modes I've seen

Retrieval failures: question outside the knowledge base, information spread across too many sections, embedding model getting confused on technical jargon.

Generation failures: confident hallucination (sounds certain but wrong), mixing up info from different chunks, going beyond what the context actually says.

System stuff: PDF parsing creating garbage chunks, important info getting split at chunk boundaries.

The scariest one is confident hallucination - the system sounds authoritative but is factually wrong. Users trust confident responses.

## Chunk size decision

Tested different sizes on business documents. 100-200 words gave me fragments without context. 1000+ words had too many topics per chunk, so embeddings got averaged out and retrieval precision sucked.

500 words hit the sweet spot - usually 1-2 complete concepts with enough context for good embeddings. 50-word overlap prevents the boundary problem where key info gets split.

Doesn't work great for all document types though. Tables and code need different approaches.

## FAISS choice

For this scale, FAISS is simpler than setting up a proper vector database. No network calls, no database config, full control over indexing. I use exact search because the dataset is small enough that approximate methods don't help much.

For production scale I'd probably switch to something like Pinecone or pgvector for persistence and concurrent access.

## What I'd improve

Short term: re-ranking with a cross-encoder (sometimes result #4 is more relevant than #1), hybrid search combining vector and keyword, better confidence scoring.

Medium term: conversation memory for follow-up questions, smarter chunking that respects document structure, some kind of evaluation framework.

Long term: multi-modal stuff for images and tables, learning from user feedback, proper vector database.

Key thing is each improvement adds complexity. I kept this version simple to nail the core concepts.

## Questions I'd ask them

- What types of documents and use cases would this handle?
- How do you currently evaluate model quality?
- What's the expected scale?
- How does the team balance research with production reliability?
- What's the process for handling model failures?

## Things not to say

- "RAG eliminates hallucination" (it reduces but doesn't eliminate)
- "My system is production-ready" (it's a learning project with known limitations)
- "Embeddings are always better" (depends on use case)
- "Higher similarity = better answers" (correlation, not causation)

Better to emphasize understanding trade-offs, experience with failure modes, honest assessment of capabilities.