from abc import ABC, abstractmethod
from typing import List, Any
from app.models.data_item import DataItem

class BaseProcessor(ABC):
    """Abstract base class for all data processors."""
    
    def __init__(self, name: str):
        self.name = name
        self.processed_count = 0

    @abstractmethod
    def process(self, item: DataItem) -> Any:
        """Processes a single DataItem. Must be implemented by subclasses."""
        pass

    def process_batch(self, items: List[DataItem]) -> List[Any]:
        """Processes a list of DataItems."""
        results = []
        for item in items:
            results.append(self.process(item))
            self.processed_count += 1
        return results
