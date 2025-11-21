"""
Shared fixtures for FileProcessor test.
"""
import pytest
from src.agent.tools.file_processor import FileProcessor
from src.logging_config import get_logger

@pytest.fixture
def file_processor(config):
    """Provide a FileProcessor instance."""
    logger = get_logger("test.file_processor")
    return FileProcessor(config=config, logger=logger)

@pytest.fixture
def sample_txt_file(tmp_path):
    """Create a simple TXT file for testing."""
    content = """
    Introduction
    This is a document about machine learning and AI systems.
    It contains multiple sections and paragraphs.

    The main section discusses various approaches to building
    intelligent systems that can learn from data.

    Another important topic is how to deploy these systems
    in production environments effectively.

    References
    [1] Smith, J. (2020). Introduction to Machine Learning.
    [2] Jones, M. (2021). Deep Learning Applications.
    [3] Brown, A. (2022). AI Systems Design Patterns.
    """
    file_path = tmp_path / "sample.txt"
    file_path.write_text(content)
    return file_path
