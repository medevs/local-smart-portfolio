"""
Pytest configuration and fixtures for backend tests.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import os
import sys

# Add the backend app to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set test environment variables before importing app
os.environ["ADMIN_API_KEY"] = "test-admin-key-for-testing-1234"
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
os.environ["DEBUG"] = "true"


@pytest.fixture(scope="session")
def test_settings():
    """Test settings with valid admin key."""
    return {
        "admin_api_key": "test-admin-key-for-testing-1234",
        "ollama_base_url": "http://localhost:11434",
        "ollama_model": "llama3.2:3b",
    }


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def admin_headers():
    """Headers with valid admin API key."""
    return {"X-Admin-Key": "test-admin-key-for-testing-1234"}


@pytest.fixture
def invalid_admin_headers():
    """Headers with invalid admin API key."""
    return {"X-Admin-Key": "invalid-key"}


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client for testing without actual LLM."""
    with patch("app.services.ollama_client.OllamaClient") as mock:
        instance = mock.return_value
        instance.check_connection = MagicMock(return_value=True)
        instance.generate = AsyncMock(return_value="This is a test response about Ahmed's skills.")
        instance.generate_stream = AsyncMock()
        yield instance


@pytest.fixture
def mock_chroma_client():
    """Mock ChromaDB client for testing without actual database."""
    with patch("app.services.chroma_client.ChromaService") as mock:
        instance = mock.return_value
        instance.check_connection = MagicMock(return_value=True)
        instance.query = MagicMock(return_value={
            "documents": [["Test document content"]],
            "metadatas": [[{"source": "test.md"}]],
            "distances": [[0.5]]
        })
        instance.get_stats = MagicMock(return_value={
            "total_chunks": 10,
            "total_documents": 2,
            "collection_name": "portfolio_docs"
        })
        instance.get_all_documents = MagicMock(return_value=[])
        yield instance


@pytest.fixture
def mock_rag_service():
    """Mock RAG service for testing."""
    with patch("app.services.rag.RAGService") as mock:
        instance = mock.return_value
        instance.query = AsyncMock(return_value={
            "response": "Test response about Ahmed's portfolio.",
            "sources": ["test.md"]
        })

        async def mock_stream():
            yield {"chunk": "Test ", "done": False, "sources": None}
            yield {"chunk": "response.", "done": False, "sources": None}
            yield {"chunk": "", "done": True, "sources": ["test.md"]}

        instance.query_stream = mock_stream
        instance.get_stats = MagicMock(return_value={
            "total_documents": 2,
            "total_chunks": 10,
            "embedding_model": "nomic-embed-text"
        })
        yield instance


@pytest.fixture
def sample_chat_request():
    """Sample chat request payload."""
    return {
        "message": "What are Ahmed's skills?",
        "history": []
    }


@pytest.fixture
def sample_chat_request_with_history():
    """Sample chat request with conversation history."""
    return {
        "message": "Tell me more about his Python experience",
        "history": [
            {"role": "user", "content": "What are Ahmed's skills?"},
            {"role": "assistant", "content": "Ahmed is skilled in Python, TypeScript, and more."}
        ]
    }


@pytest.fixture
def sample_document_content():
    """Sample document content for testing ingestion."""
    return b"""# Ahmed's Skills

## Programming Languages
- Python (Expert)
- TypeScript (Advanced)
- JavaScript (Advanced)

## Frameworks
- FastAPI
- Next.js
- React
"""


@pytest.fixture
def temp_upload_file(tmp_path, sample_document_content):
    """Create a temporary file for upload testing."""
    file_path = tmp_path / "test_document.md"
    file_path.write_bytes(sample_document_content)
    return file_path
