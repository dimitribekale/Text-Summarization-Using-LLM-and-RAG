"""
Test embedding execution
"""
import pytest
from src.agent.tools.embedder import EmbedderInput, EmbedderOutput

class TestEmbeddingExecution:

    def test_valid_chunks(self, embedder, sample_chunks):
        """execute() successfully embeds valid chunks."""
        input = EmbedderInput(chunks=sample_chunks)
        output = embedder.execute(input)
        assert output.success == True
        assert len(output.embeddings) == len(sample_chunks)
        assert output.chunks_embedded == len(sample_chunks)

    def test_correct_dimension(self, embedder, sample_chunks):
        """Each embedding has correct dimensionality (384 for all-MiniLM-L6-v2)."""
        inp = EmbedderInput(chunks=sample_chunks)
        output = embedder.execute(inp)
        assert output.embedding_dim == 384  # all-MiniLM-L6-v2 produces 384-dim vectors
        for embedding in output.embeddings:
            assert len(embedding) == 384

    def test_embeddings_are_numeric(self, embedder, sample_chunks):
          """Embeddings contain numeric values (floats)."""
          inp = EmbedderInput(chunks=sample_chunks)
          output = embedder.execute(inp)

          for embedding in output.embeddings:
              for value in embedding:
                  assert isinstance(value, (int, float))

    def test_single_chunk(self, embedder, sample_single_chunk):
        """execute() works with single chunk."""
        input = EmbedderInput(chunks=sample_single_chunk)
        output = embedder.execute(input)
        assert output.success == True
        assert len(output.embeddings) == 1
        assert output.chunks_embedded == 1

    def test_correct_output_type(self, embedder, sample_chunks):
        """execute() returns EmbedderOutput instance."""
        input = EmbedderInput(chunks=sample_chunks)
        output = embedder.execute(input)
        assert isinstance(output, EmbedderOutput)
        assert hasattr(output, 'success')
        assert hasattr(output, 'embeddings')
        assert hasattr(output, 'embedding_dim')
        assert hasattr(output, 'chunks_embedded')