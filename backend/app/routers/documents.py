"""
Unified document management endpoints.
Combines upload, list, delete operations with admin key protection.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from app.models.document import DocumentUploadResponse, DocumentMetadata, DocumentDeleteResponse
from app.models.response import DatabaseStats
from app.services.rag import get_rag_service
from app.config import get_settings
from app.utils.logger import logger
from app.utils.auth import verify_admin_key
from datetime import datetime

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(..., description="Document file to upload"),
    _: bool = Depends(verify_admin_key)
) -> DocumentUploadResponse:
    """
    Upload and ingest a document into the knowledge base.
    
    Requires X-Admin-Key header.
    
    Supported file types: .pdf, .md, .txt, .docx
    
    Args:
        file: The uploaded file
        
    Returns:
        DocumentUploadResponse with document metadata
    """
    settings = get_settings()
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Read file content
    content = await file.read()
    
    if len(content) > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {settings.max_file_size_mb}MB"
        )
    
    logger.info(f"Uploading document: {file.filename} ({len(content)} bytes)")
    
    try:
        rag = get_rag_service()
        result = await rag.ingest_document(file.filename, content)
        
        if not result.get("success"):
            return DocumentUploadResponse(
                success=False,
                message=result.get("error", "Unknown error during upload"),
                document=None
            )
        
        # Create document metadata
        document = DocumentMetadata(
            id=result["document_id"],
            filename=result["filename"],
            file_type=result["file_type"],
            file_size=result["file_size"],
            chunk_count=result["chunk_count"],
            uploaded_at=datetime.now()
        )
        
        return DocumentUploadResponse(
            success=True,
            message=f"Document '{file.filename}' uploaded successfully with {result['chunk_count']} chunks",
            document=document
        )
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload document: {str(e)}"
        )


@router.get("", response_model=List[dict])
@router.get("/", response_model=List[dict])
async def list_documents(
    _: bool = Depends(verify_admin_key)
):
    """
    List all documents in the knowledge base.
    
    Requires X-Admin-Key header.
    
    Returns:
        List of document metadata
    """
    try:
        rag = get_rag_service()
        documents = rag.get_documents()
        
        # Convert to frontend-friendly format
        result = []
        for doc in documents:
            result.append({
                "document_id": doc.get("id", ""),
                "filename": doc.get("filename", "Unknown"),
                "file_type": doc.get("file_type", "unknown"),
                "file_size": doc.get("file_size", 0),
                "chunk_count": doc.get("chunk_count", 0),
                "uploaded_at": doc.get("uploaded_at", datetime.now().isoformat())
            })
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to list documents"
        )


@router.delete("/{document_id}", response_model=DocumentDeleteResponse)
async def delete_document(
    document_id: str,
    _: bool = Depends(verify_admin_key)
) -> DocumentDeleteResponse:
    """
    Delete a document from the knowledge base.
    
    Requires X-Admin-Key header.
    
    Args:
        document_id: The document ID to delete
        
    Returns:
        DocumentDeleteResponse with deletion status
    """
    logger.info(f"Deleting document: {document_id}")
    
    try:
        rag = get_rag_service()
        result = rag.delete_document(document_id)
        
        return DocumentDeleteResponse(
            success=result["success"],
            message=result["message"],
            deleted_id=result.get("deleted_id")
        )
        
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete document"
        )


@router.get("/stats", response_model=DatabaseStats)
async def get_stats(
    _: bool = Depends(verify_admin_key)
) -> DatabaseStats:
    """
    Get knowledge base statistics.
    
    Requires X-Admin-Key header.
    
    Returns:
        DatabaseStats with document and chunk counts
    """
    try:
        rag = get_rag_service()
        stats = rag.get_stats()
        
        return DatabaseStats(
            total_documents=stats.get("total_documents", 0),
            total_chunks=stats.get("total_chunks", 0),
            collection_name=stats.get("collection_name", "unknown"),
            embedding_model=stats.get("embedding_model", "unknown")
        )
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get statistics"
        )

