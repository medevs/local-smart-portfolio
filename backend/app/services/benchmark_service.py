"""
LLM benchmark service.
Measures performance of Ollama models.
"""

import httpx
import time
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.services.ollama_client import get_ollama_client
from app.utils.logger import logger

# Cache for benchmarks (1 hour TTL)
_benchmarks_cache: Optional[Dict] = None
_cache_timestamp: Optional[datetime] = None
CACHE_TTL_SECONDS = 3600  # 1 hour

# Standard benchmark prompt
BENCHMARK_PROMPT = "Hello, how are you? Please respond with a brief greeting."


async def measure_model_latency(model_name: str, ollama_base_url: str) -> float:
    """
    Measure model latency by sending a simple request.
    
    Args:
        model_name: Name of the model to benchmark
        ollama_base_url: Base URL of Ollama service
        
    Returns:
        Latency in milliseconds
    """
    try:
        timeout = httpx.Timeout(30.0, connect=10.0)
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{ollama_base_url}/api/chat",
                json={
                    "model": model_name,
                    "messages": [
                        {"role": "user", "content": BENCHMARK_PROMPT}
                    ],
                    "stream": False,
                    "options": {
                        "num_predict": 20,  # Short response for speed test
                    }
                }
            )
            
            if response.status_code == 200:
                elapsed = (time.time() - start_time) * 1000  # Convert to ms
                return round(elapsed, 1)
            else:
                logger.warning(f"Failed to measure latency for {model_name}: {response.status_code}")
                return 0.0
                
    except Exception as e:
        logger.error(f"Error measuring latency for {model_name}: {e}")
        return 0.0


async def measure_model_speed(model_name: str, ollama_base_url: str) -> float:
    """
    Measure tokens per second for a model.
    
    Args:
        model_name: Name of the model to benchmark
        ollama_base_url: Base URL of Ollama service
        
    Returns:
        Tokens per second
    """
    try:
        timeout = httpx.Timeout(60.0, connect=10.0)
        start_time = time.time()
        tokens_generated = 0
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream(
                "POST",
                f"{ollama_base_url}/api/chat",
                json={
                    "model": model_name,
                    "messages": [
                        {"role": "user", "content": BENCHMARK_PROMPT}
                    ],
                    "stream": True,
                    "options": {
                        "num_predict": 100,  # Generate ~100 tokens
                    }
                }
            ) as response:
                if response.status_code != 200:
                    return 0.0
                
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            chunk = data.get("message", {}).get("content", "")
                            if chunk:
                                # Rough token estimation (1 token ≈ 4 characters)
                                tokens_generated += len(chunk) / 4
                            
                            if data.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue
                
                elapsed = time.time() - start_time
                if elapsed > 0:
                    tokens_per_sec = tokens_generated / elapsed
                    return round(tokens_per_sec, 1)
                return 0.0
                
    except Exception as e:
        logger.error(f"Error measuring speed for {model_name}: {e}")
        return 0.0


