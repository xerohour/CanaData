import threading
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CanaData import CanaData
from concurrent_processor import ConcurrentMenuProcessor

def test_extreme_concurrency_lock_contention(benchmark):
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def worker(worker_id):
        for i in range(200):
            with scraper._menu_data_lock:
                # Simulate memory allocations inside lock
                time.sleep(0.00005)
                scraper.allMenuItems[f"{worker_id}_{i}"] = [{"id": i}]

    def run_stress():
        threads = []
        for i in range(50):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 10000

def test_concurrent_processor_rate_limit_contention(benchmark):
    processor = ConcurrentMenuProcessor(max_workers=50, rate_limit=0.001)
    locations = [{"slug": f"loc_{i}"} for i in range(200)]

    def mock_process(loc):
        # Simulate network delay
        time.sleep(0.001)
        return {"status": "ok"}

    def run_processor_stress():
        return processor.process_locations(locations, mock_process)

    result = benchmark(run_processor_stress)
    assert len(result) == 200

def test_failure_injection_resilience():
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)
    locations = [{"slug": f"loc_{i}"} for i in range(50)]

    def flaky_process(loc):
        if int(loc["slug"].split("_")[1]) % 5 == 0:
            raise ValueError("Simulated network crash")
        return {"data": True}

    _ = processor.process_locations(locations, flaky_process)
    assert len(processor.results) == 40
    assert len(processor.errors) == 10
