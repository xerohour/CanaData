import sys
import os
import psutil
import cProfile
import pstats
import io
import time
import json
import gc

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def load_sample_data():
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    if os.path.exists(sample_file):
        with open(sample_file, 'r') as f:
             return json.load(f)
    return None

def profile_memory_usage():
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / (1024 * 1024) # MB

    data = load_sample_data()
    if not data:
        print("No sample data found.")
        return

    products = data.get('data', {}).get('products', []) * 10 # 10x multiplier for stress

    print(f"Initial Memory: {start_memory:.2f} MB")

    # Profile Processor
    processor = OptimizedDataProcessor()
    menu_items = {'test_loc_1': products, 'test_loc_2': products, 'test_loc_3': products}

    start_time = time.time()

    # Capture cProfile
    pr = cProfile.Profile()
    pr.enable()

    result = processor.process_menu_data(menu_items)

    pr.disable()
    end_time = time.time()

    # Check for memory leaks by forcing GC
    gc.collect()
    end_memory = process.memory_info().rss / (1024 * 1024)

    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(20) # Top 20 slowest functions

    print(f"Time Taken: {end_time - start_time:.4f}s")
    print(f"Final Memory: {end_memory:.2f} MB")
    print(f"Memory Diff: {end_memory - start_memory:.2f} MB")
    print(f"\nProfiler Output:\n{s.getvalue()}")

if __name__ == '__main__':
    profile_memory_usage()
