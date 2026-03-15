import os
import time
import logging
from concurrent_processor import ConcurrentMenuProcessor

logging.basicConfig(level=logging.INFO)
os.environ['RATE_LIMIT'] = '0'

def mock_process_func(location):
    # Simulate network latency
    time.sleep(0.05)
    return True

def run_benchmark():
    locations = [{'slug': f'loc-{i}', 'type': 'dispensary'} for i in range(100)]

    # Ensure rate_limit=0
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)

    start_time = time.time()
    results = processor.process_locations(locations, mock_process_func)
    end_time = time.time()

    duration = end_time - start_time
    print("Concurrency Benchmark (100 items, 10 workers, 0.05s latency)")
    print(f"Time taken: {duration:.4f} seconds")
    print(f"Items processed: {len(results)}")

if __name__ == "__main__":
    run_benchmark()
