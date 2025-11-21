import sys
import pytest
import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.config import Config

@pytest.fixture(autouse=True, scope="function")
def reset_logging():
    """
    Reset logging before each test.
    Removes all handlers so setup_logging() can configure
    fresh logging for each test.

    This runs BEFORE and AFTER each test function.
    """
    logger = logging.getLogger("agent")
    # Remove any existing handlers BEFORE test
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    yield

    # Remove handlers AFTER test (cleanup)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


@pytest.fixture
def config():
    """
    Provides a Config instance for tests.
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