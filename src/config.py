import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class Config:
    """
    Configuration data for the agent.
    Loads from environment variables.
    """
    input_folder: Path = Path(os.getenv("INPUT_FOLDER", "input_files"))
    output_folder: Path = Path(os.getenv("OUTPUT_FOLDER", "output_files"))

    model_name: str = os.getenv("MODEL_NAME",  "deepseek-r1:7b")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_timeout: int = int(os.getenv("OLLAMA_TIMEOUT", "300"))

    chunk_size: int = int(os.getenv("CHUNK_SIZE", "2500"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    top_k_chunks: int = int(os.getenv("TOP_K_CHUNKS", "3"))

    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    max_retries: int = int(os.getenv("MAX_RETRIES", "3"))
    retry_delay: float = float(os.getenv("RETRY_DELAY", "1.0"))

    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_to_file: bool = os.getenv("LOG_TO_FILE", "True").lower() == "true"
    log_file: Optional[Path] = None

    def __post_init__(self):
        """Validate configuration after initialization."""
        self.input_folder.mkdir(parents=True, exist_ok=True)
        self.output_folder.mkdir(parents=True, exist_ok=True)

        if self.log_to_file and self.log_file is None:
            self.log_file = self.output_folder / "agent.log"

    def validate(self) -> None:
        """
        Validate configuration values
        Raises ValueError if configuration is invalid.
        """
        if not self.input_folder.exists():
            raise ValueError(f"Input folder does not exist: {self.input_folder}")
        if not self.output_folder.exists():
            raise ValueError(f"Output folder does not exist: {self.output_folder}")

        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be positive integer")

        if self.max_retries < 0:
            raise ValueError("max_retries cannot be negative")

        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(f"Invalid log_level: {self.log_level}")