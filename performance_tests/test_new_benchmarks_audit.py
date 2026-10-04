import json
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_flatten_dictionary_latency(benchmark):
    scraper = CanaData(interactive_mode=False)
    with open('sample_products.json', 'r') as f:
        mock_data = json.load(f)
    items = mock_data.get('data', {}).get('products', [])
    if not items:
        items = [{"id": 1, "brand": {"name": "Test Brand"}, "prices": {"gram": 10}}]

    def run_flatten():
        for item in items:
            scraper.flatten_dictionary(item.copy())

    benchmark(run_flatten)

def test_optimized_processor_throughput(benchmark):
    processor = OptimizedDataProcessor()
    with open('sample_products.json', 'r') as f:
        mock_data = json.load(f)
    items = mock_data.get('data', {}).get('products', [])
    if not items:
        items = [{"id": 1, "brand": {"name": "Test Brand"}, "prices": {"gram": 10}}]

    df = pd.json_normalize(items)
    # Duplicate to create a larger batch
    df = pd.concat([df] * 10, ignore_index=True)

    def run_optimized():
        processor._handle_remaining_nesting(df.copy())

    benchmark(run_optimized)
