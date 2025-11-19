from abc import ABC, abstractmethod
from pydantic import BaseModel

class ToolInput(BaseModel):
    """
    Base class for tool inputs.
    """
    pass

class ToolOutput(BaseModel):
    """
    Base class for tool output.
    """
    success: bool = True
    error_message: str = ""

class Tool(ABC):
    """
    Abstract base class that call tools inherit from.
    
    Every tool must:
      1. Have a name
      2. Accept input via execute()
      3. Return output via execute()
      4. Handle errors gracefully
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Tool name.
        Used for logging and identification.
        """
        pass

    @abstractmethod
    def execute(self, input_data: ToolInput) -> ToolOutput:
        """
        Execute the tool's primary function.
        Args:
            input_data: Input data for this tool (must be ToolInput subclass)

        Returns:
            ToolOutput: Result of execution (must be ToolOutput subclass)
        Raises:
            ToolError: If execution fails (or subclass like FileProcessingError)
        """
        pass



