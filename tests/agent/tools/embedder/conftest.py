import pytest
from src.agent.tools.embedder import Embedder
from src.logging_config import get_logger

@pytest.fixture
def embedder(config):
    """Creates an embedder instance"""
    logger = get_logger("test.embedder")
    return Embedder(config=config, logger=logger)

@pytest.fixture
def sample_chunks():
    """Sample for testing"""
    return [
        "This is the first chunk about machine learning.",
        "The second chunk discusses neural networks.",
        "The third chunk covers deep learning concepts."
    ]

@pytest.fixture
def sample_single_chunk():
    """Single chunk for testing."""
    return ["Machine learning is a subset field of artificial intelligence."]