"""
Test the tool error handling.
"""
import pytest
from src.agent.tools.embedder import EmbedderInput

class TestErrorHandling:
    """Tests for error handling."""

    def test_empty_chunks(self, embedder):
        """execute() raises error for empty chunks list ."""
        input = EmbedderInput(chunks=[])
        output = embedder.execute(input)
        assert output.success == False
        assert len(output.error_message) > 0
        assert "empty" in output.error_message.lower()

    def test_empty_strings(self, embedder):
        """execute() handles chunks with empty strings."""
        input = EmbedderInput(chunks=["valid text", "", "more valid text"])
        output = embedder.execute(input)
        # Should still succeed because SentenceTransformer handles empty strings
        assert output.success == True
        assert output.chunks_embedded == 3

    def test_empty_output(self, embedder):
        """When execute fails, embeddings list is empty."""
        input = EmbedderInput(chunks=[])
        output = embedder.execute(input)
        assert output.success == False
        assert len(output.embeddings) == 0
        assert output.chunks_embedded == 0

    def test_output_null(self, embedder):
        """When execute fails, embedding_dim is 0."""
        input = EmbedderInput(chunks=[])
        output = embedder.execute(input)
        assert output.embedding_dim == 0