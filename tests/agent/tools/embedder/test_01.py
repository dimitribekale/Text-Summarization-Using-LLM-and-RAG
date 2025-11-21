"""
Test EmbedderInput validation.
"""
import pytest
from src.agent.tools.embedder import EmbedderInput

class TestInputValidation:

    def test_input_chunks(self):
        """Test if the input accepts a list of chunks"""
        chunks = ["chunk 1", "chunk 2", "chunk 3"]
        input = EmbedderInput(chunks=chunks)
        assert input.chunks == chunks
        assert input.model_name == "all-MiniLM-L6-v2"

    def test_custom_model_name(self):
        """Input accepts custom model_name."""
        chunks = ["chunk 1"]
        input = EmbedderInput(
            chunks=chunks, 
            model_name="sentence-transformers/paraphrase-MiniLM-L6-v2"
          )
        assert input.model_name == "sentence-transformers/paraphrase-MiniLM-L6-v2"

    def test_require_chunks(self):
        """Input requires chunks parameter."""
        with pytest.raises(Exception):
            EmbedderInput()

    def test_input_chunks_must_be_list(self):
        """Input chunks must be a list."""
        with pytest.raises(Exception):
            EmbedderInput(chunks="not a list")