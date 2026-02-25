import sys
import os

# Add the current directory to sys.path so we can import 'app'
# This is a bit hacky for a script, but common in testing codebases.
# We go up two levels because this script is in codebases/data_processor/app/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.data_item import DataItem
from app.processors.text import TextProcessor
from app.utils.logging import get_logger
from app.config import VERSION

logger = get_logger("Main")

def main():
    """Main entry point for the improved data processor."""
    logger.info(f"--- Data Processor v{VERSION} Initialization ---")
    
    # Create some mock data items
    raw_data = ["Apple", "Banana", "Cherry", "Date"]
    items = [DataItem(id=str(i), content=val) for i, val in enumerate(raw_data)]
    
    # Initialize the processor
    processor = TextProcessor("TextWorker-1")
    
    # Process the batch
    results = processor.process_batch(items)
    
    logger.info("\nFinal Processing Results:")
    for res in results:
        logger.info(f"  - {res}")
        
    logger.info(f"\nFinal status of '{processor.name}': {processor.processed_count} items handled.")
    logger.info("--- Data Processor Finished ---")

if __name__ == "__main__":
    main()
