"""
Tests for admin and protected endpoints.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestAdminAuthentication:
    """Test suite for admin authentication."""

    def test_admin_endpoint_requires_api_key(self, client):
        """Admin endpoints should require X-Admin-Key header."""
        response = client.get("/admin/stats")
        assert response.status_code == 401

    def test_admin_endpoint_rejects_invalid_key(self, client, invalid_admin_headers):
        """Admin endpoints should reject invalid API keys."""
        response = client.get("/admin/stats", headers=invalid_admin_headers)
        assert response.status_code == 403

    def test_admin_endpoint_accepts_valid_key(self, client, admin_headers):
        """Admin endpoints should accept valid API keys."""
        with patch("app.routers.admin.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.get_stats.return_value = {
                "total_documents": 5,
                "total_chunks": 50,
                "embedding_model": "nomic-embed-text"
            }
            mock_rag.return_value = mock_service

            response = client.get("/admin/stats", headers=admin_headers)
            assert response.status_code == 200

    def test_admin_key_too_short_is_rejected(self, client):
        """API keys shorter than 16 characters should be rejected."""
        response = client.get(
            "/admin/stats",
            headers={"X-Admin-Key": "short"}
        )
        assert response.status_code == 403


class TestAdminStats:
    """Test suite for admin stats endpoint."""

    def test_admin_stats_returns_document_count(self, client, admin_headers):
        """Admin stats should return document count."""
        with patch("app.routers.admin.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.get_stats.return_value = {
                "total_documents": 10,
                "total_chunks": 100,
                "embedding_model": "nomic-embed-text"
            }
            mock_rag.return_value = mock_service

            response = client.get("/admin/stats", headers=admin_headers)
            data = response.json()

            assert "total_documents" in data
            assert "total_chunks" in data

    def test_admin_stats_returns_embedding_model(self, client, admin_headers):
        """Admin stats should return embedding model info."""
        with patch("app.routers.admin.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.get_stats.return_value = {
                "total_documents": 5,
                "total_chunks": 50,
                "embedding_model": "nomic-embed-text"
            }
            mock_rag.return_value = mock_service

            response = client.get("/admin/stats", headers=admin_headers)
            data = response.json()

            assert "embedding_model" in data


class TestAdminDocuments:
    """Test suite for admin document management."""

    def test_admin_documents_list_requires_auth(self, client):
        """Document list endpoint should require authentication."""
        response = client.get("/admin/documents")
        assert response.status_code == 401

    def test_admin_documents_list_returns_documents(self, client, admin_headers):
        """Document list should return list of documents."""
        with patch("app.routers.admin.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.get_documents.return_value = [
                {
                    "id": "doc_123",
                    "filename": "skills.md",
                    "file_type": ".md",
                    "file_size": 1024,
                    "chunk_count": 5,
                    "uploaded_at": "2024-01-01T00:00:00"
                }
            ]
            mock_rag.return_value = mock_service

            response = client.get("/admin/documents", headers=admin_headers)
            assert response.status_code == 200
            data = response.json()
            assert "documents" in data

    def test_admin_document_delete_requires_auth(self, client):
        """Document delete endpoint should require authentication."""
        response = client.delete("/admin/documents/doc_123")
        assert response.status_code == 401

    def test_admin_document_delete_with_valid_auth(self, client, admin_headers):
        """Document delete should work with valid auth."""
        with patch("app.routers.admin.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.delete_document.return_value = {
                "success": True,
                "message": "Document deleted"
            }
            mock_rag.return_value = mock_service

            response = client.delete(
                "/admin/documents/doc_123",
                headers=admin_headers
            )
            # Should either succeed or return 404 if document doesn't exist
            assert response.status_code in [200, 404]


class TestAdminReset:
    """Test suite for admin reset endpoint."""

    def test_admin_reset_requires_auth(self, client):
        """Reset endpoint should require authentication."""
        response = client.post("/admin/reset")
        assert response.status_code == 401

    def test_admin_reset_with_valid_auth(self, client, admin_headers):
        """Reset endpoint should work with valid auth."""
        with patch("app.routers.admin.get_chroma_service") as mock_chroma:
            mock_service = MagicMock()
            mock_service.reset_collection.return_value = True
            mock_chroma.return_value = mock_service

            response = client.post("/admin/reset", headers=admin_headers)
            assert response.status_code == 200


class TestDocumentsEndpoint:
    """Test suite for documents endpoints."""

    def test_documents_list_requires_auth(self, client):
        """Documents list should require authentication."""
        response = client.get("/documents")
        assert response.status_code == 401

    def test_documents_stats_requires_auth(self, client):
        """Documents stats should require authentication."""
        response = client.get("/documents/stats")
        assert response.status_code == 401
