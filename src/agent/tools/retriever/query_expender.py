import numpy as np
from sentence_transformers import SentenceTransformer
from src.logging_config import get_logger
from src.agent.errors import ToolError

class QueryExpansionError(ToolError):
    """Raise when query expansion fails."""
    pass

class QueryExpander:
    """
    Query expansion using semantic similarity.
    Finds related terms from document chunks that help improve seach recall.
    
    Strategy:
      - Embed the query
      - Find most similar chunks
      - Extract key terms from those chunks
      - Add them to expand the search
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.logger = get_logger(__name__)
        self.model_name = model_name
        self._model = None

    def _load_model(self) -> SentenceTransformer:
        if self._model is None:
            try:
                self.logger.debug(f"Loading embedding model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                raise QueryExpansionError(
                    f"Failed to load model {self.model_name}: {str(e)}"
                ) from e
        return self._model
    
    def expand(self,
               query: str,
               chunks: list[str],
               embeddings: list[list[float]],
               max_expansions: int = 3,
               ) -> list[str]:
        """
        Expand query with semantically related terms from chunks.

        Args:
            query: Original user query
            chunks: List of document chunks
            embeddings: Pre-computed embeddings for chunks
            max_expansions: Maximum number of terms to add

        Returns:
            List of expanded query terms (includes original query)
        """
        try:
            if not chunks or not embeddings:
                self.logger.warning("Cannot expand query with empty chunks/embeddings")
                return [query]
            if len(chunks) != len(embeddings):
                raise QueryExpansionError("Chunks and embedding count mismatch")
            
            self.logger.debug(f"Expanding query: '{query}'")
            model = self._load_model()

            query_embedding = model.encode([query], convert_to_tensor=False)[0]
            query_vec = np.array(query_embedding, dtype=np.float32)

            similarities = []
            for i, chunk_embedding in enumerate(embeddings):
                chunk_vec = np.array(chunk_embedding, dtype=np.float32)
                # Cosine similarity
                similarity = np.dot(query_vec, chunk_vec) / (
                    np.linalg.norm(query_vec) * np.linalg.norm(chunk_vec) + 1e-8
                )
                similarities.append((i, similarity))
            top_indices = sorted(similarities, key=lambda x: x[1], reverse=True)[:max_expansions]
            # Extract meaningful terms from top chunks
            # Simple strategy: take first few words from each top chunk
            expanded_terms = [query]
            for idx, similarity in top_indices:
                chunk = chunks[idx]
                # Extract first few words, but skip very short ones
                words = [w for w in chunk.split()[:5] if len(w) > 3]

                if words:
                    # Add the first meaningful phrase from this chunk
                    term = " ".join(words[:2])
                    expanded_terms.append(term)
            self.logger.debug(
                f"Query expanded: original='{query}' -> "
                f"{len(expanded_terms)} total terms"
            )
            return expanded_terms[:1 + max_expansions] # Original + max_expansions
        
        except QueryExpansionError:
            raise
        except Exception as e:
            self.logger.error(f"Query expansion failed: {str(e)}")
            return [query] # Fall back to original query

