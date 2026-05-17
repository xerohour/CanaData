import pytest
import time
import os
import sys
import psutil
import json

# Ensure root directory is in path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_throughput_benchmark_legacy(benchmark):
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    # 50 items
    products = data.get('data', {}).get('products', [])
    scraper = CanaData(optimize_processing=False, interactive_mode=False)

    def process_legacy():
        flattened = []
        for item in products:
            flattened.append(scraper.flatten_dictionary(item))
        return flattened

    result = benchmark(process_legacy)
    assert len(result) > 0

def test_throughput_benchmark_optimized(benchmark):
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    # 50 items
    products = data.get('data', {}).get('products', [])
    processor = OptimizedDataProcessor(max_workers=4)

    def process_optimized():
        return processor.process_menu_data({'test_location': products})

    result = benchmark(process_optimized)
    assert len(result) > 0
