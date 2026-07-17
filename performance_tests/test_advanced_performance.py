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
    mock_data = {'loc_1': items}

    def process_data():
        return processor.process_menu_data(mock_data)

    result = benchmark(process_data)
    assert len(result) > 0
