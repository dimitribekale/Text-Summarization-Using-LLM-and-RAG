import pytest
from pathlib import Path
from src.config import Config


@pytest.fixture
def config():
    """
    Provides a Config instance for tests.

    Loads from .env file.
    """
    return Config()


@pytest.fixture
def temp_dir(tmp_path):
    """
    Provides a temporary directory for test files.

    tmp_path is a pytest built-in fixture that creates
    a unique temporary directory for each test.
    """
    return tmp_path


@pytest.fixture
def sample_text():
    """
    Provides sample text for testing.
    """
    return """
    This is a sample document for testing.
    It contains multiple sentences and paragraphs.

    The agent should be able to process this text
    and extract meaningful information from it.
    """