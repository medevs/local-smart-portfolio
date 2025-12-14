from celery import current_task
from app.tasks.celery_app import celery_app
# Import DocumentLoader here or inside function to avoid circular imports if necessary
# from app.services.document_loader import DocumentLoader
# from app.services.chroma_client import get_chroma_client

@celery_app.task(bind=True)
def process_document_async(self, file_path: str, filename: str):
    """Process document in background with progress tracking."""
    # Note: We need to import services inside the task to avoid issues with Celery worker loading
    from app.services.document_loader import DocumentLoader
    from app.services.chroma_client import get_chroma_client
    
    try:
        self.update_state(state="PROCESSING", meta={"progress": 0, "stage": "reading"})

        # Load and extract text
        loader = DocumentLoader()
        text = loader.extract_text(file_path)
        self.update_state(state="PROCESSING", meta={"progress": 30, "stage": "chunking"})

        # Chunk text
        chunks = loader.chunk_text(text)
        self.update_state(state="PROCESSING", meta={"progress": 60, "stage": "embedding"})

        # Store in ChromaDB
        chroma = get_chroma_client()
        chroma.add_documents(chunks, metadata={"source": filename})
        self.update_state(state="PROCESSING", meta={"progress": 100, "stage": "complete"})

        return {
            "status": "completed",
            "filename": filename,
            "chunks": len(chunks),
        }
    except Exception as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise
