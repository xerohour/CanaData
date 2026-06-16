import tracemalloc
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from optimized_data_processor import OptimizedDataProcessor
from CanaData import CanaData

def test_memory_legacy():
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    scraper = CanaData(optimize_processing=False, interactive_mode=False)
    products = data.get('data', {}).get('products', [])

    tracemalloc.start()
    for item in products:
        scraper.flatten_dictionary(item)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Assert memory usage is within a reasonable bound (e.g. < 5MB)
    assert peak < 5 * 1024 * 1024
    print(f"\nLegacy peak memory: {peak / 1024 / 1024:.2f} MB")

def test_memory_optimized():
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {'test_dispensary': data.get('data', {}).get('products', [])}

    tracemalloc.start()
    processor.process_menu_data(menu_items)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Assert memory usage is within a reasonable bound (e.g. < 20MB)
    assert peak < 20 * 1024 * 1024
    print(f"\nOptimized peak memory: {peak / 1024 / 1024:.2f} MB")
