"""
Metrics endpoints for system metrics and LLM benchmarks.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.models.response import SystemMetricsResponse, BenchmarksResponse
from app.services.metrics_service import get_system_metrics
from app.services.benchmark_service import get_benchmarks
from app.config import get_settings
from app.utils.logger import logger

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get("/system", response_model=SystemMetricsResponse)
async def get_system_metrics_endpoint() -> SystemMetricsResponse:
    """
    Get real-time system metrics from the homelab.
    
    Returns:
        SystemMetricsResponse with CPU, RAM, uptime, and disk metrics
    """
    try:
        metrics = await get_system_metrics()
        return SystemMetricsResponse(**metrics)
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get system metrics"
        )


@router.get("/benchmarks", response_model=BenchmarksResponse)
async def get_benchmarks_endpoint() -> BenchmarksResponse:
    """
    Get LLM performance benchmarks for all available models.
    
    Returns:
        BenchmarksResponse with benchmark results for each model
    """
    try:
        settings = get_settings()
        benchmarks_data = await get_benchmarks(settings.ollama_base_url)
        
        # Convert dicts to BenchmarkResult models
        from app.models.response import BenchmarkResult
        benchmarks = [
            BenchmarkResult(**benchmark) for benchmark in benchmarks_data
        ]
        
        timestamp = benchmarks[0].last_benchmarked if benchmarks else datetime.now().isoformat()
        
        return BenchmarksResponse(
            benchmarks=benchmarks,
            timestamp=timestamp
        )
    except Exception as e:
        logger.error(f"Error getting benchmarks: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get benchmarks"
        )

