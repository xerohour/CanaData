import cProfile
import pstats
import io
import time
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from concurrent_processor import ConcurrentMenuProcessor
from optimized_data_processor import OptimizedDataProcessor

def run_flatten_benchmark():
    processor = OptimizedDataProcessor()

    # Generate some mock nested data
    mock_item = {
        "id": 1,
        "name": "Test Item",
        "brand": {"id": 123, "name": "Brand"},
        "prices": {"gram": 10.0, "eighth": 35.0},
        "tags": ["indica", "flower"]
    }
    mock_data = {"test_location": [mock_item] * 10000}

    start_time = time.time()
    pr = cProfile.Profile()
    pr.enable()

    processor.process_menu_data(mock_data)

    pr.disable()
    end_time = time.time()

    print(f"Flattening 10,000 items took {end_time - start_time:.4f} seconds")

    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(20)
    print(s.getvalue())

if __name__ == "__main__":
    run_flatten_benchmark()
