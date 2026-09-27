import json
import os
import sys
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_core_flatten_benchmark(benchmark):
    scraper = CanaData(interactive_mode=False)
    sample_file = os.path.join(os.path.dirname(__file__), "..", "sample_products.json")
    with open(sample_file) as f:
        data = json.load(f)

    # Use first product to ensure we are testing real application logic
    item = data.get("data", {}).get("products", [])[0]

    def run_flatten():
        # Modify the ID uniquely per round to avoid key collision/caching
        item_copy = item.copy()
        item_copy["id"] = str(uuid.uuid4())
        return scraper.flatten_dictionary(item_copy)

    result = benchmark(run_flatten)
    assert result is not None

def test_core_optimized_processor(benchmark):
    sample_file = os.path.join(os.path.dirname(__file__), "..", "sample_products.json")
    with open(sample_file) as f:
        data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=2)
    # create realistic batch dataset
    items = data.get("data", {}).get("products", [])

    def process_data():
        menu_items = {str(uuid.uuid4()): items.copy()}
        return processor.process_menu_data(menu_items)

    result = benchmark(process_data)
    assert len(result) > 0
