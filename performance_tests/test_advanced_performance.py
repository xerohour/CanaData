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
    items = data.get('data', {}).get('products', [])
    items = items * 50

    def process_data():
        # First flatten the list so we have valid dictionaries
        flat_items = processor._fallback_flattening(items)
        return processor._handle_remaining_nesting(flat_items)

    result = benchmark(process_data)
    assert len(result) > 0
