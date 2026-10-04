import cProfile
import io
import json
import pstats
import time
from memory_profiler import profile
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor
import pandas as pd

with open('sample_products.json', 'r') as f:
    mock_data = json.load(f)
items = mock_data.get('data', {}).get('products', [])

def run_flatten_benchmark():
    scraper = CanaData(interactive_mode=False)
    for item in items:
        scraper.flatten_dictionary(item)

def run_optimized_benchmark():
    processor = OptimizedDataProcessor()
    df = pd.json_normalize(items)
    processor._handle_remaining_nesting(df)

@profile
def run_memory_benchmark():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems['test-listing'] = items * 10
    scraper.organize_into_clean_list()

if __name__ == '__main__':
    print("Running flattening benchmark...")
    pr = cProfile.Profile()
    pr.enable()
    run_flatten_benchmark()
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(20)
    print(s.getvalue())

    print("Running optimized processing benchmark...")
    pr2 = cProfile.Profile()
    pr2.enable()
    run_optimized_benchmark()
    pr2.disable()
    s2 = io.StringIO()
    ps2 = pstats.Stats(pr2, stream=s2).sort_stats('cumulative')
    ps2.print_stats(20)
    print(s2.getvalue())

    print("Running memory benchmark...")
    run_memory_benchmark()
