import numpy as np
from sentence_transformers import SentenceTransformer
from src.config import Config
from src.agent.tools.base import Tool
from src.agent.errors import ToolError
from src.agent.tools.embedder.base import EmbedderInput, EmbedderOutput
from src.logging_config import get_logger

class EmbeddinError(ToolError):
    """Raised when embedding fails."""
    pass

class Embedder(Tool):
    """
    Converts text chunks to vector embeddings.
    """
    def __init__(self, config: Config, logger=None):
        self.config = config
        self.model_name = config.embedding_model
        self.logger = logger or get_logger(__name__)
        self._model = None # Lazy load model

    @property
    def name(self) -> str:
        """Tool name"""
        return "Embedder"
    
    def _load_model(self) -> SentenceTransformer:
        if self._model is None:
            try:
                self.logger.debug(f"Loading embedding model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                raise EmbeddinError(
                    f"Failed to load model {self.model_name}: {str(e)}"
                ) from e
        return self._model
    
    def execute(self, input_data: EmbedderInput) -> EmbedderOutput:
        """
        Execute embeddings on text chunks.
        """
        try:
            if not input_data.chunks:
                raise EmbeddinError("Cannot embed empty list of chunks")
            
            self.logger.debug(f"Embedding {len(input_data.chunks)} chunks")
            model = self._load_model()
            embeddings = model.encode(input_data.chunks, convert_to_tensor=False)
            embeddings_list = [embedding.tolist() for embedding in embeddings]
            embedding_dim = len(embeddings_list[0]) if embeddings_list else 0

            self.logger.info(
                f"Successfully embedded {len(input_data.chunks)} chunks."
                f"Dimension: {embedding_dim}"
            )
            output = EmbedderOutput(
                success=True,
                embeddings=embeddings_list,
                embedding_dim=embedding_dim,
                chunks_embedded=len(input_data.chunks)
            )
            return output
        
        except EmbeddinError as e:
            self.logger.error(f"EmbeddingError: {str(e)}")
            return EmbedderOutput(
                success=False,
                error_message=str(e)
            )
        except Exception as e:
            self.logger.error(f"Unexpected error in Embedder: {str(e)}", exc_info=True)
            return EmbedderOutput(
                success=False,
                error_message=f"Unexpected error: {str(e)}"
            )