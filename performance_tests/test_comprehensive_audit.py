import os
import sys
import threading
import time
import json
import psutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_audit_high_concurrency(benchmark):
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            local_items = {}
            for i in range(500):
                local_items[f"{worker_id}_{i}"] = [{"id": worker_id * 1000 + i, "data": "dummy"}]

            # Simulate fast in-memory dict operations inside the lock
            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)

        threads = []
        for i in range(50):  # 50 concurrent threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 25000
        return len(scraper.allMenuItems)

    result = benchmark.pedantic(run_stress, rounds=5, iterations=1)
    assert result == 25000


def test_audit_memory_leak():
    process = psutil.Process(os.getpid())

    processor = OptimizedDataProcessor(max_workers=2)

    # Create large dummy nested data
    large_batch = {}
    for i in range(500):
        large_batch[f"loc_{i}"] = [
            {
                "id": i,
                "name": f"Product {i}",
                "brand": {"id": 1, "name": "Brand A"},
                "prices": {"ounce": [{"price": 100, "label": "ounce"}]},
                "metrics": {"aggregates": {"thc": 20, "cbd": 0}},
                "category": {"name": "Flower"},
                "locations_found_at": [f"/dispensary/loc_{i}"]
            }
        ]

    mem_before = process.memory_info().rss

    # Run processor multiple times to check for leak
    for _ in range(20):
        processor.process_menu_data(large_batch)

    mem_after = process.memory_info().rss
    diff_mb = (mem_after - mem_before) / (1024 * 1024)

    # Assert memory didn't grow unbounded (>50MB is arbitrarily large for this test)
    assert diff_mb < 50.0


def test_audit_latency_throughput(benchmark):
    processor = OptimizedDataProcessor(max_workers=2)

    # Create realistic batch
    batch = {}
    for i in range(100):
        batch[f"loc_{i}"] = [
            {
                "id": i,
                "name": f"Product {i}",
                "brand": {"id": 1, "name": "Brand A"},
                "prices": {"ounce": [{"price": 100, "label": "ounce"}], "gram": [{"price": 10, "label": "gram"}]},
                "metrics": {"aggregates": {"thc": 20, "cbd": 1}},
                "category": {"name": "Flower"},
                "locations_found_at": [f"/dispensary/loc_{i}"]
            }
        ]

    def run_process():
        return processor.process_menu_data(batch)

    result = benchmark.pedantic(run_process, rounds=50, iterations=1)
    assert len(result) == 100
