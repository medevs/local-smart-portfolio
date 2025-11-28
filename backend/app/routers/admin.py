"""
Admin endpoints for document management and system operations.
Protected by API key authentication.
"""

from fastapi import APIRouter, HTTPException, Depends
from app.models.document import DocumentListResponse, DocumentMetadata, DocumentDeleteResponse
from app.models.response import DatabaseStats, APIResponse
from app.services.rag import get_rag_service
from app.services.chroma_client import get_chroma_service
from app.utils.logger import logger
from app.utils.auth import verify_admin_key
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents(
    _: bool = Depends(verify_admin_key)
) -> DocumentListResponse:
    """
    List all documents in the knowledge base.
    
    Requires X-Admin-Key header.
    
    Returns:
        DocumentListResponse with all document metadata
    """
    try:
        rag = get_rag_service()
        documents = rag.get_documents()
        
        # Convert to DocumentMetadata
        doc_list = []
        total_chunks = 0
        
        for doc in documents:
            doc_list.append(DocumentMetadata(
                id=doc["id"],
                filename=doc["filename"],
                file_type=doc["file_type"],
                file_size=doc.get("file_size", 0),
                chunk_count=doc.get("chunk_count", 0),
                uploaded_at=datetime.fromisoformat(doc["uploaded_at"]) if doc.get("uploaded_at") else datetime.now()
            ))
            total_chunks += doc.get("chunk_count", 0)
        
        return DocumentListResponse(
            documents=doc_list,
            total_count=len(doc_list),
            total_chunks=total_chunks
        )
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to list documents"
        )


@router.delete("/documents/{document_id}", response_model=DocumentDeleteResponse)
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


@router.post("/reset", response_model=APIResponse)
async def reset_database(
    _: bool = Depends(verify_admin_key)
) -> APIResponse:
    """
    Reset the entire knowledge base.
    WARNING: This will delete all documents and chunks!
    
    Requires X-Admin-Key header.
    
    Returns:
        APIResponse with reset status
    """
    logger.warning("Resetting knowledge base!")
    
    try:
        chroma = get_chroma_service()
        success = chroma.reset_collection()
        
        if success:
            return APIResponse(
                success=True,
                message="Knowledge base reset successfully",
                data=None
            )
        else:
            return APIResponse(
                success=False,
                message="Failed to reset knowledge base",
                data=None
            )
            
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to reset knowledge base"
        )

