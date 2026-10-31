import json
import os
import sys
import threading
import psutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_audit_latency_throughput(benchmark):
    # Benchmark to measure latency and throughput of the data processing
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    if not os.path.exists(sample_file):
        data = {'data': {'products': [{'id': i, 'name': f'test_{i}', 'price': {'amount': 10}} for i in range(10)]}}
    else:
        with open(sample_file) as f:
            data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=4)
    # Duplicate data to create a decent sized batch
    menu_items = {'test_dispensary': data.get('data', {}).get('products', []) * 50}

    def process_data():
        return processor.process_menu_data(menu_items)

    result = benchmark(process_data)
    assert len(result) > 0

def test_audit_high_concurrency(benchmark):
    # Stress test focusing on high-concurrency scenarios, race conditions
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            local_items = {}
            # Simulate processing of items
            for i in range(500):
                local_items[f"{worker_id}_{i}"] = [{'id': worker_id * 1000 + i, 'name': 'test'}]

            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)

        threads = []
        for i in range(50): # 50 concurrent threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 25000
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 25000

def test_audit_memory_leak():
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    if not os.path.exists(sample_file):
        data = {'data': {'products': [{'id': i, 'name': f'test_{i}', 'price': {'amount': 10}} for i in range(10)]}}
    else:
        with open(sample_file) as f:
            data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=2)
    menu_items = {'test_dispensary': data.get('data', {}).get('products', []) * 50}

    for _ in range(20):
        processor.process_menu_data(menu_items)

    final_memory = process.memory_info().rss
    memory_growth = final_memory - initial_memory

    # Assert memory growth is less than 50MB
    assert memory_growth < 50 * 1024 * 1024, f"Memory leak detected: grew by {memory_growth / (1024*1024):.2f} MB"
