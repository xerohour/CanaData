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

    # We create a large nested dataset
    raw_products = data.get('data', {}).get('products', [])
    large_dataset = {'loc1': raw_products * 50}

    def process_data():
        return processor.process_menu_data(large_dataset)

    result = benchmark(process_data)
    assert len(result) > 0
