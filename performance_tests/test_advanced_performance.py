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
    df = pd.json_normalize(data.get('data', {}).get('products', []))
    df = pd.concat([df] * 50, ignore_index=True)

    def process_data():
        return processor._handle_remaining_nesting(df.copy())

    result = benchmark(process_data)
    assert len(result) > 0
