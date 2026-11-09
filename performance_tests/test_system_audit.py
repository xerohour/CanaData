import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
import psutil
import pytest

from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor
from cache_manager import CacheManager

def load_sample_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'sample_products.json')
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return {"loc_1": data['data']['products']}
    except FileNotFoundError:
        return {"loc_1": [{"id": i, "name": f"Product {i}", "price": i*10} for i in range(100)]}

@pytest.fixture(scope="module")
def sample_data():
    return load_sample_data()

def test_system_audit_high_concurrency():
    cana = CanaData()
    num_threads = 100
    items_per_thread = 200

    def worker_task(thread_id):
        for i in range(items_per_thread):
            item_id = f"item_{thread_id}_{i}"
            with cana._menu_data_lock:
                cana.allMenuItems[item_id] = [{"name": f"Test {i}", "thread": thread_id}]

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker_task, i) for i in range(num_threads)]
        for f in futures:
            f.result()

    duration = time.time() - start_time
    total_items = num_threads * items_per_thread

    assert len(cana.allMenuItems) == total_items
    print(f"\nSystem Concurrency Test: Processed {total_items} items across {num_threads} threads in {duration:.2f}s")

def test_system_audit_memory_leak_processor(sample_data):
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    processor = OptimizedDataProcessor()

    # Simulate heavy workload
    for _ in range(30):
        _ = processor.process_menu_data(sample_data)

    final_memory = process.memory_info().rss
    memory_growth_mb = (final_memory - initial_memory) / (1024 * 1024)

    print(f"\nSystem Memory Test: Growth was {memory_growth_mb:.2f} MB after 30 iterations")
    # Asserting memory leak is under control (threshold 50MB)
    assert memory_growth_mb < 50.0

def test_benchmark_data_processing_latency(benchmark, sample_data):
    processor = OptimizedDataProcessor()

    def run_process():
        return processor.process_menu_data(sample_data)

    result = benchmark(run_process)
    assert result is not None

def test_benchmark_cache_manager_throughput(benchmark):
    cache = CacheManager(enable_disk_cache=False)

    def run_cache_operations():
        cache.set("test_url", {"data": "test"})
        return cache.get("test_url")

    result = benchmark(run_cache_operations)
    assert result is not None
