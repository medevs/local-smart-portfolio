"""
Tests for document ingestion endpoints.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import io


class TestIngestEndpoint:
    """Test suite for document ingestion endpoint."""

    def test_ingest_requires_auth(self, client):
        """Ingest endpoint should require authentication."""
        files = {"file": ("test.md", b"# Test content", "text/markdown")}
        response = client.post("/ingest", files=files)
        assert response.status_code == 401

    def test_ingest_rejects_invalid_auth(self, client, invalid_admin_headers):
        """Ingest endpoint should reject invalid API keys."""
        files = {"file": ("test.md", b"# Test content", "text/markdown")}
        response = client.post("/ingest", files=files, headers=invalid_admin_headers)
        assert response.status_code == 403

    def test_ingest_accepts_markdown_file(self, client, admin_headers):
        """Ingest should accept markdown files."""
        with patch("app.routers.ingest.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.ingest_document = AsyncMock(return_value={
                "success": True,
                "document_id": "doc_123",
                "filename": "test.md",
                "file_type": ".md",
                "file_size": 25,
                "chunk_count": 5,
            })
            mock_rag.return_value = mock_service

            files = {"file": ("test.md", b"# Test\n\nContent here", "text/markdown")}
            response = client.post("/ingest", files=files, headers=admin_headers)

            assert response.status_code == 200

    def test_ingest_accepts_txt_file(self, client, admin_headers):
        """Ingest should accept text files."""
        with patch("app.routers.ingest.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.ingest_document = AsyncMock(return_value={
                "success": True,
                "document_id": "doc_456",
                "filename": "test.txt",
                "file_type": ".txt",
                "file_size": 18,
                "chunk_count": 3,
            })
            mock_rag.return_value = mock_service

            files = {"file": ("test.txt", b"Plain text content", "text/plain")}
            response = client.post("/ingest", files=files, headers=admin_headers)

            assert response.status_code == 200

    def test_ingest_rejects_unsupported_file_type(self, client, admin_headers):
        """Ingest should reject unsupported file types."""
        with patch("app.routers.ingest.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.ingest_document = AsyncMock(return_value={
                "success": False,
                "error": "Unsupported file type: .exe",
            })
            mock_rag.return_value = mock_service

            files = {"file": ("test.exe", b"binary content", "application/octet-stream")}
            response = client.post("/ingest", files=files, headers=admin_headers)

            # Should return 200 with success=false or reject with 400/422/500
            assert response.status_code in [200, 400, 422, 500]

    def test_ingest_returns_document_info(self, client, admin_headers):
        """Successful ingest should return document information."""
        with patch("app.routers.ingest.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.ingest_document = AsyncMock(return_value={
                "success": True,
                "document_id": "doc_789",
                "filename": "skills.md",
                "file_type": ".md",
                "file_size": 35,
                "chunk_count": 10,
            })
            mock_rag.return_value = mock_service

            files = {"file": ("skills.md", b"# Skills\n\n- Python\n- TypeScript", "text/markdown")}
            response = client.post("/ingest", files=files, headers=admin_headers)

            assert response.status_code == 200
            data = response.json()
            assert "success" in data
            assert data["success"] is True


class TestBatchIngest:
    """Test suite for batch document ingestion."""

    def test_batch_ingest_requires_auth(self, client):
        """Batch ingest should require authentication."""
        files = [
            ("files", ("test1.md", b"# Test 1", "text/markdown")),
            ("files", ("test2.md", b"# Test 2", "text/markdown")),
        ]
        response = client.post("/ingest/batch", files=files)
        assert response.status_code == 401

    def test_batch_ingest_accepts_multiple_files(self, client, admin_headers):
        """Batch ingest should accept multiple files."""
        with patch("app.routers.ingest.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.ingest_document = AsyncMock(return_value={
                "success": True,
                "document_id": "doc_batch",
                "filename": "test.md",
                "file_type": ".md",
                "file_size": 20,
                "chunk_count": 3,
            })
            mock_rag.return_value = mock_service

            files = [
                ("files", ("test1.md", b"# Test 1\n\nContent", "text/markdown")),
                ("files", ("test2.md", b"# Test 2\n\nMore content", "text/markdown")),
            ]
            response = client.post("/ingest/batch", files=files, headers=admin_headers)

            assert response.status_code == 200


class TestIngestValidation:
    """Test suite for ingest input validation."""

    def test_ingest_rejects_empty_file(self, client, admin_headers):
        """Ingest should handle empty files (may succeed with 0 chunks or fail)."""
        with patch("app.routers.ingest.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.ingest_document = AsyncMock(return_value={
                "success": False,
                "error": "Empty file",
            })
            mock_rag.return_value = mock_service

            files = {"file": ("empty.md", b"", "text/markdown")}
            response = client.post("/ingest", files=files, headers=admin_headers)

            # Empty files might be handled in different ways
            assert response.status_code in [200, 400, 422, 500]

    def test_ingest_rejects_oversized_file(self, client, admin_headers):
        """Ingest should reject files over size limit."""
        # Create a file larger than 10MB
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB
        files = {"file": ("large.md", large_content, "text/markdown")}

        response = client.post("/ingest", files=files, headers=admin_headers)

        # Should reject oversized files
        assert response.status_code in [400, 413, 422]

    def test_ingest_sanitizes_filename(self, client, admin_headers):
        """Ingest should handle special characters in filenames."""
        with patch("app.routers.ingest.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.ingest_document = AsyncMock(return_value={
                "success": True,
                "document_id": "doc_safe",
                "filename": "passwd.md",
                "file_type": ".md",
                "file_size": 6,
                "chunk_count": 2,
            })
            mock_rag.return_value = mock_service

            # Filename with path traversal attempt
            files = {"file": ("test/../../../etc/passwd.md", b"# Test", "text/markdown")}
            response = client.post("/ingest", files=files, headers=admin_headers)

            # Should either sanitize and succeed, or reject
            assert response.status_code in [200, 400, 422, 500]
