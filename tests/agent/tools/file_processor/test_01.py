"""
Input validation test case.
"""
import pytest
from src.agent.tools.file_processor import FileProcessorInput

class TestInputValidation:
    
    def test_input_with_default_param(self):
        input = FileProcessorInput(file_path="test.txt")
        assert input.file_path == "test.txt"
        assert input.chunk_size == 2500

    def test_input_with_custom_chunk_size(self):
        input = FileProcessorInput(
            file_path="test.txt",
            chunk_size=1000
        )
        assert input.chunk_size == 1000

    def test_validate_real_file(self, sample_txt_file):
        """Validate that validate_file() returns True for existing file."""
        input = FileProcessorInput(file_path=str(sample_txt_file))
        assert input.validate_file() == True

    def test_validate_missing_file(self):
        """Validate that validate_file() returns false for missing file."""
        input = FileProcessorInput(file_path="nonexistent.txt")
        assert input.validate_file() == False

    def test_validate_file_type(self, sample_txt_file):
        """Validate that validate_file_type() returns True for .txt files."""
        input = FileProcessorInput(file_path=str(sample_txt_file))
        assert input.validate_file_type() == True

    def test_validate_invalid_format(self):
        """validate_file_type() returns False for unsupported formats."""
        input = FileProcessorInput(file_path="test.doc")
        assert input.validate_file_type() == False