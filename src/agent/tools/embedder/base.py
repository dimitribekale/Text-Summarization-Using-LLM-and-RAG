from pydantic import BaseModel, Field
from src.agent.tools.base import ToolInput, ToolOutput

class EmbedderInput(ToolInput):
    """
    Input for Embedder tool.
    """
    chunks: list[str] = Field(
        ...,
        description="List of text chunks to convert to embeddings"
    )
    model_name: str = Field(
        default="all-MiniLM-L6-v2",
        description="Name of SentenceTransformer model to use"
    )

class EmbedderOutput(ToolOutput):

    embeddings: list[list[float]] = Field(
        default_factory=list,
        description="List of embedding vectors"
    )
    embedding_dim: int = Field(
        default=0,
        description="Dimensionality of each embedding"
    )
    chunks_embedded: int = Field(
        default=0,
        description="Number of chunks that were embedded"
    )