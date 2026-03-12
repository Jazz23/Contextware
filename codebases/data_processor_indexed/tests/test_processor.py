import unittest
import sys
import os

# Add the root of the data_processor to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.data_item import DataItem
from app.processors.text import TextProcessor

class TestTextProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = TextProcessor("TestWorker")

    def test_process_item(self):
        item = DataItem(id="test-1", content="hello world")
        result = self.processor.process(item)
        self.assertEqual(result, "PROCESSED[test-1]: HELLO WORLD")
        self.assertIn("processed_at", item.metadata)

    def test_process_batch(self):
        items = [
            DataItem(id="1", content="apple"),
            DataItem(id="2", content="banana")
        ]
        results = self.processor.process_batch(items)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], "PROCESSED[1]: APPLE")
        self.assertEqual(results[1], "PROCESSED[2]: BANANA")
        self.assertEqual(self.processor.processed_count, 2)

if __name__ == "__main__":
    unittest.main()
