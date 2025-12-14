from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=True)
    session_id = Column(String(255), index=True)  # Browser session
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

class Document(Base):
    """
    Represents a searchable document chunk (as per rag.txt spec).
    This table stores CHUNKS to enable granular keyword search and RRF alignment with ChromaDB.
    """
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=True)
    source = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    content = Column(Text, nullable=True)
    tsv = Column(TSVECTOR)
    
    # Metadata fields (optional but useful for consistency with Chroma)
    # parent_id = Column(UUID(as_uuid=True), nullable=True) 
    # position = Column(Integer, nullable=True)

    __table_args__ = (
        Index('idx_docs_tsv', 'tsv', postgresql_using='gin'),
    )

class UploadedFile(Base):
    """
    Tracks file uploads/ingestion status.
    """
    __tablename__ = "uploaded_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=True)
    chunk_count = Column(Integer, default=0)
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

