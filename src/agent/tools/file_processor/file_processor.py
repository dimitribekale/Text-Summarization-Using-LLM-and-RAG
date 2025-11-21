"""
Extracts and chunks text from PDF/TXT files.
"""
import re
from pathlib import Path
from src.agent.tools.base import Tool
from src.agent.errors import FileProcessingError
from src.agent.tools.file_processor.base import FileProcessorInput, FileProcessorOutput
from src.logging_config import get_logger


class FileProcessor(Tool):
    """
    Reads files and extracts/chunks test
    """
    def __init__(self, config, logger=None):
        self.config = config
        self.logger = logger or get_logger(__name__)

    @property
    def name(self) -> str:
        """Tool name"""
        return "FileProcessor"
    
    def execute(self, input_data: FileProcessorInput) -> FileProcessorOutput:
        """
        Execute tool
        
        Args:
            input_data: FileProcessorInput with file_path and parameters
        Returns:
            FileProcessorOutput with chunks and metadata
        """
        try:
            logger = self.logger
            logger.debug(f"Validating input for file: {input_data.file_path}")

            if not input_data.validate_file():
                raise FileProcessingError(f"File does not exist: {input_data.file_path}")
            
            if not input_data.validate_file_type():
                raise FileProcessingError(
                    f"Unsupported file type: {input_data.file_path}"
                    "Supported types: .pdf, .txt"
                    )
            logger.info(f"Reading file: {input_data.file_path}")
            raw_text = self._read_file(input_data.file_path)
            logger.debug(f"Read {len(raw_text)} characters from file.")

            logger.debug("Cleaning text ...")
            cleaned_text = self._clean_text(raw_text)
            logger.debug(f"Cleaned text: {len(cleaned_text)} characters")

            logger.debug(
              f"Chunking text with size={input_data.chunk_size}, "
              f"overlap={input_data.chunk_overlap}"
            )
            chunks = self._chunk_text(
                cleaned_text,
                input_data.chunk_size,
                input_data.chunk_overlap
            )
            logger.info(f"Created {len(chunks)} chunks")

            # Calculate some statistics
            total_chars = sum(len(chunk) for chunk in chunks)
            file_size = Path(input_data.file_path).stat().st_size

            # Build the output
            output = FileProcessorOutput(
                success=True,
                filename=Path(input_data.file_path).name,
                chunks=chunks,
                chunk_count=len(chunks),
                total_characters=total_chars,
                file_size_bytes=file_size
            )
            logger.info(
                f"FileProcessor completed successfully. "
                f"File: {output.filename}, Chunks: {output.chunk_count}"
            )
            return output
        
        except FileProcessingError as e:
            logger.error(f"FileProcessingError: {str(e)}")
            return FileProcessorOutput(
                success=False,
                error_message=str(e),
                filename=Path(input_data.file_path).name
            )
        except Exception as e:
            logger.error(f"Unexpected error in FileProcessor: {str(e)}", exc_info=True)
            return FileProcessorOutput(
                success=False,
                error_message=f"Unexpected error: {str(e)}",
                filename=input_data.file_path
            )

    def _read_file(self, file_path: str) -> str:
        """Read PDF and TXT"""
        try:
            path = Path(file_path)
            if not path.exists():
                raise FileProcessingError(f"File not found: {file_path}")
            
            ext = path.suffix.lower()
            if ext == '.pdf':
                try:
                    from PyPDF2 import PdfReader
                except ImportError:
                    raise FileProcessingError("PyPDF2 not installed.")
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
            elif ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()

            else: # Unsupported format.
                raise FileProcessingError(f"Unsupported file format: {ext}. Supported format are .pdf, .txt")                   
        except FileProcessingError:
            raise

        except Exception as e:
            raise FileProcessingError(f"Failed to read file {file_path}: {str(e)}") from e
    
    def _clean_text(self, text: str) -> str:
        """
        Removes unwanted sections
        Such as references, bibliography, etc..."""
        text_lower = text.lower()

        unwanted_sections = [
            r'references?\s*\n',         
            r'bibliography\s*\n',       
            r'appendix\s+[a-z]?\s*\n', 
            r'appendices\s*\n',        
            r'index\s*\n',             
            r'acknowledgments?\s*\n',  
            r'works? cited\s*\n',
        ]

        earliest_match = None
        earliest_position = len(text)

        for pattern in unwanted_sections:
            match = re.search(pattern, text_lower)
            if match:
                if match.start() < earliest_position:
                    earliest_position = match.start()
                    earliest_match = match

        # If a section was found, keep only text before it
        if earliest_match:
            text = text[:earliest_match.start()]
            self.logger.debug(f"Removed text after: {earliest_match.group()}")

        return text.strip()

    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> list[str]:
        """
        Split text into overlapping chunks
        Chunks overlap to provide context for semantic search.
        """
        if chunk_size <= 0:
            raise FileProcessingError(f"Chunk_size must be a positive number, got {chunk_size}")
        
        if overlap < 0 or overlap >= chunk_size:
            raise FileProcessingError(f"overlap must be positive and inferior to chunk_size")
        
        if not text:
            raise FileProcessingError("Cannot chunk empty text")
        
        chunks = []
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            chunk = text[start:end]
            chunks.append(chunk)

            # Move start position by (chunk_size - overlap)
            # THis creates the overlap for context
            step = chunk_size - overlap
            start += step
        return chunks


