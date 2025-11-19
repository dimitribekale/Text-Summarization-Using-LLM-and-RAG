


class AgentError(Exception):
    """
    Base exception for all agent-related errors
    """
    pass

class ToolError(AgentError):
    """
    Tool failed to execute.
    This is raised when a tool encounters an error
    during execution.
    """
    pass

class FileProcessingError(ToolError):
    """
    File processing (reading/chunking) failed.
    Use cases:
    - PDF is corrupted
    - File doesn't exist
    - File is too large
    - Text extraction failed
    """
    pass

class EmbeddingError(ToolError):
    """
    Creating embeddings failed.
    """
    pass

class RetrievalError(ToolError):
    """
    Retrieval/ search failed
    """
    pass

class LLMError(ToolError):
    """
    LLM (Ollama) operation failed
    """
    pass

class OllamaConnectionError(LLMError):
    """
    Connection to Ollama server failed.
    """
    pass

class OllamaTimeoutError(LLMError):
    """
    Ollama took too long to respond.
    """
    pass

class ConfigurationError(AgentError):
    """
    Configuration is invalid or incomplete.
    """
    pass

class ValidationError(AgentError):
    """
    Input validation failed.
    
    - Empty input
    - Wrong data type
    - Invalid parameter
    """
    pass