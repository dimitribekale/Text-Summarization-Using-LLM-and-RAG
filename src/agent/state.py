from typing import Any, Dict
from pydantic import BaseModel


class WorkflowState(BaseModel):
    """
    Represent the state of workflow execution.
    This object is passed between tools, accumulating results
    as each tool completes.
    
    """
    files_processed: int = 0
    files_failed: int = 0
    total_files: int = 0
    results: list[Dict[str, Any]] = []
    errors: list[Dict[str, str]] = []