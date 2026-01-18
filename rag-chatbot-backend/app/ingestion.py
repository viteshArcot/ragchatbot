import PyPDF2
import pdfplumber
from typing import List, Dict, Any
from .chunking import DocumentChunker
from .embeddings import document_retriever
import uuid
from io import BytesIO

class PDFProcessor:
    """
    Handles the complete pipeline from PDF upload to searchable chunks.
    
    The process: PDF bytes → extracted text → chunks → embeddings → searchable index
    
    I use two PDF libraries because PDF text extraction is notoriously unreliable:
    - PyPDF2: Fast and handles most PDFs well
    - pdfplumber: Slower but better with complex layouts, tables
    
    If both fail, the PDF probably has text as images (scanned document)
    and would need OCR, which I haven't implemented.
    """
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.text_chunker = DocumentChunker(chunk_size, overlap)
    
    def _extract_with_pypdf2(self, pdf_bytes: bytes) -> str:
        """
        Primary PDF text extraction method using PyPDF2.
        
        PyPDF2 is fast and works well for most business documents.
        It struggles with:
        - Complex layouts (multi-column text)
        - Tables with merged cells
        - Documents with unusual fonts
        """
        try:
            pdf_file = BytesIO(pdf_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            extracted_text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:  # Some pages might be empty or image-only
                    extracted_text += page_text + "\n\n"  # Add spacing between pages
            
            return extracted_text
        except Exception as e:
            raise Exception(f"PyPDF2 extraction failed: {str(e)}")
    
    def _extract_with_pdfplumber(self, pdf_bytes: bytes) -> str:
        """
        Fallback PDF text extraction using pdfplumber.
        
        pdfplumber is more sophisticated - it can handle tables and complex layouts
        better than PyPDF2, but it's slower. I use it as a fallback when PyPDF2
        fails or produces poor results.
        """
        try:
            with pdfplumber.open(BytesIO(pdf_bytes)) as pdf_document:
                extracted_text = ""
                
                for page in pdf_document.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n\n"
                
                return extracted_text
        except Exception as e:
            raise Exception(f"pdfplumber extraction failed: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """
        Extract text from PDF with automatic fallback between extraction methods.
        
        I try PyPDF2 first because it's faster. If that fails or produces
        very little text, I fall back to pdfplumber.
        
        Future improvement: Could add heuristics to detect which method
        to use based on PDF characteristics.
        """
        try:
            # Try the fast method first
            text = self._extract_with_pypdf2(pdf_bytes)
            
            # If we got very little text, the PDF might have complex layout
            # Try the more sophisticated extractor
            if len(text.strip()) < 100:  # Arbitrary threshold
                text = self._extract_with_pdfplumber(pdf_bytes)
            
            return text
        except:
            # If PyPDF2 completely failed, try pdfplumber
            return self._extract_with_pdfplumber(pdf_bytes)
    
    def process_uploaded_pdf(self, pdf_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Complete pipeline: PDF → text → chunks → searchable index.
        
        This is the main entry point for PDF processing. It coordinates
        all the steps and returns metadata about what was processed.
        
        Returns information the API can send back to the user so they know
        what happened to their document.
        """
        # Step 1: Extract text from the PDF
        document_text = self.extract_text_from_pdf(pdf_bytes)
        
        if not document_text.strip():
            raise Exception(
                "No text could be extracted from this PDF. "
                "It might be a scanned document that needs OCR."
            )
        
        # Step 2: Split the text into manageable chunks
        text_chunks = self.text_chunker.split_into_chunks(document_text)
        
        if not text_chunks:
            raise Exception("Document text could not be split into chunks")
        
        # Step 3: Generate a unique ID for this document
        # This helps us track which chunks came from which document
        document_id = str(uuid.uuid4())
        
        # Step 4: Prepare metadata for each chunk
        # This metadata gets stored alongside the embeddings so we can
        # trace results back to their source
        chunk_metadata = []
        for chunk_index, chunk_text in enumerate(text_chunks):
            metadata = {
                'chunk_id': f"{document_id}_{chunk_index}",
                'doc_id': document_id,
                'filename': filename,
                'text': chunk_text,
                'chunk_index': chunk_index
                # Future: Could add page numbers, section headers, etc.
            }
            chunk_metadata.append(metadata)
        
        # Step 5: Add chunks to the searchable index
        # This creates embeddings and adds them to FAISS
        document_retriever.add_document_chunks(text_chunks, chunk_metadata)
        
        # Return summary information for the API response
        return {
            'doc_id': document_id,
            'filename': filename,
            'num_chunks': len(text_chunks),
            'total_text_length': len(document_text),
            'avg_chunk_length': len(document_text) // len(text_chunks) if text_chunks else 0
        }

# Global PDF processor instance
# Using a global instance avoids recreating the chunker for every request
pdf_processor = PDFProcessor()