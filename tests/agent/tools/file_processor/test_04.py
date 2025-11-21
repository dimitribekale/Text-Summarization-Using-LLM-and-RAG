"""Test execute() method."""
import pytest
from src.agent.tools.file_processor import FileProcessorInput

class TestExecute:
    """Tests for execute() method."""

    def test_valid_file(self, file_processor, sample_txt_file):
        """execute() succeeds with valid file."""
        inp = FileProcessorInput(file_path=str(sample_txt_file))
        output = file_processor.execute(inp)
        assert output.success == True

    def test_return_filename(self, file_processor, sample_txt_file):
        """execute() returns original filename."""
        inp = FileProcessorInput(file_path=str(sample_txt_file))
        output = file_processor.execute(inp)
        assert output.filename == sample_txt_file.name

    def test_return_chunks(self, file_processor, sample_txt_file):
        """execute() returns list of chunks."""
        inp = FileProcessorInput(file_path=str(sample_txt_file))
        output = file_processor.execute(inp)
        assert isinstance(output.chunks, list)
        assert len(output.chunks) > 0

    def test_missing_file(self, file_processor):
        """execute() handles missing file gracefully."""
        inp = FileProcessorInput(file_path="nonexistent.txt")
        output = file_processor.execute(inp)
        assert output.success == False
        assert len(output.error_message) > 0

    def test_invalid_format(self, file_processor, tmp_path):
        """execute() handles unsupported file format gracefully."""
        invalid_file = tmp_path / "test.doc"
        invalid_file.write_text("content")
        inp = FileProcessorInput(file_path=str(invalid_file))
        output = file_processor.execute(inp)
        assert output.success == False