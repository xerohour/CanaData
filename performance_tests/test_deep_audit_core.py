import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_deep_audit_concurrency(benchmark):
    # Deep stress test targeting potential N+1 or scaling limitations in concurrent extraction
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            local_items = {}
            for i in range(100):
                # Unique IDs to avoid collision during global state injection
                local_items[f"{worker_id}_{i}"] = [{'id': worker_id * 1000 + i, 'name': 'test', 'price': {'amount': 50}}]

            # Mimic the exact lock contention pattern
            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)

        threads = []
        for i in range(100): # High concurrency (100 threads)
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 10000
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 10000

def test_deep_audit_memory_leak():
    import psutil
    process = psutil.Process(os.getpid())

    # Initialize processor
    processor = OptimizedDataProcessor(max_workers=2)

    # Generate mock heavy workload
    mock_data = [{'id': i, 'category': {'name': 'test'}, 'price': {'amount': 100}} for i in range(500)]
    menu_items = {f'dispensary_{j}': mock_data for j in range(20)}

    # Force GC before taking baseline
    import gc
    gc.collect()
    initial_memory = process.memory_info().rss

    # Process repeatedly to simulate sustained workload
    for _ in range(50): # 50 iterations of heavy data
        processor.process_menu_data(menu_items)

    gc.collect()
    final_memory = process.memory_info().rss
    memory_growth = final_memory - initial_memory

    # Assert memory growth is stable (less than 100MB growth)
    assert memory_growth < 100 * 1024 * 1024, f"Memory leak detected: grew by {memory_growth / (1024*1024):.2f} MB"

def test_deep_audit_flattening_latency(benchmark):
    # Measure strict CPU latency for the core algorithm bypassing the scraper network tier
    processor = OptimizedDataProcessor(max_workers=4)

    # Generate large, complex nested dictionary to stress the normalization routine
    mock_data = []
    for i in range(1000):
        mock_data.append({
            'id': i,
            'name': f'Product {i}',
            'brand': {'id': i*10, 'name': 'Test Brand'},
            'price': {'amount': 50.0, 'currency': 'USD', 'tiers': [{'weight': '1g', 'price': 10}, {'weight': '3.5g', 'price': 30}]},
            'images': [{'url': 'http://test.com/img1.jpg'}, {'url': 'http://test.com/img2.jpg'}],
            'tags': ['indica', 'thc', 'sale'],
            'metadata': {'testing': {'thc': 25.5, 'cbd': 0.1}, 'vendor': {'name': 'Vendor A'}}
        })

    menu_items = {'super_dispensary_1': mock_data, 'super_dispensary_2': mock_data}

    def process_data():
        return processor.process_menu_data(menu_items)

    result = benchmark(process_data)
    # Ensure all data was processed
    assert len(result) == 2000
