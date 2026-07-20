import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from optimized_data_processor import OptimizedDataProcessor


def test_processing_benchmark_optimized(benchmark):
    sample_file = os.path.join(os.path.dirname(__file__), "..", "sample_products.json")
    with open(sample_file) as f:
        data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {"test_dispensary": data.get("data", {}).get("products", [])}

    def process_data():
        return processor.process_menu_data(menu_items)

    result = benchmark(process_data)
    assert len(result) > 0
