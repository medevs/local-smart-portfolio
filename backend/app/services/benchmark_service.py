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
    Uses actual token count from Ollama response for accuracy.
    
    Args:
        model_name: Name of the model to benchmark
        ollama_base_url: Base URL of Ollama service
        
    Returns:
        Tokens per second, or 0.0 if failed/timeout
    """
    try:
        # Longer timeout for larger models
        timeout = httpx.Timeout(120.0, connect=10.0)
        start_time = time.time()
        tokens_generated = 0
        actual_tokens = 0
        
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
                        "num_predict": 50,  # Reduced for faster benchmark
                    }
                }
            ) as response:
                if response.status_code != 200:
                    logger.warning(f"Speed test failed for {model_name}: {response.status_code}")
                    return 0.0
                
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            
                            # Use actual token count if available (more accurate)
                            if "eval_count" in data:
                                actual_tokens = data.get("eval_count", 0)
                            
                            chunk = data.get("message", {}).get("content", "")
                            if chunk:
                                # Fallback: estimate tokens (1 token ≈ 4 characters)
                                tokens_generated += len(chunk) / 4
                            
                            if data.get("done", False):
                                # Use actual token count if we have it
                                if actual_tokens > 0:
                                    tokens_generated = actual_tokens
                                break
                        except json.JSONDecodeError:
                            continue
                
                elapsed = time.time() - start_time
                if elapsed > 0 and tokens_generated > 0:
                    tokens_per_sec = tokens_generated / elapsed
                    return round(tokens_per_sec, 1)
                return 0.0
                
    except httpx.TimeoutException:
        logger.warning(f"Speed test timeout for {model_name}")
        return 0.0
    except Exception as e:
        logger.error(f"Error measuring speed for {model_name}: {e}")
        return 0.0


async def get_model_memory_usage(model_name: str, ollama_base_url: str) -> float:
    """
    Get memory usage for a model from Ollama API.
    Uses actual file size from disk or parameter count for accuracy.
    
    Args:
        model_name: Name of the model
        ollama_base_url: Base URL of Ollama service
        
    Returns:
        Memory usage in GB
    """
    try:
        timeout = httpx.Timeout(10.0, connect=5.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            # Get model info from Ollama
            response = await client.post(
                f"{ollama_base_url}/api/show",
                json={"name": model_name}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Method 1: Calculate from parameter count and quantization (most accurate)
                model_info = data.get("model_info", {})
                if model_info:
                    param_count = model_info.get("general.parameter_count", 0)
                    if param_count > 0:
                        # Get quantization level from details
                        details = data.get("details", {})
                        quant_level = details.get("quantization_level", "Q4_K_M")
                        
                        # Calculate size based on quantization bits per parameter
                        bits_per_param = {
                            "Q2_K": 2.2, "Q3_K_M": 3.2, "Q3_K_S": 3.1,
                            "Q4_K_M": 4.5, "Q4_K_S": 4.3, "Q4_0": 4.0,
                            "Q5_K_M": 5.4, "Q5_K_S": 5.2, "Q5_0": 5.0,
                            "Q6_K": 6.2, "Q8_0": 8.0,
                            "F16": 16.0, "F32": 32.0
                        }
                        
                        bits = bits_per_param.get(quant_level, 4.5)  # Default Q4_K_M
                        size_bytes = (param_count * bits) / 8
                        size_gb = size_bytes / (1024 ** 3)
                        return round(size_gb, 2)
                
                # Method 2: Try to get size from modelfile path
                modelfile = data.get("modelfile", "")
                if "FROM" in modelfile and "blobs" in modelfile:
                    # Extract blob path and try to get file size
                    import os
                    import re
                    match = re.search(r'FROM\s+([^\s]+)', modelfile)
                    if match:
                        blob_path = match.group(1)
                        if os.path.exists(blob_path):
                            size_bytes = os.path.getsize(blob_path)
                            size_gb = size_bytes / (1024 ** 3)
                            return round(size_gb, 2)
            
            # Fallback: estimate based on model name and quantization
            model_lower = model_name.lower()
            details = data.get("details", {}) if response.status_code == 200 else {}
            quant = details.get("quantization_level", "Q4_K_M")
            
            # More accurate estimates based on quantization
            if "8b" in model_lower or ":8b" in model_lower:
                return 4.5 if "Q4" in quant else 7.0
            elif "7b" in model_lower or ":7b" in model_lower:
                return 4.0 if "Q4" in quant else 6.5
            elif "3.8b" in model_lower or "3.8" in model_lower:
                return 2.3 if "Q4" in quant else 3.5
            elif "3b" in model_lower or ":3b" in model_lower:
                return 2.0 if "Q4" in quant else 3.0
            elif "tiny" in model_lower:
                return 0.6
            else:
                return 2.0
                    
    except Exception as e:
        logger.debug(f"Error getting memory usage for {model_name}: {e}")
        # Fallback estimation
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
                
                # Get memory usage first (fast, no model loading needed)
                memory = await get_model_memory_usage(model_name, ollama_base_url)
                
                # Measure speed (may take time, especially for large models)
                speed = await measure_model_speed(model_name, ollama_base_url)
                
                # Measure latency (quick health check)
                latency = await measure_model_latency(model_name, ollama_base_url)
                
                # Calculate quality score
                quality = calculate_quality_score(model_name, speed, memory)
                
                # Only add if we got at least memory or speed
                if memory > 0 or speed > 0:
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
                else:
                    logger.warning(f"Skipping {model_name}: no valid data collected")
                
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

