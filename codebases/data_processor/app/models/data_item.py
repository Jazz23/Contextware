from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class DataItem:
    """A model representing a single data item to be processed."""
    id: str
    content: str
    timestamp: datetime = datetime.now()
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
