"""
Document loader for processing various file types.
Supports PDF, Markdown, TXT, and DOCX files.
"""

import os
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.config import get_settings
from app.utils.logger import logger
from app.utils.chunking import chunk_text


class DocumentLoader:
    """Service for loading and processing documents."""
    
    def __init__(self):
        settings = get_settings()
        self.upload_dir = Path(settings.upload_dir)
        self.allowed_extensions = settings.allowed_extensions_list
        self.max_file_size = settings.max_file_size_bytes
        
        # Ensure upload directory exists
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_file(self, filename: str, file_size: int) -> tuple[bool, str]:
        """
        Validate file before processing.
        
        Args:
            filename: Name of the file
            file_size: Size of the file in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check extension
        ext = Path(filename).suffix.lower()
        if ext not in self.allowed_extensions:
            return False, f"File type {ext} not allowed. Allowed: {', '.join(self.allowed_extensions)}"
        
        # Check size
        if file_size > self.max_file_size:
            max_mb = self.max_file_size / (1024 * 1024)
            return False, f"File too large. Maximum size: {max_mb:.1f}MB"
        
        return True, ""
    
    async def save_file(self, filename: str, content: bytes) -> tuple[str, Path]:
        """
        Save uploaded file to disk.
        
        Args:
            filename: Original filename
            content: File content as bytes
            
        Returns:
            Tuple of (document_id, file_path)
        """
        # Generate unique document ID
        doc_id = f"doc_{uuid.uuid4().hex[:12]}"
        
        # Create safe filename
        ext = Path(filename).suffix.lower()
        safe_filename = f"{doc_id}{ext}"
        file_path = self.upload_dir / safe_filename
        
        # Write file
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"Saved file: {safe_filename}")
        return doc_id, file_path
    
    def load_text_file(self, file_path: Path) -> str:
        """Load content from a text file (.txt, .md)."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()
    
    def load_pdf(self, file_path: Path) -> str:
        """Load content from a PDF file."""
        try:
            from pypdf import PdfReader
            
            reader = PdfReader(str(file_path))
            text_parts = []
            
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            
            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
            return ""
    
    def load_docx(self, file_path: Path) -> str:
        """Load content from a DOCX file."""
        try:
            from docx import Document
            
            doc = Document(str(file_path))
            text_parts = []
            
            for para in doc.paragraphs:
                if para.text.strip():
                    text_parts.append(para.text)
            
            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"Error loading DOCX: {e}")
            return ""
    
    def load_file(self, file_path: Path) -> str:
        """
        Load content from a file based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Extracted text content
        """
        ext = file_path.suffix.lower()
        
        if ext in [".txt", ".md"]:
            return self.load_text_file(file_path)
        elif ext == ".pdf":
            return self.load_pdf(file_path)
        elif ext == ".docx":
            return self.load_docx(file_path)
        else:
            logger.warning(f"Unsupported file type: {ext}")
            return ""
    
    async def process_file(
        self,
        filename: str,
        content: bytes
    ) -> Dict[str, Any]:
        """
        Process an uploaded file: save, extract text, and chunk.
        
        Args:
            filename: Original filename
            content: File content as bytes
            
        Returns:
            Dict with document info and chunks
        """
        # Validate
        is_valid, error = self.validate_file(filename, len(content))
        if not is_valid:
            return {"success": False, "error": error}
        
        # Save file
        doc_id, file_path = await self.save_file(filename, content)
        
        # Extract text
        text = self.load_file(file_path)
        
        if not text.strip():
            return {
                "success": False,
                "error": "Could not extract text from file"
            }
        
        # Determine if markdown for better chunking
        is_markdown = file_path.suffix.lower() == ".md"
        
        # Chunk the text
        chunks = chunk_text(text, is_markdown=is_markdown)
        
        if not chunks:
            return {
                "success": False,
                "error": "Could not chunk document"
            }
        
        # Prepare metadata
        file_stat = file_path.stat()
        metadata = {
            "document_id": doc_id,
            "filename": filename,
            "file_type": file_path.suffix.lower(),
            "file_size": file_stat.st_size,
            "uploaded_at": datetime.now().isoformat(),
        }
        
        return {
            "success": True,
            "document_id": doc_id,
            "filename": filename,
            "file_type": file_path.suffix.lower(),
            "file_size": file_stat.st_size,
            "chunks": chunks,
            "chunk_count": len(chunks),
            "metadata": metadata,
        }
    
    def delete_file(self, document_id: str) -> bool:
        """
        Delete a document file from disk.
        
        Args:
            document_id: The document ID
            
        Returns:
            True if file was deleted
        """
        # Find file with this document ID
        for file_path in self.upload_dir.iterdir():
            if file_path.stem == document_id:
                try:
                    file_path.unlink()
                    logger.info(f"Deleted file: {file_path.name}")
                    return True
                except Exception as e:
                    logger.error(f"Error deleting file: {e}")
                    return False
        
        logger.warning(f"File not found for document: {document_id}")
        return False
    
    def list_files(self) -> List[Dict[str, Any]]:
        """List all uploaded files."""
        files = []
        
        for file_path in self.upload_dir.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    "filename": file_path.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
        
        return files


# Singleton instance
_document_loader: Optional[DocumentLoader] = None


def get_document_loader() -> DocumentLoader:
    """Get or create the document loader singleton."""
    global _document_loader
    if _document_loader is None:
        _document_loader = DocumentLoader()
    return _document_loader

