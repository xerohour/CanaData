import time
import threading
from concurrent_processor import ConcurrentMenuProcessor

def dummy_process(loc):
    return True

processor = ConcurrentMenuProcessor(max_workers=50, rate_limit=0.01)
locations = [{'slug': f'loc-{i}'} for i in range(100)]

start = time.time()
processor.process_locations(locations, dummy_process)
end = time.time()

print(f"Concurrency Benchmark: {end - start:.4f} seconds")
