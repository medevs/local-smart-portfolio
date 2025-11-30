"""
System metrics collection service.
Collects real-time system metrics using psutil.
"""

import psutil
import time
import httpx
from typing import Dict, Optional
from datetime import datetime, timedelta
from app.utils.logger import logger
from app.services.ollama_client import get_ollama_client

# Cache for metrics (30 second TTL)
_metrics_cache: Optional[Dict] = None
_cache_timestamp: Optional[datetime] = None
CACHE_TTL_SECONDS = 30


async def get_system_metrics() -> Dict:
    """
    Get current system metrics.
    Uses caching to avoid excessive system calls.
    
    Returns:
        Dictionary with system metrics
    """
    global _metrics_cache, _cache_timestamp
    
    # Check cache
    if _metrics_cache and _cache_timestamp:
        age = (datetime.now() - _cache_timestamp).total_seconds()
        if age < CACHE_TTL_SECONDS:
            return _metrics_cache
    
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        ram_usage_gb = memory.used / (1024 ** 3)
        ram_usage_percent = memory.percent
        ram_total_gb = memory.total / (1024 ** 3)
        
        # System uptime
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime_delta = datetime.now() - boot_time
        uptime_days = uptime_delta.days
        uptime_hours = uptime_delta.seconds // 3600
        uptime_total_hours = uptime_days * 24 + uptime_hours
        
        # Calculate uptime percentage (assuming 30 days = 100%)
        # This is a simple calculation - you can adjust based on your needs
        uptime_percent = min(99.9, (uptime_total_hours / (30 * 24)) * 100) if uptime_total_hours > 0 else 0
        
        # Disk usage (root partition)
        try:
            disk = psutil.disk_usage('/')
            disk_usage_percent = disk.percent
            disk_free_gb = disk.free / (1024 ** 3)
        except Exception:
            disk_usage_percent = 0
            disk_free_gb = 0
        
        # Measure Ollama model latency (quick health check)
        model_latency_ms = 0.0
        try:
            ollama = get_ollama_client()
            if await ollama.check_connection():
                # Quick latency test
                start = time.time()
                timeout = httpx.Timeout(5.0, connect=2.0)
                async with httpx.AsyncClient(timeout=timeout) as client:
                    await client.get(f"{ollama.base_url}/api/tags")
                model_latency_ms = round((time.time() - start) * 1000, 1)
        except Exception as e:
            logger.debug(f"Could not measure Ollama latency: {e}")
            model_latency_ms = 0.0
        
        metrics = {
            "cpu_usage": round(cpu_percent, 1),
            "ram_usage_gb": round(ram_usage_gb, 2),
            "ram_usage_percent": round(ram_usage_percent, 1),
            "ram_total_gb": round(ram_total_gb, 2),
            "uptime_days": uptime_days,
            "uptime_hours": uptime_total_hours,
            "uptime_percent": round(uptime_percent, 1),
            "disk_usage_percent": round(disk_usage_percent, 1),
            "disk_free_gb": round(disk_free_gb, 2),
            "model_latency_ms": model_latency_ms,
            "timestamp": datetime.now().isoformat()
        }
        
        # Update cache
        _metrics_cache = metrics
        _cache_timestamp = datetime.now()
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error collecting system metrics: {e}")
        # Return default values on error
        return {
            "cpu_usage": 0.0,
            "ram_usage_gb": 0.0,
            "ram_usage_percent": 0.0,
            "ram_total_gb": 0.0,
            "uptime_days": 0,
            "uptime_hours": 0,
            "uptime_percent": 0.0,
            "disk_usage_percent": 0.0,
            "disk_free_gb": 0.0,
            "model_latency_ms": 0.0,
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

