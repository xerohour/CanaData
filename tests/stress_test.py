import time
import pytest
from concurrent_processor import ConcurrentMenuProcessor

def test_stress_concurrency():
    processor = ConcurrentMenuProcessor(max_workers=50, rate_limit=0.01)
    locations = [{'slug': f'loc_{i}', 'type': 'dispensary'} for i in range(500)]

    def process_func(loc):
        time.sleep(0.01)
        if loc['slug'] == 'loc_250':
            raise Exception("Simulated Failure")
        return True

    start_time = time.time()
    processor.process_locations(locations, process_func)
    end_time = time.time()

    print(f"Processed 500 locations with 50 workers in {end_time - start_time:.2f} seconds")
    print(f"Errors encountered: {len(processor.errors)}")

if __name__ == '__main__':
    test_stress_concurrency()
