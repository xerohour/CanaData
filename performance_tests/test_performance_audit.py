import pytest
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor
import time
import os
import json

def test_legacy_flatten(benchmark):
    scraper = CanaData(optimize_processing=False, interactive_mode=False)
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)
    products = data.get('data', {}).get('products', [])

    def process():
        return [scraper.flatten_dictionary(item) for item in products]

    benchmark(process)

def test_optimized_flatten(benchmark):
    processor = OptimizedDataProcessor()
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)
    menu_items = {'test_loc': data.get('data', {}).get('products', [])}

    def process():
        return processor.process_menu_data(menu_items)

    benchmark(process)
