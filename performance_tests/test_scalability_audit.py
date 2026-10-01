import json
import os
import sys
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_scalability_horizontal_scaling(benchmark):
    # Benchmark to measure horizontal scaling using ThreadPoolExecutor
    # Simulate processing chunks of data as multiple "nodes" or "processes"

    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    if os.path.exists(sample_file):
        with open(sample_file) as f:
            data = json.load(f)
        base_products = data.get('data', {}).get('products', [])
    else:
        # Generate mock data if file not found
        base_products = [{'id': i, 'name': f'mock_product_{i}', 'brand': {'id': 1, 'name': 'mock_brand'}} for i in range(100)]

    # Create large dataset
    menu_items = {'test_dispensary': base_products * 20}

    def process_workload():
        processor = OptimizedDataProcessor(max_workers=8)
        return processor.process_menu_data(menu_items)

    result = benchmark(process_workload)
    assert len(result) > 0

def test_stress_concurrent_mutations(benchmark):
    # Benchmark testing concurrent mutations on shared state (CanaData allMenuItems)

    def run_concurrent_mutations():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems.clear() # Clear state before each benchmark run

        def worker(worker_id):
            local_items = {}
            for i in range(100):
                # Use unique IDs to avoid collision during stress test
                unique_key = f"{worker_id}_{uuid.uuid4()}_{i}"
                local_items[unique_key] = [{'id': i, 'name': f'test_{i}'}]

            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)

        threads = []
        for i in range(20):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 2000
        return len(scraper.allMenuItems)

    result = benchmark(run_concurrent_mutations)
    assert result == 2000
