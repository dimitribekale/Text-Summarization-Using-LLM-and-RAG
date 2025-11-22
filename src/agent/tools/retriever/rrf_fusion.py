import numpy as np
from src.logging_config import get_logger

class RRFFusion:
    """
    Reciprocal Rank Fusion (RRF) combiner.
    Merge BM25 and semantic rankings into a single score.
    """
    def __init__(self, k: int = 60):
        """
        Args:
            k: Constant in RRF formula (standard value is 60)
               Higher k = rankings more equal, lower k = best ranks dominate
        """
        self.logger = get_logger(__name__)
        self.k = k

    def fuse(self,
             bm25_scores: list[float],
             semantic_scores: list[float],
             bm25_weight: float = 0.3,
             semantic_weight: float = 0.7
             ) -> np.ndarray:
        """
        Fuse two ranking scores using RRF.
        Args:
            bm25_scores: List of BM25 relevance scores
            semantic_scores: List of semantic similarity scores
            bm25_weight: Weight for BM25 ranking (0.0 - 1.0)
            semantic_weight: Weight for semantic ranking (0.0 - 1.0)
        Returns:
            List of fused scores combining both methods.
        """
        try:
            if len(bm25_scores) != len(semantic_scores):
                raise ValueError("Score lists must have same length")
            n = len(bm25_scores)
            # Convert scores to rankings (0 = best, n-1 = worst)
            # argsort gives indices, second argsort gives ranks
            bm25_ranks = np.argsort(np.argsort(bm25_scores)[::-1])[::-1]
            semantic_ranks = np.argsort(np.argsort(semantic_scores)[::-1])[::-1]

            fused_scores = []
            for i in range(n):
                rrf_bm25 = 1.0 / (self.k + bm25_ranks[i])
                rrf_semantic = 1.0 / (self.k + semantic_ranks[i])

                fused = (bm25_weight * rrf_bm25) + (semantic_weight * rrf_semantic)
                fused_scores.append(fused)

            self.logger.debug(
                f"RRF fusion complete. Mean: {np.mean(fused_scores):.6f},"
                f"Max: {np.max(fused_scores):.6f}"
            )
            return np.array(fused_scores)
        
        except Exception as e:
            self.logger.error(f"RRF fusion failed: {str(e)}")
            return np.array([0.0] * len(bm25_scores))