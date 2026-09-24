import cProfile
import io
import json
import os
import pstats
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor
from memory_profiler import profile

# Setup mock data for performance testing
mock_data = []
with open(os.path.join(os.path.dirname(__file__), '..', 'sample_products.json'), 'r') as f:
    mock_data = json.load(f)

def run_cpu_benchmark():
    scraper = CanaData(interactive_mode=False)
    # duplicate for scale
    items = mock_data.get('data', {}).get('products', []) * 10
    scraper.allMenuItems['test-listing'] = items

    start_time = time.time()
    scraper.organize_into_clean_list()
    print(f"Organize into clean list (flattening & Pandas operations) took {time.time() - start_time:.4f}s")

@profile
def run_memory_benchmark():
    scraper = CanaData(interactive_mode=False)
    # duplicate for scale
    items = mock_data.get('data', {}).get('products', []) * 10
    scraper.allMenuItems['test-listing'] = items

    # Process
    scraper.organize_into_clean_list()

if __name__ == '__main__':
    print("Running CPU profiling benchmark...")
    pr = cProfile.Profile()
    pr.enable()
    run_cpu_benchmark()
    pr.disable()

    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(30)
    print(s.getvalue())

    print("Running Memory profiling benchmark...")
    run_memory_benchmark()
