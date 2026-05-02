import cProfile
import json
from memory_profiler import profile
import os
import sys

# Ensure root directory is in path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from optimized_data_processor import OptimizedDataProcessor
from CanaData import CanaData

def load_data():
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        return json.load(f)

@profile
def memory_profile_legacy(data):
    scraper = CanaData(optimize_processing=False, interactive_mode=False)
    products = data.get('data', {}).get('products', [])
    flattened = []
    for item in products:
        flattened.append(scraper.flatten_dictionary(item))
    return flattened

@profile
def memory_profile_optimized(data):
    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {'test_dispensary': data.get('data', {}).get('products', [])}
    return processor.process_menu_data(menu_items)

def cprofile_legacy():
    data = load_data()
    scraper = CanaData(optimize_processing=False, interactive_mode=False)
    products = data.get('data', {}).get('products', [])
    flattened = []
    for _ in range(100):
        for item in products:
            flattened.append(scraper.flatten_dictionary(item))

def cprofile_optimized():
    data = load_data()
    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {'test_dispensary': data.get('data', {}).get('products', []) * 100}
    processor.process_menu_data(menu_items)

if __name__ == '__main__':
    print("Running memory profiles...")
    data = load_data()
    print("\n--- Memory Profile: Legacy ---")
    memory_profile_legacy(data)
    print("\n--- Memory Profile: Optimized ---")
    memory_profile_optimized(data)

    print("\nRunning cProfile benchmarks...")
    print("\n--- cProfile: Legacy (100 iterations) ---")
    cProfile.run('cprofile_legacy()', sort='cumtime')
    print("\n--- cProfile: Optimized (100 batches) ---")
    cProfile.run('cprofile_optimized()', sort='cumtime')
