import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimized_data_processor import OptimizedDataProcessor

def test_large_nesting_performance(benchmark):
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    processor = OptimizedDataProcessor()

    # We will test the pure python flatten_all_items instead of pandas _handle_remaining_nesting
    items_with_location = []
    for _ in range(50):
        for item in data.get('data', {}).get('products', []):
            items_with_location.append({**item, '_location_id': 'loc1'})

    def process_data():
        return processor._flatten_all_items(items_with_location)

    result = benchmark(process_data)
    assert len(result) > 0
