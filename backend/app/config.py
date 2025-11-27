"""
Application configuration using Pydantic Settings.
Loads environment variables from .env file.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application Settings
    app_name: str = Field(default="AI Portfolio Backend")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=True)
    
    # Server Settings
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    
    # CORS Settings
    cors_origins: str = Field(default="http://localhost:3000,http://127.0.0.1:3000")
    
    # Ollama Settings
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama3.2:3b")
    
    # ChromaDB Settings
    chroma_persist_dir: str = Field(default="./data/chroma_db")
    chroma_collection_name: str = Field(default="portfolio_docs")
    
    # Document Settings
    upload_dir: str = Field(default="./data/documents")
    max_file_size_mb: int = Field(default=10)
    allowed_extensions: str = Field(default=".pdf,.md,.txt,.docx")
    
    # RAG Settings
    chunk_size: int = Field(default=500)
    chunk_overlap: int = Field(default=50)
    top_k_results: int = Field(default=3)
    
    # Embedding Model
    embedding_model: str = Field(default="all-MiniLM-L6-v2")
    
    # Admin Settings
    admin_api_key: str = Field(default="dev-admin-key-123")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Parse allowed extensions from comma-separated string."""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]
    
    @property
    def max_file_size_bytes(self) -> int:
        """Convert MB to bytes."""
        return self.max_file_size_mb * 1024 * 1024
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid reading .env file multiple times.
    """
    return Settings()


# Create directories if they don't exist
def ensure_directories():
    """Create necessary directories for the application."""
    settings = get_settings()
    
    directories = [
        settings.chroma_persist_dir,
        settings.upload_dir,
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

