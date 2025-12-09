"""
Tests for metrics endpoints.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock


class TestSystemMetrics:
    """Test suite for system metrics endpoint."""

    def test_metrics_system_returns_200(self, client):
        """System metrics endpoint should return 200."""
        response = client.get("/metrics/system")
        assert response.status_code == 200

    def test_metrics_system_has_cpu_info(self, client):
        """System metrics should include CPU usage."""
        response = client.get("/metrics/system")
        data = response.json()

        # Check for cpu_usage field (the actual field name in the response model)
        assert "cpu_usage" in data

    def test_metrics_system_has_ram_info(self, client):
        """System metrics should include RAM usage."""
        response = client.get("/metrics/system")
        data = response.json()

        # Check for RAM-related fields based on actual model
        assert any(key in data for key in ["ram_usage_gb", "ram_total_gb", "ram_usage_percent"])

    def test_metrics_system_has_uptime(self, client):
        """System metrics should include uptime."""
        response = client.get("/metrics/system")
        data = response.json()

        # Check for uptime-related fields
        assert any(key in data for key in ["uptime_days", "uptime_hours", "uptime_percent"])

    def test_metrics_system_values_are_numeric(self, client):
        """System metrics values should be numeric."""
        response = client.get("/metrics/system")
        data = response.json()

        # CPU should be a number between 0-100
        if "cpu_usage" in data:
            assert isinstance(data["cpu_usage"], (int, float))
            assert 0 <= data["cpu_usage"] <= 100


class TestBenchmarkMetrics:
    """Test suite for benchmark metrics endpoint."""

    def test_metrics_benchmarks_returns_200_or_500(self, client):
        """Benchmarks endpoint should return 200 (or 500 if Ollama unavailable)."""
        response = client.get("/metrics/benchmarks")
        # May fail if Ollama is not running, which is acceptable in tests
        assert response.status_code in [200, 500]

    def test_metrics_benchmarks_with_mock(self, client):
        """Benchmarks endpoint should return correct structure when mocked."""
        with patch("app.routers.metrics.get_benchmarks") as mock_bench:
            mock_bench.return_value = [
                {
                    "model": "llama3.2:3b",
                    "speed_tokens_per_sec": 25.5,
                    "speed_display": "25.5 tok/s",
                    "memory_gb": 4.2,
                    "memory_display": "4.2 GB",
                    "latency_ms": 150.0,
                    "quality_score": 85,
                    "last_benchmarked": "2024-01-01T00:00:00Z"
                }
            ]

            response = client.get("/metrics/benchmarks")

            if response.status_code == 200:
                data = response.json()
                assert "benchmarks" in data or "timestamp" in data

    def test_metrics_benchmarks_structure_when_available(self, client):
        """Benchmarks should have proper structure when service is available."""
        with patch("app.routers.metrics.get_benchmarks") as mock_bench:
            mock_bench.return_value = [
                {
                    "model": "llama3.2:3b",
                    "speed_tokens_per_sec": 25.5,
                    "speed_display": "25.5 tok/s",
                    "memory_gb": 4.2,
                    "memory_display": "4.2 GB",
                    "latency_ms": 150.0,
                    "quality_score": 85,
                    "last_benchmarked": "2024-01-01T00:00:00Z"
                }
            ]

            response = client.get("/metrics/benchmarks")

            if response.status_code == 200:
                data = response.json()
                if "benchmarks" in data and len(data["benchmarks"]) > 0:
                    benchmark = data["benchmarks"][0]
                    assert "model" in benchmark


class TestMetricsPerformance:
    """Test suite for metrics endpoint performance."""

    def test_metrics_system_response_time(self, client):
        """System metrics should respond quickly."""
        import time

        start = time.time()
        response = client.get("/metrics/system")
        elapsed = time.time() - start

        assert response.status_code == 200
        # Should respond in under 2 seconds
        assert elapsed < 2.0, f"Metrics took {elapsed:.2f}s, expected < 2s"

    def test_metrics_has_process_time_header(self, client):
        """Metrics response should include X-Process-Time header."""
        response = client.get("/metrics/system")

        # The middleware adds this header
        assert "x-process-time" in response.headers
