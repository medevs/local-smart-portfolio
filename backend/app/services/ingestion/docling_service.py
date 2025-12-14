import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from app.utils.logger import logger

# Check if Docling is available (it's heavy and optional)
DOCLING_AVAILABLE = False
try:
    from docling.document_converter import DocumentConverter
    from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
    DOCLING_AVAILABLE = True
except ImportError:
    logger.warning("Docling not available, using fallback methods only")


@dataclass
class ChunkingResult:
    """Result of document chunking with metadata about the process."""
    chunks: List[Dict[str, Any]]
    method: str  # "hybrid", "fallback_langchain", "fallback_pypdf", "fallback_docx", "fallback_text"
    total_chunks: int
    source_file: str


class DoclingIngestionService:
    """
    Ingestion service with optional Docling support.
    Falls back to PyPDF/python-docx if Docling is not available or fails.

    Pipeline:
    1. Try Docling DocumentConverter + HybridChunker (if available)
    2. Fallback to PyPDF/python-docx + LangChain chunker
    """

    def __init__(self, max_tokens: int = 512, use_docling: bool = False):
        """
        Args:
            max_tokens: Maximum tokens per chunk
            use_docling: Whether to try Docling first (slower but better quality)
        """
        self.max_tokens = max_tokens
        self.use_docling = use_docling and DOCLING_AVAILABLE
        self._converter = None
        self._chunker = None
        self._tokenizer = None
        logger.info(f"DoclingIngestionService initialized (docling={'enabled' if self.use_docling else 'disabled'})")

    def _get_converter(self):
        """Lazy-load Docling DocumentConverter with optimized settings."""
        if self._converter is None:
            from docling.document_converter import DocumentConverter, PdfFormatOption
            from docling.datamodel.pipeline_options import PdfPipelineOptions
            from docling.datamodel.base_models import InputFormat

            # Optimize for speed: disable table structure recognition (slowest part)
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_table_structure = False  # Skip table structure (saves ~60s)
            pipeline_options.do_ocr = False  # Skip OCR for text-based PDFs (saves ~20s)

            self._converter = DocumentConverter(
                format_options={
                    InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
                }
            )
            logger.info("Docling DocumentConverter loaded (optimized: no table structure, no OCR)")
        return self._converter

    def _get_chunker(self):
        """Lazy-load HybridChunker with tokenizer."""
        if self._chunker is None:
            try:
                from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
                from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
                from transformers import AutoTokenizer

                # Use HuggingFace tokenizer wrapper (as per Docling docs)
                EMBED_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
                self._tokenizer = HuggingFaceTokenizer(
                    tokenizer=AutoTokenizer.from_pretrained(EMBED_MODEL_ID)
                )
                self._chunker = HybridChunker(
                    tokenizer=self._tokenizer,
                    max_tokens=self.max_tokens,
                    merge_peers=True  # Merge small adjacent chunks
                )
                logger.info(f"HybridChunker loaded with max_tokens={self.max_tokens}")
            except Exception as e:
                logger.warning(f"Failed to load HybridChunker: {e}")
                self._chunker = None
        return self._chunker

    def _read_document_with_docling(self, file_path: str) -> Tuple[Optional[str], Optional[Any]]:
        """
        Read document using Docling.
        Returns: (markdown_content, docling_document)
        """
        try:
            converter = self._get_converter()
            result = converter.convert(file_path)
            doc = result.document
            markdown = doc.export_to_markdown()
            logger.info(f"[DOCLING] Successfully converted: {os.path.basename(file_path)}")
            return markdown, doc
        except Exception as e:
            logger.warning(f"[DOCLING] Conversion failed: {e}")
            return None, None

    def _read_document_fallback(self, file_path: str) -> Tuple[str, str]:
        """
        Fallback text extraction when Docling fails.
        Returns: (text_content, method_used)
        """
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.pdf':
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            text_parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            logger.info(f"[FALLBACK-PYPDF] Extracted {len(text_parts)} pages")
            return "\n\n".join(text_parts), "fallback_pypdf"

        elif ext == '.docx':
            from docx import Document
            doc = Document(file_path)
            text_parts = [para.text for para in doc.paragraphs if para.text.strip()]
            logger.info(f"[FALLBACK-DOCX] Extracted {len(text_parts)} paragraphs")
            return "\n\n".join(text_parts), "fallback_docx"

        elif ext in ['.md', '.txt']:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"[FALLBACK-TEXT] Read {len(content)} characters")
            return content, "fallback_text"

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _chunk_with_hybrid(self, content: str, docling_doc: Any) -> Optional[List[Dict[str, Any]]]:
        """
        Chunk using Docling's HybridChunker (structure-aware).

        Uses chunker.contextualize() to get context-enriched text that includes
        heading hierarchy - better for RAG/embeddings than raw text.
        """
        chunker = self._get_chunker()
        if chunker is None or docling_doc is None:
            return None

        try:
            chunks = list(chunker.chunk(dl_doc=docling_doc))

            processed_chunks = []
            for i, chunk in enumerate(chunks):
                # Get contextualized text (includes heading hierarchy)
                # contextualize() is better for RAG than serialize()
                try:
                    text = chunker.contextualize(chunk=chunk)
                except Exception:
                    # Fallback to raw text if contextualize fails
                    text = chunk.text

                # Extract metadata safely
                headings = []
                if hasattr(chunk, 'meta') and chunk.meta:
                    if hasattr(chunk.meta, 'headings') and chunk.meta.headings:
                        headings = [str(h) for h in chunk.meta.headings]

                processed_chunks.append({
                    "text": text,
                    "metadata": {
                        "chunk_index": i,
                        "headings": headings,
                        "has_context": True
                    }
                })

            logger.info(f"[HYBRID-CHUNKER] Created {len(processed_chunks)} structure-aware chunks")
            return processed_chunks

        except Exception as e:
            logger.warning(f"[HYBRID-CHUNKER] Failed: {e}")
            return None

    def _chunk_with_langchain(self, content: str) -> List[Dict[str, Any]]:
        """
        Fallback chunking using LangChain's RecursiveCharacterTextSplitter.
        """
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        chunks = splitter.split_text(content)

        processed_chunks = []
        for i, text in enumerate(chunks):
            processed_chunks.append({
                "text": text,
                "metadata": {
                    "chunk_index": i,
                    "headings": [],
                    "has_context": False
                }
            })

        logger.info(f"[LANGCHAIN-CHUNKER] Created {len(processed_chunks)} simple chunks")
        return processed_chunks

    def process_document(self, file_path: str, original_filename: str = None) -> List[Dict[str, Any]]:
        """
        Process a document and return chunks with metadata.

        Strategy (when use_docling=True):
        1. Try Docling conversion + HybridChunker (best quality but slow)
        2. Fallback to Docling + LangChain chunker
        3. Fallback to PyPDF/python-docx + LangChain chunker

        Strategy (when use_docling=False, default):
        - Directly use PyPDF/python-docx + LangChain chunker (fast)

        Args:
            file_path: Path to the file (may be temp file)
            original_filename: Original filename to use in metadata

        Returns chunks with 'method' in metadata showing which strategy was used.
        """
        logger.info(f"Processing document: {file_path}")
        # Use original filename for metadata, not temp file name
        filename = original_filename or os.path.basename(file_path)

        # Fast path: Skip Docling entirely (default)
        if not self.use_docling:
            logger.info(f"Using fast fallback extraction (Docling disabled)")
            try:
                content, method = self._read_document_fallback(file_path)
                if content and content.strip():
                    chunks = self._chunk_with_langchain(content)
                    logger.info(f"[SUCCESS] Used {method} strategy for {filename}")
                    return self._finalize_chunks(chunks, filename, method)
            except Exception as e:
                logger.error(f"[FAILED] Fallback extraction failed: {e}")
                raise ValueError(f"Could not process document: {e}")

        # Slow path: Try Docling first (if enabled)
        markdown, docling_doc = self._read_document_with_docling(file_path)

        if markdown and docling_doc:
            chunks = self._chunk_with_hybrid(markdown, docling_doc)
            if chunks:
                method = "hybrid"
                logger.info(f"[SUCCESS] Used {method} strategy for {filename}")
                return self._finalize_chunks(chunks, filename, method)

            # Strategy 2: Docling worked but HybridChunker failed
            chunks = self._chunk_with_langchain(markdown)
            method = "fallback_langchain"
            logger.info(f"[SUCCESS] Used {method} strategy for {filename}")
            return self._finalize_chunks(chunks, filename, method)

        # Strategy 3: Docling failed, use fallback extraction
        try:
            content, method = self._read_document_fallback(file_path)
            if not content or not content.strip():
                raise ValueError("No content extracted")

            chunks = self._chunk_with_langchain(content)
            logger.info(f"[SUCCESS] Used {method} strategy for {filename}")
            return self._finalize_chunks(chunks, filename, method)

        except Exception as e:
            logger.error(f"[FAILED] All strategies failed for {filename}: {e}")
            raise ValueError(f"Could not process document: {e}")

    def _finalize_chunks(self, chunks: List[Dict[str, Any]], source: str, method: str) -> List[Dict[str, Any]]:
        """Add source and method to all chunks."""
        for chunk in chunks:
            chunk["metadata"]["source"] = source
            chunk["metadata"]["method"] = method
            chunk["metadata"]["total_chunks"] = len(chunks)
        return chunks
