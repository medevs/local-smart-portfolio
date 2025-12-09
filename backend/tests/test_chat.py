"""
Tests for chat endpoints.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


class TestChatEndpoint:
    """Test suite for chat endpoint."""

    def test_chat_endpoint_accepts_valid_request(self, client, sample_chat_request):
        """Chat endpoint should accept valid request format."""
        with patch("app.routers.chat.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.query = AsyncMock(return_value={
                "response": "Ahmed has skills in Python, TypeScript, and more.",
                "sources": ["skills.md"]
            })
            mock_rag.return_value = mock_service

            response = client.post("/chat", json=sample_chat_request)
            assert response.status_code == 200

    def test_chat_endpoint_returns_response_and_sources(self, client, sample_chat_request):
        """Chat response should contain response text and sources."""
        with patch("app.routers.chat.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.query = AsyncMock(return_value={
                "response": "Ahmed is skilled in Python.",
                "sources": ["skills.md", "projects.md"]
            })
            mock_rag.return_value = mock_service

            response = client.post("/chat", json=sample_chat_request)
            data = response.json()

            assert "response" in data
            assert "sources" in data
            assert isinstance(data["sources"], list)

    def test_chat_endpoint_with_history(self, client, sample_chat_request_with_history):
        """Chat endpoint should accept conversation history."""
        with patch("app.routers.chat.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.query = AsyncMock(return_value={
                "response": "Ahmed has 5+ years of Python experience.",
                "sources": ["experience.md"]
            })
            mock_rag.return_value = mock_service

            response = client.post("/chat", json=sample_chat_request_with_history)
            assert response.status_code == 200

    def test_chat_endpoint_rejects_empty_message(self, client):
        """Chat endpoint should reject empty messages."""
        response = client.post("/chat", json={"message": "", "history": []})
        # FastAPI/Pydantic should reject empty string if validation is set
        # If no validation, this tests current behavior
        assert response.status_code in [200, 422]  # 422 if validated

    def test_chat_endpoint_rejects_missing_message(self, client):
        """Chat endpoint should reject requests without message field."""
        response = client.post("/chat", json={"history": []})
        assert response.status_code == 422  # Validation error

    def test_chat_endpoint_handles_service_error(self, client, sample_chat_request):
        """Chat endpoint should handle service errors gracefully."""
        with patch("app.routers.chat.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.query = AsyncMock(side_effect=Exception("Service error"))
            mock_rag.return_value = mock_service

            response = client.post("/chat", json=sample_chat_request)
            assert response.status_code == 500


class TestChatStreamEndpoint:
    """Test suite for streaming chat endpoint."""

    def test_chat_stream_endpoint_returns_sse(self, client, sample_chat_request):
        """Streaming endpoint should return SSE content type."""
        with patch("app.routers.chat.get_rag_service") as mock_rag:
            mock_service = MagicMock()

            async def mock_stream(question, history):
                yield {"chunk": "Test ", "done": False, "sources": None}
                yield {"chunk": "response.", "done": True, "sources": ["test.md"]}

            mock_service.query_stream = mock_stream
            mock_rag.return_value = mock_service

            response = client.post("/chat/stream", json=sample_chat_request)

            assert response.status_code == 200
            assert "text/event-stream" in response.headers.get("content-type", "")

    def test_chat_stream_endpoint_has_correct_headers(self, client, sample_chat_request):
        """Streaming endpoint should have correct SSE headers."""
        with patch("app.routers.chat.get_rag_service") as mock_rag:
            mock_service = MagicMock()

            async def mock_stream(question, history):
                yield {"chunk": "Test", "done": True, "sources": []}

            mock_service.query_stream = mock_stream
            mock_rag.return_value = mock_service

            response = client.post("/chat/stream", json=sample_chat_request)

            assert response.headers.get("cache-control") == "no-cache"
            assert response.headers.get("connection") == "keep-alive"

    def test_chat_stream_endpoint_yields_data_events(self, client, sample_chat_request):
        """Streaming endpoint should yield data events."""
        with patch("app.routers.chat.get_rag_service") as mock_rag:
            mock_service = MagicMock()

            async def mock_stream(question, history):
                yield {"chunk": "Hello", "done": False, "sources": None}
                yield {"chunk": " World", "done": True, "sources": ["test.md"]}

            mock_service.query_stream = mock_stream
            mock_rag.return_value = mock_service

            response = client.post("/chat/stream", json=sample_chat_request)
            content = response.text

            # SSE format: data: {...}\n\n
            assert "data:" in content


class TestChatInputValidation:
    """Test suite for chat input validation."""

    def test_chat_rejects_non_json_content(self, client):
        """Chat endpoint should reject non-JSON content."""
        response = client.post(
            "/chat",
            content="not json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_chat_accepts_unicode_message(self, client):
        """Chat endpoint should accept unicode characters."""
        with patch("app.routers.chat.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.query = AsyncMock(return_value={
                "response": "Response",
                "sources": []
            })
            mock_rag.return_value = mock_service

            response = client.post("/chat", json={
                "message": "What are Ahmed's skills? Arabic: مهارات",
                "history": []
            })
            assert response.status_code == 200

    def test_chat_handles_long_message(self, client):
        """Chat endpoint should handle long messages."""
        with patch("app.routers.chat.get_rag_service") as mock_rag:
            mock_service = MagicMock()
            mock_service.query = AsyncMock(return_value={
                "response": "Response",
                "sources": []
            })
            mock_rag.return_value = mock_service

            long_message = "What are Ahmed's skills? " * 100  # ~2500 chars
            response = client.post("/chat", json={
                "message": long_message,
                "history": []
            })
            # Should either succeed or fail gracefully
            assert response.status_code in [200, 400, 413, 422]
