from typing import List
import re

class DocumentChunker:
    """
    Splits documents into chunks for better retrieval.
    
    The chunk size thing took way more experimentation than I expected.
    Started with 200 words because it seemed reasonable, but kept getting
    fragments like "The algorithm works well" with zero context about
    which algorithm or why it works well.
    
    Tried 1000+ words next - that was worse. The embeddings seemed to 
    average out all the different topics in each chunk, so retrieval
    got really imprecise.
    
    500 words feels like the sweet spot for most business docs I've tested.
    Usually captures 1-2 complete ideas with enough context for the 
    embedding model to do its thing properly.
    
    The 50-word overlap was born out of frustration with the "boundary problem" -
    kept finding key info split across chunks. Like chunk N ending with
    "The solution requires:" and chunk N+1 starting with the actual steps.
    50 words usually covers 2-3 sentences, which seems to bridge most gaps.
    
    This approach definitely doesn't work for everything though. Tables get
    mangled, code snippets break weirdly, and structured docs need different
    treatment. Good enough for now.
    """
    
    def __init__(self, target_chunk_size: int = 500, overlap_size: int = 50):
        # These values work well for general business documents
        # Technical papers might benefit from larger chunks, tweets from smaller ones
        self.target_chunk_size = target_chunk_size
        self.overlap_size = overlap_size
    
    def split_into_chunks(self, document_text: str) -> List[str]:
        """
        Split document text into overlapping chunks using word-based splitting.
        
        I use word-based chunking rather than character-based because:
        - More predictable chunk sizes
        - Doesn't break words in half
        - Easier to reason about overlap
        
        Trade-off: Doesn't respect sentence boundaries, so some chunks might
        end mid-sentence. The sentence-based method below handles this better
        but is more complex.
        """
        words = document_text.split()
        if not words:
            return []
        
        chunks = []
        
        # Create overlapping windows of words
        # Step size = chunk_size - overlap to create the overlap
        step_size = self.target_chunk_size - self.overlap_size
        
        for start_idx in range(0, len(words), step_size):
            # Extract a chunk of words
            end_idx = start_idx + self.target_chunk_size
            chunk_words = words[start_idx:end_idx]
            
            if chunk_words:  # Only add non-empty chunks
                chunk_text = ' '.join(chunk_words)
                chunks.append(chunk_text.strip())
        
        return chunks
    
    def split_by_sentences(self, document_text: str) -> List[str]:
        """
        Split text into chunks that respect sentence boundaries.
        
        This method is more sophisticated - it tries to keep complete sentences
        together while staying within the target chunk size. Better for readability
        but more complex logic.
        
        I use this for documents where sentence structure is important,
        like legal documents or academic papers.
        """
        # Split into sentences using common sentence endings
        # This regex isn't perfect (doesn't handle "Dr. Smith" well) but works for most text
        sentences = re.split(r'[.!?]+', document_text)
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        
        if not sentences:
            return []
        
        chunks = []
        current_chunk_sentences = []
        current_word_count = 0
        
        for sentence in sentences:
            sentence_word_count = len(sentence.split())
            
            # If adding this sentence would exceed our target size, finalize current chunk
            if (current_word_count + sentence_word_count > self.target_chunk_size 
                and current_chunk_sentences):
                
                # Save the current chunk
                chunk_text = ' '.join(current_chunk_sentences)
                chunks.append(chunk_text)
                
                # Start new chunk with overlap from previous chunk
                # Keep the last few sentences for context
                overlap_sentence_count = max(1, self.overlap_size // 20)  # Rough estimate
                overlap_sentences = current_chunk_sentences[-overlap_sentence_count:]
                
                current_chunk_sentences = overlap_sentences + [sentence]
                current_word_count = sum(len(s.split()) for s in current_chunk_sentences)
            else:
                # Add sentence to current chunk
                current_chunk_sentences.append(sentence)
                current_word_count += sentence_word_count
        
        # Don't forget the last chunk
        if current_chunk_sentences:
            final_chunk = ' '.join(current_chunk_sentences)
            chunks.append(final_chunk)
        
        return chunks