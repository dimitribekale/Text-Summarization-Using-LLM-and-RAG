import numpy as np
from sentence_transformers import CrossEncoder
from src.logging_config import get_logger
from src.agent.errors import ToolError

class CrossEncoderError(ToolError):
    """Raised when reranking fails."""
    pass 

class Reranker:
    """
    Cross-encoder reranker for accurate relevance scoring.
    Unlike dual-encoders (which embed query and chunks separately),
    cross-encoders take query-chunk pairs and directly output relevance scores.
    """
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.logger = get_logger(__name__)
        self.model_name = model_name
        self._model = None
    
    def _load_model(self) -> CrossEncoder:
        if self._model is None:
            try:
                self.logger.debug(f"Loading cross-encoder: {self.model_name}")
                self._model = CrossEncoder(self.model_name)
            except Exception as e:
                raise CrossEncoderError(
                    f"Failed to load cross-encoder {self.model_name}: {str(e)}"
                ) from e
        return self._model
    
    def rerank(self, query: str, chunks: list[str]) -> list[float]:
        """
        Rerank chunks using cross-encoder.
        Args:
            query: User query string
            chunks: List of document chunks to rerank
        Returns:
            List of relevance scores normalized to [0, 1]
        """
        try:
            if not chunks:
                return []
            self.logger.debug(f"Reranking {len(chunks)} chunks with cross-encoder")
            model = self._load_model()
            pairs = [[query, chunk] for chunk in chunks]
            scores = model.predict(pairs)
            # Normalize to [0, 1] range for consistency
            scores_min = np.min(scores)
            scores_max = np.max(scores)
            if scores_max > scores_min:
                normalized_scores = (scores - scores_min) / (scores_max - scores_min)
            else:
                # All scores are same, uniform distribution
                normalized_scores = np.ones_like(scores) * 0.5
            self.logger.debug(
                f"Cross-encoder reranking complete. Mean: {np.mean(normalized_scores):.4f}, "
                f"Max: {np.max(normalized_scores):.4f}"
            )
            return normalized_scores.tolist()

        except CrossEncoderError:
            raise
        except Exception as e:
            self.logger.error(f"Cross-encoder reranking failed: {str(e)}")
            # Fallback: return uniform scores
            return [0.5] * len(chunks)