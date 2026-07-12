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
    items = items * 50

    def process_data():
        flattened = []
        for item in items:
            flattened.append(processor._flatten_dictionary_custom(item))
        return processor._normalize_data(flattened)

    result = benchmark(process_data)
    assert len(result) > 0
