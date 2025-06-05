"""
PDF Processing Service for LEVRA Voice Assistant

Handles PDF upload, text extraction, and context management
for enhanced AI conversations with document context.
"""

import PyPDF2
import io
import re
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    """
    Service class for processing PDF documents and extracting text content
    for use in AI conversations.
    """
    
    def __init__(self):
        """Initialize the PDF processor."""
        self.max_file_size = 10 * 1024 * 1024  # 10MB limit
        self.max_text_length = 50000  # Reasonable context limit
    
    def extract_text_from_pdf(self, pdf_file) -> Dict[str, any]:
        """
        Extract text content from uploaded PDF file.
        
        Args:
            pdf_file: File object from Flask request
            
        Returns:
            Dict containing extracted text, metadata, and status
        """
        try:
            # Validate file size
            if pdf_file.content_length and pdf_file.content_length > self.max_file_size:
                return {
                    "success": False,
                    "error": "File size exceeds 10MB limit",
                    "text": "",
                    "metadata": {}
                }
            
            # Read PDF content
            pdf_bytes = pdf_file.read()
            pdf_file_obj = io.BytesIO(pdf_bytes)
            
            # Extract text using PyPDF2
            reader = PyPDF2.PdfReader(pdf_file_obj)
            
            # Get metadata
            metadata = {
                "filename": pdf_file.filename,
                "num_pages": len(reader.pages),
                "file_size": len(pdf_bytes)
            }
            
            # Extract text from all pages
            extracted_text = ""
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    extracted_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num + 1}: {e}")
                    continue
            
            # Clean and process text
            cleaned_text = self._clean_text(extracted_text)
            
            # Truncate if too long
            if len(cleaned_text) > self.max_text_length:
                cleaned_text = cleaned_text[:self.max_text_length] + "\n\n[Text truncated due to length...]"
                metadata["truncated"] = True
            
            return {
                "success": True,
                "text": cleaned_text,
                "metadata": metadata,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"PDF processing error: {e}")
            return {
                "success": False,
                "error": f"Failed to process PDF: {str(e)}",
                "text": "",
                "metadata": {}
            }
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text ready for AI processing
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Remove page headers/footers patterns (common noise)
        text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\d{1,2}/\d{1,2}/\d{4}', '', text)  # Remove dates
        
        # Normalize line breaks
        text = text.strip()
        
        return text
    
    def create_context_prompt(self, pdf_text: str, metadata: Dict) -> str:
        """
        Create a formatted context prompt for the AI agent.
        
        Args:
            pdf_text: Extracted PDF text
            metadata: File metadata
            
        Returns:
            Formatted context prompt
        """
        context_prompt = f"""
DOCUMENT CONTEXT:
================
Filename: {metadata.get('filename', 'Unknown')}
Pages: {metadata.get('num_pages', 'Unknown')}
Content Length: {len(pdf_text)} characters

DOCUMENT CONTENT:
{pdf_text}

================
END OF DOCUMENT CONTEXT

Instructions: Use the above document as context for our conversation. Reference specific information from the document when relevant to provide more personalized and accurate responses.
"""
        return context_prompt

# Global processor instance
pdf_processor = PDFProcessor()
