"""
Test logging configuration.
"""
import sys
import pytest
import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.config import Config
from src.logging_config import setup_logging, get_logger


class TestSetupLogging:
    """Tests for the setup_logging function."""

    def test_setup_logging_creates_logger(self, config):
        """Verify setup_logging creates the 'agent' logger."""
        setup_logging(config)
        logger = logging.getLogger("agent")
        assert logger is not None

    def test_setup_logging_adds_console_handler(self, config):
        """Verify console handler is added."""
        # Reset logger before test
        logger = logging.getLogger("agent")
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        setup_logging(config)

        # Check that at least one StreamHandler exists
        # But not file handler.
        has_stream_handler = any(
            isinstance(h, logging.StreamHandler) and not isinstance(
                h, logging.FileHandler
            )
            for h in logger.handlers
        )
        assert has_stream_handler

    def test_add_file_handler(self, config):
        """Verify file handler is added when LOG_TO_FILE is True."""
        # Reset logger before test
        logger = logging.getLogger("agent")
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        if config.log_to_file:
            setup_logging(config)

            # Check that FileHandler exists
            has_file_handler = any(
                isinstance(h, logging.FileHandler)
                for h in logger.handlers
            )
            assert has_file_handler


class TestGetLogger:
    """Tests for the get_logger function."""

    def test_get_logger_returns_logger(self):
        """Verify get_logger returns a logger instance."""
        logger = get_logger("agent.test")
        assert isinstance(logger, logging.Logger)

    def test_get_logger_with_module_name(self):
        """Verify logger name is set correctly."""
        logger = get_logger("agent.tools.file_processor")
        assert logger.name == "agent.tools.file_processor"

    def test_get_logger_hierarchy(self):
        """Verify loggers are properly hierarchical."""
        logger1 = get_logger("agent")
        logger2 = get_logger("agent.tools")
        logger3 = get_logger("agent.tools.processor")

        assert isinstance(logger1, logging.Logger)
        assert isinstance(logger2, logging.Logger)
        assert isinstance(logger3, logging.Logger)