"""
Logging configuration using Loguru.
Provides structured logging with colored output and file rotation.
"""

import sys
from loguru import logger
from pathlib import Path


def setup_logging(debug: bool = True) -> None:
    """
    Configure Loguru logger with console and file handlers.
    
    Args:
        debug: Enable debug level logging
    """
    # Remove default handler
    logger.remove()
    
    # Console handler with colors
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    logger.add(
        sys.stderr,
        format=log_format,
        level="DEBUG" if debug else "INFO",
        colorize=True,
    )
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # File handler with rotation
    logger.add(
        log_dir / "app_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG" if debug else "INFO",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
    )
    
    # Error-only file handler
    logger.add(
        log_dir / "errors_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
    )
    
    logger.info("Logging configured successfully")


# Export logger instance
__all__ = ["logger", "setup_logging"]

