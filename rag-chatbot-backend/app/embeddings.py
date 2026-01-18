from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Tuple

class DocumentRetriever:
    """
    Handles the retrieval part of the RAG pipeline.
    
    I went with embeddings over keyword search after trying both approaches.
    The semantic matching just works better for document Q&A - "car repair" 
    actually finds "automotive maintenance" which feels like magic when it works.
    
    Trade-off I learned the hard way: embeddings completely miss exact matches.
    If someone asks for "Model XYZ-123", keyword search would nail it, but 
    embeddings might whiff if that model number doesn't appear in similar contexts.
    
    FAISS choice was mostly practical - I needed something that scales better
    than numpy cosine similarity but didn't want to set up a whole vector database.
    IndexFlatIP gives me exact search (no approximation weirdness) and I can
    always upgrade to approximate methods later if I need the speed.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Load the embedding model once at startup
        # This model converts text to 384-dimensional vectors
        self.embedding_model = SentenceTransformer(model_name)
        
        # FAISS index for fast similarity search
        # Using IndexFlatIP (inner product) because it's simple and works well
        self.vector_index = None
        
        # Keep track of the actual text chunks and their metadata
        self.stored_chunks = []
        self.chunk_metadata = []
        
    def _create_embeddings(self, text_chunks: List[str]) -> np.ndarray:
        """
        Convert text chunks into vector embeddings.
        
        The sentence-transformer model does the heavy lifting here - it understands
        semantic meaning, so 'car' and 'automobile' will have similar embeddings.
        """
        return self.embedding_model.encode(text_chunks)
    
    def build_initial_index(self, initial_documents: List[str]):
        """
        Create the vector index with some starter documents.
        
        I include a few example documents so the system works out of the box,
        even before users upload their own PDFs.
        """
        self.stored_chunks = initial_documents
        self.chunk_metadata = [{'text': doc, 'source': 'system'} for doc in initial_documents]
        
        # Convert documents to embeddings
        embeddings = self._create_embeddings(initial_documents)
        
        # Create FAISS index
        # Using inner product similarity, which approximates cosine similarity after normalization
        embedding_dimension = embeddings.shape[1]
        self.vector_index = faiss.IndexFlatIP(embedding_dimension)
        
        # Normalize embeddings for cosine similarity
        # This is important - without normalization, longer documents would dominate
        faiss.normalize_L2(embeddings)
        self.vector_index.add(embeddings.astype('float32'))
    
    def add_document_chunks(self, new_chunks: List[str], metadata: List[dict] = None):
        """
        Add new document chunks to the existing index.
        
        This happens when users upload PDFs - we chunk them and add to our searchable index.
        In a production system, I'd probably batch these operations for efficiency.
        """
        if not new_chunks:
            return
            
        # Convert new chunks to embeddings
        new_embeddings = self._create_embeddings(new_chunks)
        faiss.normalize_L2(new_embeddings)
        
        # Initialize index if this is the first time
        if self.vector_index is None:
            embedding_dimension = new_embeddings.shape[1]
            self.vector_index = faiss.IndexFlatIP(embedding_dimension)
            self.stored_chunks = []
            self.chunk_metadata = []
        
        # Add to the searchable index
        self.vector_index.add(new_embeddings.astype('float32'))
        self.stored_chunks.extend(new_chunks)
        
        # Store metadata for each chunk (filename, page number, etc.)
        if metadata:
            self.chunk_metadata.extend(metadata)
        else:
            # Fallback metadata if none provided
            self.chunk_metadata.extend([{'text': chunk, 'source': 'uploaded'} for chunk in new_chunks])
    
    def find_relevant_chunks(self, user_question: str, num_results: int = 5) -> Tuple[List[str], List[float]]:
        """
        The core retrieval logic - convert question to embedding, find similar chunks.
        
        This part only does retrieval, not generation. Took me a while to really
        get this separation - retrieval finds potentially relevant stuff, but it
        doesn't know if those chunks actually answer the question. That's the LLM's job.
        
        Similarity scores I've learned to interpret:
        - Above 0.7: Usually spot-on, same topic
        - 0.4-0.7: Might be relevant, worth including  
        - Below 0.4: Probably off-topic, but sometimes surprises me
        
        The tricky part is that high similarity doesn't guarantee a good answer.
        I've seen chunks about "car maintenance schedules" score 0.85 for 
        "when should I change oil?" but not actually contain the answer.
        
        I stick with top-5 because more than that and the prompt gets unwieldy,
        plus I found diminishing returns after the first few results anyway.
        
        TODO: The no-reranking thing bites me sometimes - result #4 can be more
        relevant than #1 for specific questions, but I don't catch that.
        """
        if not self.vector_index or not self.stored_chunks:
            return [], []
            
        # Convert the user's question to the same embedding space as our documents
        question_embedding = self.embedding_model.encode([user_question])
        faiss.normalize_L2(question_embedding)
        
        # Search for similar chunks
        # FAISS returns similarity scores and indices of the most similar chunks
        similarity_scores, chunk_indices = self.vector_index.search(
            question_embedding.astype('float32'), num_results
        )
        
        # Extract the actual text chunks and their similarity scores
        # TODO: Should probably add some filtering here for very low similarity scores
        # but for now just return whatever FAISS gives us
        retrieved_chunks = [
            self.stored_chunks[idx] for idx in chunk_indices[0] 
            if idx < len(self.stored_chunks)
        ]
        similarity_values = similarity_scores[0].tolist()
        
        return retrieved_chunks, similarity_values

# Global document retriever instance
# I use a global instance to avoid reloading the embedding model on every request
document_retriever = DocumentRetriever()

# Initialize with some example documents so the system works immediately
# These help users understand what the system can do before they upload their own PDFs
example_knowledge_base = [
    "FastAPI is a modern web framework for building APIs with Python.",
    "RAG combines retrieval and generation for better AI responses.",
    "Vector databases store embeddings for similarity search.",
    "OpenRouter provides access to multiple language models.",
    "FAISS is a library for efficient similarity search."
]
document_retriever.build_initial_index(example_knowledge_base)