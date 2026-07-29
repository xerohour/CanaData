import pytest
import time
import sys
import os
import json
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimized_data_processor import OptimizedDataProcessor
from CanaData import CanaData

@pytest.fixture
def sample_data():
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    if not os.path.exists(sample_file):
        return None
    with open(sample_file, 'r') as f:
        data = json.load(f)
    return data.get('data', {}).get('products', []) * 10  # multiplier for benchmark

def test_optimized_flattening_latency(benchmark, sample_data):
    if not sample_data:
        pytest.skip("No sample data")
    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {'loc1': sample_data}

    def run_process():
        return processor.process_menu_data(menu_items)

    result = benchmark(run_process)
    assert len(result) > 0

def test_legacy_flattening_latency(benchmark, sample_data):
    if not sample_data:
        pytest.skip("No sample data")
    scraper = CanaData(optimize_processing=False, interactive_mode=False)

    def run_process():
        flattened = []
        for item in sample_data:
            flattened.append(scraper.flatten_dictionary(item))
        return flattened

    result = benchmark(run_process)
    assert len(result) > 0
