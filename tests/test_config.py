"""
Tests for configuration management.
"""
import sys
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.config import Config


class TestConfigLoading:
    """Tests for Config class initialization."""

    def test_config_loads_from_env(self):
        """Verify Config loads values from .env."""
        config = Config()
        assert config.model_name is not None
        assert config.input_folder is not None

    def test_config_creates_folders(self, config):
        """Verify Config creates input and output folders."""
        assert config.input_folder.exists()
        assert config.output_folder.exists()

    def test_config_log_file_path_set(self, config):
        """Verify log file path is set when enabled."""
        if config.log_to_file:
            assert config.log_file is not None


class TestConfigValidation:
    """Tests for Config validation."""

    def test_validate_success(self, config):
        """Verify validate() succeeds with valid config."""
        # Should not raise exception
        config.validate()

    def test_validate_invalid_log_level(self):
        """Verify validation fails with invalid log level."""
        config = Config()
        config.log_level = "INVALID_LEVEL"

        with pytest.raises(ValueError):
            config.validate()