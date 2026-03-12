import time
from app.processors.base import BaseProcessor
from app.models.data_item import DataItem
from app.utils.logging import get_logger
from app.config import SIMULATED_DELAY

logger = get_logger("TextProcessor")

class TextProcessor(BaseProcessor):
    """A concrete processor for text-based data."""
    
    def process(self, item: DataItem) -> str:
        """Processes a single text item with a log and a short delay."""
        logger.info(f"Processing item {item.id}: {item.content[:20]}...")
        # Simulate some minor work
        time.sleep(SIMULATED_DELAY)
        
        # Transform the content
        processed_content = f"PROCESSED[{item.id}]: {item.content.upper()}"
        
        # Update metadata
        item.metadata['processed_at'] = time.time()
        
        return processed_content
