import time
import sys
import os
sys.path.append(os.path.abspath('.'))
from concurrent_processor import ConcurrentMenuProcessor

def mock_process_func(location):
    time.sleep(0.01) # Simulate minimal processing delay
    return {"id": location["id"], "status": "processed"}

def main():
    locations = [{"id": f"loc_{i}", "slug": f"slug_{i}"} for i in range(100)]

    # Test with different max_workers
    for workers in [1, 5, 10, 20]:
        processor = ConcurrentMenuProcessor(max_workers=workers, rate_limit=0)
        start = time.time()
        results = processor.process_locations(locations, mock_process_func)
        end = time.time()
        print(f"Workers: {workers:2d} | Time: {end - start:.3f}s | Processed: {len(results)}")

if __name__ == "__main__":
    main()
