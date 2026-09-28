import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_deep_audit_high_concurrency(benchmark):
    # This tests the high concurrency and race conditions in distributed systems scaling as requested.
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            # Fast in-memory dict operations wrapped by the lock do not cause contention
            local_items = {}
            for i in range(150):
                local_items[f"{worker_id}_{i}"] = [{"id": worker_id * 1000 + i}]

            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)

        threads = []
        for i in range(25):  # 25 concurrent threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 3750
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 3750

def test_deep_audit_latency_throughput(benchmark):
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    if not os.path.exists(sample_file):
        data = {"data": {"products": [{"id": 1, "name": "test"}] * 100}}
    else:
        with open(sample_file) as f:
            data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {'test_dispensary': data.get('data', {}).get('products', []) * 50}

    def process_data():
        return processor.process_menu_data(menu_items)

    result = benchmark(process_data)
    assert len(result) > 0

def test_deep_audit_large_nesting_performance(benchmark):
    processor = OptimizedDataProcessor(max_workers=4)

    # Create a deeply nested large dictionary
    large_item = {"id": 1, "name": "test"}
    current_level = large_item
    for i in range(20):
        current_level[f"level_{i}"] = {"nested_val": i}
        current_level = current_level[f"level_{i}"]

    menu_items = {'test_dispensary': [large_item] * 500}

    def process_data():
        return processor.process_menu_data(menu_items)

    result = benchmark(process_data)
    assert len(result) > 0
