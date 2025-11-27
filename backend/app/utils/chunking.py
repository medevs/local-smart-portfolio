"""
Text chunking utilities for document processing.
Uses LangChain text splitters for intelligent chunking.
"""

from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownTextSplitter
from app.config import get_settings
from app.utils.logger import logger


def create_text_splitter(
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
    is_markdown: bool = False
) -> RecursiveCharacterTextSplitter:
    """
    Create a text splitter with the specified parameters.
    
    Args:
        chunk_size: Maximum size of each chunk
        chunk_overlap: Number of characters to overlap between chunks
        is_markdown: Whether to use markdown-aware splitting
        
    Returns:
        Configured text splitter
    """
    settings = get_settings()
    
    size = chunk_size or settings.chunk_size
    overlap = chunk_overlap or settings.chunk_overlap
    
    if is_markdown:
        return MarkdownTextSplitter(
            chunk_size=size,
            chunk_overlap=overlap,
        )
    
    return RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def chunk_text(
    text: str,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
    is_markdown: bool = False
) -> List[str]:
    """
    Split text into chunks.
    
    Args:
        text: The text to chunk
        chunk_size: Maximum size of each chunk
        chunk_overlap: Number of characters to overlap between chunks
        is_markdown: Whether to use markdown-aware splitting
        
    Returns:
        List of text chunks
    """
    if not text or not text.strip():
        logger.warning("Empty text provided for chunking")
        return []
    
    splitter = create_text_splitter(chunk_size, chunk_overlap, is_markdown)
    chunks = splitter.split_text(text)
    
    logger.debug(f"Split text into {len(chunks)} chunks")
    return chunks


def chunk_documents(
    documents: List[dict],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None
) -> List[dict]:
    """
    Chunk a list of documents while preserving metadata.
    
    Args:
        documents: List of dicts with 'content' and 'metadata' keys
        chunk_size: Maximum size of each chunk
        chunk_overlap: Number of characters to overlap between chunks
        
    Returns:
        List of chunked documents with metadata
    """
    chunked_docs = []
    
    for doc in documents:
        content = doc.get("content", "")
        metadata = doc.get("metadata", {})
        
        # Determine if markdown based on file extension
        filename = metadata.get("filename", "")
        is_markdown = filename.lower().endswith(".md")
        
        chunks = chunk_text(content, chunk_size, chunk_overlap, is_markdown)
        
        for i, chunk in enumerate(chunks):
            chunked_docs.append({
                "content": chunk,
                "metadata": {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                }
            })
    
    logger.info(f"Chunked {len(documents)} documents into {len(chunked_docs)} chunks")
    return chunked_docs

