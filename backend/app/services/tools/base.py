from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    """Base class for all tools."""
    
    name: str
    description: str
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the tool logic."""
        pass
    
    def to_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for the tool."""
        # This should return the schema in the format Ollama expects
        # For now, we'll keep it simple or implement per tool
        pass
