import numpy as np
from sentence_transformers import SentenceTransformer
from src.logging_config import get_logger
from src.agent.errors import ToolError

class SemanticSearchError(ToolError):
    """Raised when semantic search fails."""
    pass

class SemanticSearcher:
    """
    Semantic search scorer.
    Measures meaning-based similarity using embedding vectors.
    """
    def __init__(self, model_name: str ="all-MiniLM-L6-v2"):
        self.logger = get_logger(__name__)
        self.model_name = model_name
        self._model = None

    def _load_model(self) -> SentenceTransformer:
        if self._model is None:
            try:
                self.logger.debug(f"Loading embedding model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                raise SemanticSearchError(
                    f"Failed to load model {self.model_name}: {str(e)}"
                ) from e
        return self._model
    
    def score(self, query: str, embeddings: list[list[float]]) -> np.ndarray:
        """
        Uses cosine similarity between query and chunk embeddings
        to calculate semantic scores.
        Returns:
            List of similarity scores normalzied to [0, 1]
        """
        try:
            if len(embeddings) == 0:
                return np.array([])
            model = self._load_model()
            query_embedding = model.encode([query], convert_to_tensor=False)[0]
            scores =[]
            for chunk_embedding in embeddings:
                query_vec = np.array(query_embedding, dtype=np.float32)
                chunk_vec = np.array(chunk_embedding, dtype=np.float32)

                cosine_similarity = np.dot(query_vec, chunk_vec) / (
                    np.linalg.norm(query_vec) * np.linalg.norm(chunk_vec) + 1e-8
                )
                # Normalize from [-1, 1] t0 [0, 1]
                normalized_score = (cosine_similarity + 1) / 2
                scores.append(float(normalized_score))

            self.logger.debug(
                f"Semantic scoring complete. Mean: {np.mean(scores):.4f}, "
                f"Max: {np.max(scores):.4f}" 
            )
            return np.array(scores)
        
        except SemanticSearchError:
            raise
        except Exception as e:
            self.logger.error(f"Semantic scoring failed: {str(e)}")
            return np.array([0.0] * len(embeddings))