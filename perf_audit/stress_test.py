import time
import sys
import os
import threading
sys.path.append(os.path.abspath('.'))
from concurrent_processor import ConcurrentMenuProcessor

def mock_heavy_process_func(location):
    # Simulate CPU bound work and sleep
    sum(i * i for i in range(10000))
    time.sleep(0.05)
    return {"id": location["id"], "thread": threading.get_ident()}

def main():
    locations = [{"id": f"loc_{i}", "slug": f"slug_{i}"} for i in range(500)]

    # High worker count stress test
    workers = 100
    print(f"Starting stress test with {workers} workers for {len(locations)} items...")
    processor = ConcurrentMenuProcessor(max_workers=workers, rate_limit=0)
    start = time.time()
    results = processor.process_locations(locations, mock_heavy_process_func)
    end = time.time()

    unique_threads = len(set(r.get("thread") for r in results.values() if r))
    print(f"Stress Test Complete. Time: {end - start:.3f}s")
    print(f"Processed: {len(results)} | Errors: {len(processor.errors)} | Unique Threads Used: {unique_threads}")

if __name__ == "__main__":
    main()
