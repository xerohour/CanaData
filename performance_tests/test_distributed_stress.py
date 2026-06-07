import concurrent.futures
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_high_concurrency_lock_contention():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = []

    def worker_task(item_id):
        start = time.perf_counter()
        with scraper._menu_data_lock:
            scraper.allMenuItems.append({'id': item_id})
        end = time.perf_counter()
        return end - start

    num_workers = 100
    latencies = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(worker_task, i) for i in range(1000)]
        for future in concurrent.futures.as_completed(futures):
            latencies.append(future.result())

    assert len(scraper.allMenuItems) == 1000
    avg_latency = sum(latencies) / len(latencies)
    print(f"\nAverage lock acquisition + append latency: {avg_latency*1000:.4f} ms")
    assert avg_latency < 0.1 # Should be very fast, but tests framework
