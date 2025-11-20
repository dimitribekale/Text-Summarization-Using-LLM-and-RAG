from pathlib import Path
from pydantic import Field
from src.agent.tools.base import ToolInput, ToolOutput


class FileProcessorInput(ToolInput):
    """Defines the input data format required"""
    file_path: str = Field(..., description="Absolute or relative path to the file")
    chunk_size: int = Field(default=2500,
                            description="Target size of each chunks in charaters")
    chunk_overlap: int = Field(
        default=200,
        description="Character overlap between consecutive chunks for context."
    )

    def validate_file(self) -> bool:
        return Path(self.file_path).exists() 
    
    def validate_file_type(self) -> bool:
        ext = Path(self.file_path).suffix.lower()
        return ext in ['.pdf', '.txt']
    
class FileProcessorOutput(ToolOutput):

    filename: str = Field(
        default="",
        description="Name of the processed file"
    )
    chunks: list[str] = Field(
        default_factory=list,
        description="List of text chunks extracted from the file"
    )
    chunk_count: int = Field(
        default=0,
        description="Total number of chunks created"
    )
    total_characters: int = Field(
        default=0,
        description="Total characters accross all chunks"
    )
    file_size_bytes: int = Field(
        default=0,
        description="Original file size in bytes"
    )