import numpy as np
from rank_bm25 import BM25Okapi
from src.logging_config import get_logger

class BM25Scorer:

    def __init__(self):
        self.logger = get_logger(__name__)
        self._bm25_index = None
        self._cached_chunks = None

    def build_index(self, chunks: list[str]) -> None:
        """
        Build BM25 index from chunks.
        Uses caching: if chunks are same, reuse index.
        """
        if self._bm25_index is not None and self._cached_chunks == chunks:
            self.logger.debug("Reusing cached BM25 index")
            return
        
        self.logger.debug(f"Building index. Chunks type: {type(chunks)}, First chunk type: {type(chunks[0]) if chunks else 'empty'}")

        tokenized_chunks = [chunk.lower().split() for chunk in chunks]
        self._bm25_index = BM25Okapi(tokenized_chunks)
        self._cached_chunks = chunks
        self.logger.debug(f"Built BM25 index for {len(chunks)} chunks")

    def score(self, query: str, chunks: list[str]) -> list[float]:
        """
        Calculate BM25 scores for all chunks.
        
        Returns:
            List of BM25 scores (higher = more relevant)
        """
        try:
            self.build_index(chunks)
            query_tokens = query.lower().split()
            scores = self._bm25_index.get_scores(query_tokens)

            # Normalize scores to [0, 1]
            max_score = np.max(scores)
            if max_score > 0:
                scores = scores / max_score

            self.logger.debug(f"BM25 scoring complete. Mean: {np.mean(scores):.4f}, Max: {np.max(scores):.4f}")
            return scores
        except Exception as e:
            self.logger.error(f"BM25 scoring failed: {str(e)}")
            return [0.0] * len(chunks)