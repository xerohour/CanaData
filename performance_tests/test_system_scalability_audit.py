import json
import os
import sys
import threading
import time
import psutil
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_audit_memory_leak_container():
    """Test memory leak over repeated data processing."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    if os.path.exists(sample_file):
        with open(sample_file) as f:
            data = json.load(f)
    else:
        data = {"data": {"products": [{"id": 1, "name": "test"}] * 100}}

    processor = OptimizedDataProcessor(max_workers=2)
    menu_items = {'test_dispensary': data.get('data', {}).get('products', []) * 50}

    for _ in range(25):
        processor.process_menu_data(menu_items)

    final_memory = process.memory_info().rss
    memory_growth = final_memory - initial_memory

    # Assert memory growth is less than 50MB
    assert memory_growth < 50 * 1024 * 1024, f"Memory leak detected: {memory_growth / (1024*1024):.2f} MB"

def test_audit_latency_throughput(benchmark):
    """Benchmark data processing latency and throughput."""
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    if os.path.exists(sample_file):
        with open(sample_file) as f:
            data = json.load(f)
    else:
        data = {"data": {"products": [{"id": 1, "name": "test"}] * 100}}

    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {'test_dispensary': data.get('data', {}).get('products', []) * 50}

    def process_data():
        return processor.process_menu_data(menu_items)

    result = benchmark(process_data)
    assert len(result) > 0

def test_audit_high_concurrency_race_conditions(benchmark):
    """Stress test focusing on high-concurrency scenarios and race conditions."""
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            local_items = {}
            for i in range(500):
                local_items[f"{worker_id}_{i}"] = [{'id': worker_id * 1000 + i, 'name': 'stress_test'}]

            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)

        threads = []
        for i in range(50):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 25000
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 25000
