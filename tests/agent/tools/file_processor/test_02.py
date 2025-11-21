"""Test the _chunk_text() method"""
import pytest
from src.agent.errors import FileProcessingError

class TextChunkText:

    def test_create_chunks(self, file_processor):
        """_chunk_text() returns a list of chunks."""
        text = "AAABBBCCCDDDEEEFFFGGG"
        chunks = file_processor._chunk_text(text, chunk_size=5, chunk_overlap=2)
        assert isinstance(chunks, list)
        assert len(chunks) > 0

    def test_create_overlap(self, file_processor):
        """Create chunks overlap as specified."""
        text = "AAABBBCCCDDDEEEFFFGGG"
        chunks = file_processor._chunk_text(text, chunk_size=5, chunk_overlap=2)
        assert chunks[0][-2:] == chunks[1][:2]

    def test_chunk_respects_size(self, file_processor):
        """Chunks don't exceed specified size (except last)."""
        text = "A" * 1000
        chunks = file_processor._chunk_text(text, chunk_size=100, chunk_overlap=10)

        # All chunks except last should be exactly chunk_size
        for chunk in chunks[:-1]:
            assert len(chunk) == 100

    def test_invalid_size(self, file_processor):
          """Invalid chunk_size raises FileProcessingError."""
          with pytest.raises(FileProcessingError):
              file_processor._chunk_text("text", chunk_size=0, chunk_overlap=0)

    def test_invalid_overlap(self, file_processor):
        """Invalid overlap raises FileProcessingError."""
        with pytest.raises(FileProcessingError):
            file_processor._chunk_text("text", chunk_size=5, chunk_overlap=10)