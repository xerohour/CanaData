import cProfile
import io
import json
import pstats
import time
import os

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from memory_profiler import profile
from optimized_data_processor import OptimizedDataProcessor

# Setup mock data for performance testing
mock_data = []
sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
if not os.path.exists(sample_file):
    mock_data = {"data": {"products": [{"id": 1, "name": "test"}] * 100}}
else:
    with open(sample_file, 'r') as f:
        mock_data = json.load(f)

def run_flatten_benchmark():
    processor = OptimizedDataProcessor(max_workers=4)
    start_time = time.time()
    menu_items = {'test_dispensary': mock_data.get('data', {}).get('products', []) * 50}
    processor.process_menu_data(menu_items)
    print(f"Flattening took {time.time() - start_time:.4f}s")

@profile
def run_memory_benchmark():
    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {'test_dispensary': mock_data.get('data', {}).get('products', []) * 50}
    processor.process_menu_data(menu_items)

if __name__ == '__main__':
    print("Running scalability flattening benchmark...")
    pr = cProfile.Profile()
    pr.enable()
    run_flatten_benchmark()
    pr.disable()

    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(20)
    print(s.getvalue())

    print("Running scalability memory benchmark...")
    run_memory_benchmark()
