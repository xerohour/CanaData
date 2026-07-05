import os
import sys
import json
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimized_data_processor import OptimizedDataProcessor

def test_large_nesting_performance(benchmark):
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    processor = OptimizedDataProcessor()
    items = data.get('data', {}).get('products', [])
    items_large = items * 50
    mock_all_menu_items = {'test_loc': items_large}

    def process_data():
        return processor.process_menu_data(mock_all_menu_items)

    result = benchmark(process_data)
    assert len(result) > 0
