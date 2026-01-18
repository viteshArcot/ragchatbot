# Things That Break (And Why)

Running notes on when this RAG system fails and what I've learned from debugging it.

## Retrieval going wrong

**Questions outside the knowledge base**
This happens more than I expected. User asks about something not in any uploaded documents, but the system still finds the "best match" and the LLM generates a confident answer anyway. 

Example: Documents about car maintenance, user asks about cooking recipes. System finds some chunk about "maintenance schedules" (because it mentions time/frequency), LLM confidently explains meal prep schedules.

The similarity scores are usually low (<0.3) but I don't surface that to users yet. Should probably add some kind of "I'm not confident about this" warning.

**Information spread everywhere**
Some questions need info from like 5+ different sections to answer properly, but I only retrieve 3 chunks. Get a lot of "I need more information" responses or partial answers.

Worst case was a financial report where revenue was in one section, expenses in another, and the analysis in a third. User asked about profit margins and got a very incomplete picture.

Could retrieve more chunks but then the prompt gets unwieldy and costs go up.

**Embedding model bias**
The all-MiniLM model I'm using was trained on general web text, so it struggles with specialized domains. Medical documents with Latin terms, legal docs with specific citations, technical manuals with part numbers.

Relevant chunks get low similarity scores even when they're actually on-topic. Domain-specific models would help but add complexity.

## Generation problems

**Confident hallucination (the scary one)**
LLM generates detailed, authoritative-sounding answers that aren't supported by the context. This is the most dangerous failure mode because users trust confident responses.

Real example I hit: Context mentioned "quarterly results were strong" but LLM responded with "Q4 revenue was $2.3M" - completely made up that number.

Happens even with explicit instructions to stick to the context. LLMs are trained to be helpful and confident, hard to make them say "I don't know."

**Context confusion**
LLM mixes information from different chunks incorrectly. Like taking Product A's price from chunk 1 and Product B's features from chunk 2, then saying Product A has those features at that price.

Worse when chunks are about similar but distinct things. The model doesn't track provenance well within the context.

**Going beyond the context**
LLM adds implications or predictions not actually in the source material. Context says "sales increased 10% in Q1" and LLM responds "this trend will continue throughout the year."

Usually trying to be helpful by elaborating, but it's adding information that isn't there.

## Document processing issues

**Scanned PDFs**
PyPDF2 and pdfplumber can't handle image-based text. Scanned contracts, photographed documents, anything that needs OCR just fails completely. System appears broken from user perspective.

Should add OCR preprocessing but that's a whole other complexity layer.

**Complex layouts**
Tables, multi-column text, documents with figures - the text extraction gets garbled. End up with chunks that are fragments of sentences in random order.

Financial statements are particularly bad. The reading order doesn't match visual layout.

**Mixed languages**
The embedding model is optimized for English. Spanish documents, code mixed with comments, anything non-English performs poorly.

Multilingual models exist but again, adds complexity.

## Chunking boundary problems

**Tables split across chunks**
Table headers in one chunk, actual data in another. LLM can't interpret the structure properly.

Price lists are the worst - "Product | Price" header in chunk N, actual prices in chunk N+1.

**Math formulas**
Equations get split mid-formula. "E = mc" in one chunk, "² where c is the speed of light" in the next. 

Word-based chunking doesn't understand semantic units.

## Scale issues I haven't hit yet but will

**Large document collections**
FAISS IndexFlatIP is O(n) exact search. Works fine for a few thousand chunks but will get slow with 10k+.

Approximate search methods exist but introduce their own complexity and potential quality issues.

**Concurrent users**
SQLite isn't great for concurrent writes. FAISS index could get corrupted with multiple simultaneous updates.

Would need proper database and locking mechanisms for real multi-user scenarios.

## Detection strategies that actually work

**Similarity score monitoring**
I track average similarity scores over time. Dropping averages usually indicate knowledge base drift or users asking different types of questions.

Below 0.3 is almost always out-of-scope. Above 0.7 is usually good. The middle range is where things get tricky.

**Response pattern watching**
Look for:
- High frequency of "I don't have enough information" responses
- Very repetitive answers (suggests prompt issues)
- Very short responses (possible context problems)
- Very long responses (possible hallucination)

**Manual spot checks**
Still the most reliable method. Sample 10-20 random queries, check answers against source documents. Tedious but catches things automated metrics miss.

## Why RAG systems sound confident but are wrong

This is the fundamental problem: LLMs are trained to sound helpful and authoritative. High similarity scores make the system "think" it found good context. Users trust confident-sounding responses. No built-in uncertainty quantification.

The combination is dangerous - system finds "relevant" context, LLM fills in gaps from training data, response sounds authoritative and specific, user believes it.

## When not to use RAG

RAG isn't always the answer. Better alternatives:
- Need exact information → search engines
- Structured data → proper database queries  
- Real-time info → APIs, not static documents
- High accuracy requirements → rule-based systems
- Small, well-defined knowledge → fine-tune smaller models

RAG works best for large, unstructured document collections where approximate answers are acceptable and context helps but isn't mission-critical.

## Evaluation reality

Unlike supervised ML, RAG evaluation is messy. No ground truth for most real documents. "Correct" answers often have multiple valid formulations. Context relevance is subjective.

What actually works:
1. Human evaluation (expensive, doesn't scale)
2. Similarity score monitoring (proxy metric, not ground truth)
3. User feedback (when available, often biased)
4. Failure case collection (learn from mistakes)

Most production RAG systems rely heavily on manual spot-checking and user complaints. Automated evaluation is still an active research area with no perfect solutions.