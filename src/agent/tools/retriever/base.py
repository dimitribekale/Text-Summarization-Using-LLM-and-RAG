import numpy as np
from pydantic import BaseModel, Field
from dataclasses import dataclass
from src.agent.tools.base import ToolInput, ToolOutput

@dataclass
class HybridScores:
    """
    Container for all scoring stages in hybrid retrieval.
    Attributes:
        bm25_scores: Lexical relevance scores
        semantic_scores: Embedding similarity scores
        fused_scores: Combined scores after RRF fusion
        final_scores: Scores after reranking
    """
    bm25_scores: np.ndarray
    semantic_scores: np.ndarray
    fused_scores: np.ndarray
    final_scores: np.ndarray

    def __post_init__(self):
        """Validate that all score arrays have the same length."""
        lengths = [
            len(self.bm25_scores),
            len(self.semantic_scores),
            len(self.fused_scores),
            len(self.final_scores)
        ]
        if len(set(lengths)) != 1:
            raise ValueError(
                f"All score arrays must have same length. "
                f"Got: bm25={lengths[0]}, semantic={lengths[1]}, "
                f"fused={lengths[2]}, final={lengths[3]}"
            )



class ChunkMetadata(BaseModel):
    """Metadata about a chunk."""
    chunk_index: int = Field(...)
    source_position: str = Field(
        default="middle",
        description="Position in document: 'intro', 'middle', 'conclusion'"
    )
    chunk_length: int = Field(default=0, description="Length of the chunk in characters")
    is_header: bool = Field(default=False, description="Whether this chunk is a header/title")

class RetrieverResult(BaseModel):
    """Single result from retriever."""
    chunk: str = Field(...)
    chunk_index: int = Field(...)
    bm25_score: float = Field(default=0.0, description="BM25 lexical relevance score")
    semantic_score: float = Field(default=0.0, description="Semantic similarity score")
    bm25_rank: int = Field(default=0, description="BM25 ranking position")
    semantic_rank: int = Field(default=0, description="Semantic ranking position")
    rrf_score: float = Field(default=0.0, description="RRF combined score")
    rerank_score: float = Field(default=0.0, description="Cross-encoder reranking score")
    final_score: float = Field(default=0.0, description="Final combined score after all stages")
    diversity_penality: float = Field(default=0.0, description="Penality for similarity to already selected chunks")
    metadata: ChunkMetadata = Field(default_factory=lambda: ChunkMetadata(chunk_index=0))

class RetrieverInput(ToolInput):
    """Input for hybrid retriever tool."""
    query: str = Field(..., description="User query to search")
    chunks: list[str] = Field(..., description="Document chunks to search through")
    embeddings: list[list[float]] = Field(..., description="Embeddings for the chunks")

    top_k: int = Field(default=5, ge=1, le=100, description="Number of final results to return")
    use_bm25: bool = Field(default=True, description="Enable BM25 lexical search")
    use_semantic: bool = Field(default=True, description="Enable semantic search")
    use_reranking: bool = Field(default=True, description="Enable cross-encoder reranking")
    use_diversity: bool = Field(default=True, description="Apply diversity penalty to avoid redundancy")

    bm25_weight: float = Field(default=0.3, ge=0.0, le=1.0, description="Weight for BM25 in RRF")
    semantic_weight: float = Field(default=0.7, ge=0.0, le=1.0, description="Weight for semantic in RRF")
    rerank_weight: float = Field(default=0.5, ge=0.0, le=1.0, description="Weight for reranking in final score")

    expand_query: bool = Field(default=True, description="Expand query with related terms")
    max_expansions: int = Field(default=3, ge=1, le=10, description="Max related terms to add")

    diversity_threshold: float = Field(default=0.85, ge=0.0, le=1.0, description="Similarity threshold for diversity penality")
    deversity_penality_strength: float = Field(default=0.5, ge=0.0, le=1.0, description="How much to penalize similar chunks")

    chunk_metadata: list[ChunkMetadata] = Field(default_factory=list, description="Metadata for each chunk")

    def validate_dimensions(self) -> bool:
        """Verify embeddings dimension consistency."""
        if not self.embeddings:
            return False
        first_dim = len(self.embeddings[0])
        return all(len(e) == first_dim for e in self.embeddings)
    
    def validate_consistency(self) -> bool:
        """Verify chunks and embeddings counts match."""
        return len(self.chunks) == len(self.embeddings)
    
    def validate_weights(self) -> bool:
        """Verify weights sum to reasonable values."""
        return 0.0 < (self.bm25_weight + self.semantic_weight) <= 2.0
    
class RetrieverOutput(ToolOutput):

    results: list[RetrieverResult] = Field(default_factory=list, description="Ranked list of relevant chunks with detailed scoring")
    results_count: int = Field(default=0, description="Number of results returned")
    query_expanded: bool = Field(default=False, description="Whether query was expanded")
    expanded_query_terms: list[str] = Field(default_factory=list, description="Terms added during expansion")
    reranking_applied: bool = Field(default=False, description="Whether reranking was applied")
    processing_stages: dict = Field(
        default_factory=dict,
        description="Stats from each processing stage: {'bm25': {...}, 'semantic': {...}, 'rrf': {...}, ...}"
    )