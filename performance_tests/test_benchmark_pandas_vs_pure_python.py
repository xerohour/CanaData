import json
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimized_data_processor import OptimizedDataProcessor

def test_pandas_normalization(benchmark):
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)
    items = data.get('data', {}).get('products', []) * 10

    def run_pandas():
        df = pd.json_normalize(items, sep='.')
        return df.to_dict('records')

    benchmark(run_pandas)

def test_pure_python_normalization(benchmark):
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)
    items = data.get('data', {}).get('products', []) * 10
    processor = OptimizedDataProcessor()

    def run_pure_python():
        flat_items = [processor._flatten_dictionary_custom(item) for item in items]
        keys = set()
        for item in flat_items:
            keys.update(item.keys())
        template = dict.fromkeys(keys, 'None')
        return [{**template, **item} for item in flat_items]

    benchmark(run_pure_python)
