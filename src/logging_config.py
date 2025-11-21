import logging
from pathlib import Path
from typing import Optional
from src.config import Config

def setup_logging(config: Config) -> None:
    """
    Set up logging for the agent.
    Configures both console and file logging based on config.
    """
    logger = logging.getLogger("agent")

    if logger.hasHandlers():
        print(f"DEBUG: setup_logging returning early. Handlers: {len(logger.handlers)}")
        return

    print(f"DEBUG: setup_logging proceeding. Handlers: {len(logger.handlers)}")
    # Convert log level string to logging constant
    # "INFO" -> logging.INFO, "DEBUG" -> logging.DEBUG etc...
    log_level = getattr(logging, config.log_level.upper())
    logger.setLevel(logging.DEBUG)

    log_format = "%(asctime)s |  %(levelname)-8s | %(name)s | %(message)s"
    formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) # Only info and above
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if config.log_to_file and config.log_file:
        try:
            file_handler = logging.FileHandler(config.log_file)
            file_handler.setLevel(logging.DEBUG) # All levels in file
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not set up file logging: {e}")

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    Args:
        name: Module name (__name__)
    Returns:
        logging.Logger: Configured logger for this module.
    """
    return logging.getLogger(name)
