import pytest
import threading
from CanaData import CanaData
import time
import uuid

def test_audit_high_concurrency(benchmark):
    scraper = CanaData(cache_enabled=False, optimize_processing=True, max_workers=50)

    def worker():
        worker_id = str(uuid.uuid4())
        for i in range(500):
            with scraper._menu_data_lock:
                scraper.allMenuItems[f"test_{worker_id}_{i}"] = [{'id': i, 'name': 'test'}]

    def run_concurrently():
        scraper.allMenuItems.clear()
        threads = []
        for _ in range(50):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    benchmark(run_concurrently)
    assert len(scraper.allMenuItems) == 25000

def test_audit_latency_throughput(benchmark):
    scraper = CanaData(cache_enabled=False, optimize_processing=True, max_workers=5)

    # We need to simulate processing the payload using the actual optimized processor
    def simulate_heavy_batch():
        scraper.allMenuItems.clear()
        batch = []
        for i in range(100): # Reduced size for heavy recursive process
            batch.append({'id': i, 'name': 'test', 'price': 10.0, 'nested': {'a': 1, 'b': 2, 'c': {'d': 4}}})

        # Simulate processing the batch
        with scraper._menu_data_lock:
            for item in batch:
                flattened = scraper.flatten_dictionary(item)
                scraper.allMenuItems[f"latency_{flattened.get('id', i)}"] = [flattened]

    benchmark(simulate_heavy_batch)
    assert len(scraper.allMenuItems) == 100
