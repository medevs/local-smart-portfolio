"""
Tests for health check endpoints.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestHealthEndpoints:
    """Test suite for health check endpoints."""

    def test_health_endpoint_returns_200(self, client):
        """Health endpoint should return 200 status."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_has_required_fields(self, client):
        """Health response should contain required fields."""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert "version" in data
        assert "timestamp" in data
        assert "services" in data

    def test_health_ready_endpoint(self, client):
        """Readiness endpoint should return ready status."""
        response = client.get("/health/ready")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"

    def test_health_live_endpoint(self, client):
        """Liveness endpoint should return alive status."""
        response = client.get("/health/live")
        assert response.status_code == 200
        assert response.json()["status"] == "alive"

    def test_health_services_structure(self, client):
        """Health endpoint should return services status structure."""
        response = client.get("/health")
        data = response.json()

        assert "services" in data
        services = data["services"]
        assert "ollama" in services
        assert "chromadb" in services

    def test_health_with_ollama_status(self, client):
        """Health should return ollama status (connected or not)."""
        response = client.get("/health")
        data = response.json()

        # Should not fail even if services have issues
        assert response.status_code == 200
        # Ollama status should be present (either connected or disconnected)
        assert "services" in data
        assert "ollama" in data["services"]

    def test_health_degraded_still_returns_200(self, client):
        """Health should still return 200 even in degraded state."""
        response = client.get("/health")

        # Health check should still succeed (degraded state is acceptable)
        assert response.status_code == 200
        # Status might be healthy or degraded
        data = response.json()
        assert data["status"] in ["healthy", "degraded"]


class TestRootEndpoint:
    """Test suite for root endpoint."""

    def test_root_endpoint_returns_200(self, client):
        """Root endpoint should return 200 status."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_has_api_info(self, client):
        """Root endpoint should return API information."""
        response = client.get("/")
        data = response.json()

        assert "name" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data

    def test_root_endpoint_docs_path(self, client):
        """Root endpoint should point to correct docs path."""
        response = client.get("/")
        data = response.json()

        assert data["docs"] == "/docs"
        assert data["health"] == "/health"
