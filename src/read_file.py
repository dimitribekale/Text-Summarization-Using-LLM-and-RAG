import re
import PyPDF2
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer



class FileProcessor:
    """
    Class to handle reading and processing files.
    Supports .txt and .pdf formats.

    """
    def __init__(self, file_path: Path, embedder = None):
        self.supported_formats = [".txt", ".pdf"]
        self.file_path = file_path
        self.max_chunk_length = 2500
        self.embedder = embedder if embedder else SentenceTransformer("all-MiniLM-L6-v2")


    def __call__(self) -> tuple[str, list, np.ndarray]:

        """
        Process the file: read, clean, chunk, and embed.
        Returns the filename and a list of chunks.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        text = self.read_file()
        chunks = self.chunk_text(text)
        embeddings = self.embed_chunks(chunks)
        return self.file_path.name, chunks, embeddings

    def read_file(self) -> str:
        """
        Read file content from .txt or .pdf.
        """
        if self.file_path.suffix.lower() == self.supported_formats[0]:
            return self.file_path.read_text(encoding="utf-8")
        elif self.file_path.suffix.lower() == self.supported_formats[1]:
            text = ""
            with self.file_path.open("rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            cleaned_text = self.clean_text(text)
            return cleaned_text
        else:
            raise ValueError(f"Unsupported file type: {self.file_path.suffix}")


    def clean_text(self, text: str) -> str:
        """
        Remove sections like 'Bibliography' or 'References' if present.
    
        """
        match = re.search(r"(Bibliography|References)", text, re.IGNORECASE)
        return text[:match.start()] if match else text


    def chunk_text(self, text: str) -> list:
        """
        Split text into smaller chunks; for RAG, shorter chunks are easier to retrieve.
        """

        paragraphs = text.split("\n")
        chunks = []
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) + 1 > self.max_chunk_length:
                chunks.append(current_chunk.strip())
                current_chunk = para + "\n"
            else:
                current_chunk += para + "\n"
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks
    
    def embed_chunks(self, chunks: list) -> np.ndarray:
        """
        Compute embedding for each chunk.
        """
        return np.array([self.embedder.encode(chunk) for chunk in chunks])


        
    