async def get_model_memory_usage(model_name: str, ollama_base_url: str) -> float:
    """
    Get memory usage for a model from Ollama API.
    
    Args:
        model_name: Name of the model
        ollama_base_url: Base URL of Ollama service
        
    Returns:
        Memory usage in GB
    """
    try:
        timeout = httpx.Timeout(10.0, connect=5.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            # Try to get model info from Ollama
            response = await client.post(
                f"{ollama_base_url}/api/show",
                json={"name": model_name}
            )
            
            if response.status_code == 200:
                data = response.json()
                # Ollama returns size in bytes - check multiple possible fields
                size_bytes = data.get("size", 0) or data.get("model_size", 0) or data.get("file_size", 0)
                
                # Also check modelfile for size info
                if size_bytes == 0:
                    modelfile = data.get("modelfile", "")
                    # Try to extract size from modelfile or use model details
                    model_details = data.get("details", {})
                    if model_details:
                        size_bytes = model_details.get("size", 0) or model_details.get("model_size", 0)
                
                if size_bytes > 0:
                    size_gb = size_bytes / (1024 ** 3)
                    return round(size_gb, 2)
            
            # Fallback: estimate based on model name (more accurate)
            model_lower = model_name.lower()
            if "8b" in model_lower or ":8b" in model_lower:
                return 4.5  # Quantized 8B models are ~4.5GB
            elif "7b" in model_lower or ":7b" in model_lower:
                return 4.0  # Quantized 7B models are ~4GB
            elif "3.8b" in model_lower or "3.8" in model_lower:
                return 2.3  # Phi-3.8B quantized
            elif "3b" in model_lower or ":3b" in model_lower:
                return 2.0  # Quantized 3B models are ~2GB
            elif "tiny" in model_lower:
                return 0.6  # TinyLlama is ~600MB
            else:
                return 2.0  # Default estimate
                    
    except Exception as e:
        logger.debug(f"Error getting memory usage for {model_name}: {e}")
        # Fallback estimation based on model name
        model_lower = model_name.lower()
        if "8b" in model_lower or ":8b" in model_lower:
            return 4.5
        elif "7b" in model_lower or ":7b" in model_lower:
            return 4.0
        elif "3.8b" in model_lower or "3.8" in model_lower:
            return 2.3
        elif "3b" in model_lower or ":3b" in model_lower:
            return 2.0
        elif "tiny" in model_lower:
            return 0.6
        return 2.0


def calculate_quality_score(model_name: str, speed: float, memory: float) -> int:
    """
    Calculate a quality score based on model characteristics.
    This is a simple heuristic - you can improve this.
    
    Args:
        model_name: Name of the model
        speed: Tokens per second
        memory: Memory usage in GB
        
    Returns:
        Quality score (0-100)
    """
    model_lower = model_name.lower()
    
    # Base score from model size and type (larger models generally better)
    if "deepseek" in model_lower:
        base_score = 90  # DeepSeek models are high quality
    elif "phi3" in model_lower or "phi-3" in model_lower:
        base_score = 94  # Phi-3 models are excellent
    elif "qwen" in model_lower:
        base_score = 88  # Qwen models are good
    elif "8b" in model_lower or ":8b" in model_lower:
        base_score = 92
    elif "7b" in model_lower or ":7b" in model_lower:
        base_score = 88
    elif "3.8b" in model_lower or "3.8" in model_lower:
        base_score = 94  # Phi-3.8B is excellent
    elif "3b" in model_lower or ":3b" in model_lower:
        base_score = 87
    elif "tiny" in model_lower:
        base_score = 82  # TinyLlama is smaller but decent
    else:
        base_score = 80
    
    # Adjust based on speed (faster is better, but not the only factor)
    if speed > 50:
        speed_bonus = 3
    elif speed > 20:
        speed_bonus = 2
    elif speed > 5:
        speed_bonus = 1
    else:
        speed_bonus = 0
    
    # Adjust based on memory efficiency (lower memory is better for same quality)
    if memory < 2:
        memory_bonus = 2
    elif memory < 4:
        memory_bonus = 1
    else:
        memory_bonus = 0
    
    final_score = min(100, base_score + speed_bonus + memory_bonus)
    return int(final_score)


async def get_benchmarks(ollama_base_url: str) -> List[Dict]:
    """
    Get benchmarks for all available Ollama models.
    Uses caching to avoid expensive benchmark runs.
    
    Args:
        ollama_base_url: Base URL of Ollama service
        
    Returns:
        List of benchmark results
    """
    global _benchmarks_cache, _cache_timestamp
    
    # Check cache
    if _benchmarks_cache and _cache_timestamp:
        age = (datetime.now() - _cache_timestamp).total_seconds()
        if age < CACHE_TTL_SECONDS:
            return _benchmarks_cache.get("benchmarks", [])
    
    try:
        # Get list of available models
        timeout = httpx.Timeout(10.0, connect=5.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(f"{ollama_base_url}/api/tags")
            
            if response.status_code != 200:
                logger.warning("Failed to get model list from Ollama")
                return []
            
            data = response.json()
            models = [model["name"] for model in data.get("models", [])]
            
            if not models:
                logger.warning("No models found in Ollama")
                return []
        
        # Benchmark each model
        benchmarks = []
        for model_name in models:
            try:
                logger.info(f"Benchmarking model: {model_name}")
                
                # Measure speed
                speed = await measure_model_speed(model_name, ollama_base_url)
                
                # Get memory usage
                memory = await get_model_memory_usage(model_name, ollama_base_url)
                
                # Measure latency
                latency = await measure_model_latency(model_name, ollama_base_url)
                
                # Calculate quality score
                quality = calculate_quality_score(model_name, speed, memory)
                
                benchmarks.append({
                    "model": model_name,
                    "speed_tokens_per_sec": speed,
                    "speed_display": f"{speed} tok/s" if speed > 0 else "N/A",
                    "memory_gb": memory,
                    "memory_display": f"{memory}GB",
                    "latency_ms": latency,
                    "quality_score": quality,
                    "last_benchmarked": datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Error benchmarking model {model_name}: {e}")
                continue
        
        # Update cache
        _benchmarks_cache = {
            "benchmarks": benchmarks,
            "timestamp": datetime.now().isoformat()
        }
        _cache_timestamp = datetime.now()
        
        return benchmarks
        
    except Exception as e:
        logger.error(f"Error getting benchmarks: {e}")
        return []

