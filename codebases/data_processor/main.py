import time

class Processor:
    """A class to process data with simulated delay and logging."""
    
    def __init__(self, name: str):
        self.name = name
        self.processed_count = 0

    def log(self, message: str):
        print(f"[{self.name}] {message}")

    def process_item(self, item: str):
        """Processes a single item with a log and a short delay."""
        self.log(f"Processing item: {item}")
        # Simulate some minor work
        time.sleep(0.05)
        self.processed_count += 1
        return f"PROCESSED: {item}"

    def process_all(self, items: list[str]):
        """Processes a list of items and returns the results."""
        self.log(f"Starting batch process of {len(items)} items")
        results = [self.process_item(item) for item in items]
        self.log(f"Batch process complete. Total processed: {self.processed_count}")
        return results

def top_level_func():
    """A top-level helper function for basic greetings."""
    print("Top level function called.")

def main():
    """Main entry point for the data processor utility."""
    print("--- Data Processor Initialization ---")
    
    # Run the top-level helper
    top_level_func()
    
    # Create and run a processor
    items = ["Apple", "Banana", "Cherry", "Date"]
    processor = Processor("DataWorker-1")
    
    results = processor.process_all(items)
    
    print("\nFinal Processing Results:")
    for res in results:
        print(f"  - {res}")
        
    print(f"\nFinal status of '{processor.name}': {processor.processed_count} items handled.")
    print("--- Data Processor Finished ---")

if __name__ == "__main__":
    main()
