"""
Document ingestion endpoint.
Handles file upload and processing into the knowledge base.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.document import DocumentUploadResponse, DocumentMetadata
from app.services.rag import get_rag_service
from app.config import get_settings
from app.utils.logger import logger
from datetime import datetime

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("", response_model=DocumentUploadResponse)
@router.post("/", response_model=DocumentUploadResponse)
async def ingest_document(
    file: UploadFile = File(..., description="Document file to ingest")
) -> DocumentUploadResponse:
    """
    Upload and ingest a document into the knowledge base.
    
    Supported file types: .pdf, .md, .txt, .docx
    
    The document will be:
    1. Validated for type and size
    2. Saved to disk
    3. Text extracted
    4. Split into chunks
    5. Embedded and stored in vector database
    
    Args:
        file: The uploaded file
        
    Returns:
        DocumentUploadResponse with document metadata
    """
    settings = get_settings()
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Read file content
    content = await file.read()
    
    if len(content) > settings.max_file_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {settings.max_file_size_mb}MB"
        )
    
    logger.info(f"Ingesting document: {file.filename} ({len(content)} bytes)")
    
    try:
        rag = get_rag_service()
        result = await rag.ingest_document(file.filename, content)
        
        if not result.get("success"):
            return DocumentUploadResponse(
                success=False,
                message=result.get("error", "Unknown error during ingestion"),
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
            message=f"Document '{file.filename}' ingested successfully with {result['chunk_count']} chunks",
            document=document
        )
        
    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest document: {str(e)}"
        )


@router.post("/batch")
async def ingest_batch(
    files: list[UploadFile] = File(..., description="Multiple document files")
):
    """
    Upload and ingest multiple documents at once.
    
    Args:
        files: List of uploaded files
        
    Returns:
        Results for each file
    """
    results = []
    
    for file in files:
        try:
            content = await file.read()
            rag = get_rag_service()
            result = await rag.ingest_document(file.filename or "unknown", content)
            results.append({
                "filename": file.filename,
                "success": result.get("success", False),
                "message": result.get("error") if not result.get("success") else "Ingested successfully",
                "chunk_count": result.get("chunk_count", 0)
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "message": str(e),
                "chunk_count": 0
            })
    
    successful = sum(1 for r in results if r["success"])
    
    return {
        "total": len(files),
        "successful": successful,
        "failed": len(files) - successful,
        "results": results
    }

