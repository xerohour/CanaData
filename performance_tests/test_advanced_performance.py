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
    products = data.get('data', {}).get('products', [])
    items_with_location = [{**item, '_location_id': 'test'} for item in products] * 50

    def process_data():
        return processor._flatten_batch(items_with_location.copy())

    result = benchmark(process_data)
    assert len(result) > 0
