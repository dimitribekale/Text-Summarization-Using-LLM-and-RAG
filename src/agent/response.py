from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DocumentChunk(BaseModel):
    """
    A single chunk of a document.
    """
    filename: str = Field(..., description="Original filename")
    content: str = Field(..., description="Text content of this chunk")
    chunk_index: int = Field(..., description="Which chunk number is this")
    embedding: Optional[list[float]] = Field(
        None,
        description="Vector embedding of this chunk"
    )

class SummaryResult(BaseModel):
    """
    The final summary result for a document.
    """
    filename: str = Field(..., description="Original filename")
    summary: str = Field(..., description="Generated summary")
    processed_at: datetime = Field(
        default_factory=datetime.now,
        description="When this was processed"
    )
    success: bool = Field(True, description="Did processing succeed?")
    error: Optional[str] = Field(None, description="Error message if failed")
    chunk_used: int = Field(
        0,
        description="How many chunks were used for retrieval"
    )
    processing_time_seconds: float = Field(
        0.0,
        description="How long processing took"
    )

class AgentResponse(BaseModel):
    """
    Complete agent execution response.
    
    This is the final output after processing all documents.
    """
    total_files: int = Field(description="Total files processed")
    successful: int = Field(description="Files successfully summarized")
    failed: int = Field(description="Files that failed")
    results: list[SummaryResult] = Field(
        description="All summary results"
    )
    execution_time_seconds: float = Field(
        description="Total time to process all the files"
    )

    def success_rate(self) -> float:
        """Calculate percentage of successful summaries."""
        if self.total_files == 0:
            return 0.0
        return (self.successful / self.total_files)* 100