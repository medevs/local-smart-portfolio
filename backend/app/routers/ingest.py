"""
Document ingestion endpoint.
Handles file upload and processing into the knowledge base.
Protected by admin API key authentication.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.models.document import DocumentUploadResponse, DocumentMetadata
from app.services.ingestion.orchestrator import IngestionOrchestrator
from app.config import get_settings
from app.utils.logger import logger
from app.utils.auth import verify_admin_key
from datetime import datetime
import os
import shutil
import tempfile

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("", response_model=DocumentUploadResponse)
@router.post("/", response_model=DocumentUploadResponse)
async def ingest_document(
    file: UploadFile = File(..., description="Document file to ingest"),
    _: bool = Depends(verify_admin_key),
) -> DocumentUploadResponse:
    """
    Upload and ingest a document using the Agentic RAG pipeline (Docling + Postgres + Chroma).
    """
    settings = get_settings()

    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # Save to temp file because Docling needs a path
    tmp_path = None
    try:
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        logger.info(f"Ingesting document: {file.filename} via Docling")

        # Orchestrate ingestion (manages its own db session)
        # Pass original filename to preserve it in metadata
        orchestrator = IngestionOrchestrator()
        result = await orchestrator.ingest_file(tmp_path, original_filename=file.filename)

        # Cleanup temp file
        os.unlink(tmp_path)

        # Create response
        document = DocumentMetadata(
            id=result["document_id"],
            filename=file.filename,
            file_type=suffix,
            file_size=0,
            chunk_count=result["chunks"],
            uploaded_at=datetime.utcnow()
        )

        return DocumentUploadResponse(
            success=True,
            message=f"Document '{file.filename}' ingested successfully with {result['chunks']} chunks",
            document=document
        )

    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest document: {str(e)}"
        )


@router.post("/batch")
async def ingest_batch(
    files: list[UploadFile] = File(..., description="Multiple document files"),
    _: bool = Depends(verify_admin_key),
):
    """
    Upload and ingest multiple documents at once using Agentic RAG pipeline.
    """
    results = []
    orchestrator = IngestionOrchestrator()

    for file in files:
        tmp_path = None
        try:
            suffix = os.path.splitext(file.filename)[1] if file.filename else ""
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = tmp.name

            result = await orchestrator.ingest_file(tmp_path, original_filename=file.filename)

            results.append({
                "filename": file.filename,
                "success": True,
                "message": "Ingested successfully",
                "chunk_count": result["chunks"]
            })

        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "message": str(e),
                "chunk_count": 0
            })
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    successful = sum(1 for r in results if r["success"])

    return {
        "total": len(files),
        "successful": successful,
        "failed": len(files) - successful,
        "results": results
    }

