from typing import List, Dict, Any, Optional
import uuid
import os
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Document, UploadedFile
from app.db.database import AsyncSessionLocal
from app.services.ingestion.docling_service import DoclingIngestionService
from app.services.chroma_client import get_chroma_client
from app.config import get_settings
from app.utils.logger import logger


class IngestionOrchestrator:
    """
    Orchestrates document ingestion:
    Docling -> Postgres (keyword search) + ChromaDB (semantic search)
    """

    def __init__(self):
        settings = get_settings()
        # Use Docling if enabled in config (USE_DOCLING=true)
        self.docling = DoclingIngestionService(use_docling=settings.use_docling)
        self.chroma = get_chroma_client()

    async def ingest_file(self, file_path: str, original_filename: str = None) -> Dict[str, Any]:
        """
        Orchestrates the ingestion process:
        1. Track file in UploadedFiles
        2. Extract chunks via Docling
        3. Save chunks to Postgres (Documents table) with TSVECTOR
        4. Save chunks to ChromaDB with metadata

        Args:
            file_path: Path to the file (may be temp file)
            original_filename: Original filename from upload (preserves actual name)
        """
        # Use original filename if provided, otherwise extract from path
        filename = original_filename or os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        async with AsyncSessionLocal() as db:
            # 1. Create UploadedFile record
            upload_record = UploadedFile(
                filename=filename,
                file_type=os.path.splitext(filename)[1],
                file_size=file_size,
                status="processing"
            )
            db.add(upload_record)
            await db.commit()
            await db.refresh(upload_record)

            try:
                # 2. Extract chunks (sync operation)
                logger.info(f"Starting Docling extraction for {filename}")
                chunks = self.docling.process_document(file_path, original_filename=filename)
                logger.info(f"Extracted {len(chunks)} chunks")

                if not chunks:
                    raise ValueError("No chunks extracted from document")

                # Prepare data lists
                pg_documents = []
                chroma_texts = []
                chroma_metadatas = []
                chroma_ids = []

                for i, chunk in enumerate(chunks):
                    chunk_id = str(uuid.uuid4())
                    content = chunk["text"]
                    source = chunk["metadata"]["source"]

                    # Metadata for Chroma (Strictly following rag.txt)
                    metadata = {
                        "chunk_id": chunk_id,
                        "document_id": str(upload_record.id),
                        "source": source,
                        "position": i
                    }

                    # Postgres Document (Chunk)
                    pg_doc = Document(
                        id=uuid.UUID(chunk_id),
                        title=filename,
                        source=source,
                        content=content,
                    )

                    pg_documents.append(pg_doc)
                    chroma_texts.append(content)
                    chroma_metadatas.append(metadata)
                    chroma_ids.append(chunk_id)

                # 3. Save to Postgres with TSVECTOR
                db.add_all(pg_documents)
                await db.commit()

                # Update TSVECTOR for keyword search
                tsvector_count = 0
                for doc in pg_documents:
                    try:
                        await db.execute(
                            Document.__table__.update().
                            where(Document.id == doc.id).
                            values(tsv=func.to_tsvector('english', doc.content))
                        )
                        tsvector_count += 1
                    except Exception as e:
                        logger.warning(f"[INGEST] TSVECTOR failed for chunk {doc.id}: {e}")
                await db.commit()
                logger.info(f"[INGEST] TSVECTOR indexed {tsvector_count}/{len(pg_documents)} chunks")

                # 4. Save to Chroma
                self.chroma.add_documents(
                    texts=chroma_texts,
                    metadatas=chroma_metadatas,
                    ids=chroma_ids
                )

                # Update UploadedFile status
                upload_record.status = "completed"
                upload_record.chunk_count = len(chunks)
                upload_record.processed_at = datetime.utcnow()
                await db.commit()

                logger.info(f"Ingestion complete for {filename}: {len(chunks)} chunks")
                return {"status": "success", "chunks": len(chunks), "document_id": str(upload_record.id)}

            except Exception as e:
                logger.error(f"Ingestion failed: {e}")
                upload_record.status = "failed"
                upload_record.error_message = str(e)
                await db.commit()
                raise e
