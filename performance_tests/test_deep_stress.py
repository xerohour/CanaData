import json
import os
import sys
import threading
import uuid
from memory_profiler import profile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor


def test_concurrency_race_condition(benchmark):
    """
    Stress test focusing on high-concurrency scenarios and race conditions
    in the distributed processing architecture.
    """
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems.clear() # Clear shared state

        def worker(worker_id):
            local_items = {}
            for i in range(250):
                # Use uuid for keys to prevent collision
                local_items[f"{worker_id}_{str(uuid.uuid4())}"] = [
                    {'id': str(uuid.uuid4()), 'name': 'stress_test', 'prices': {'ounce': [200.0]}}
                ]

            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)

        threads = []
        for i in range(100): # High concurrency: 100 threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 25000
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 25000

def test_memory_leak_deep():
    """
    Test memory consumption during repeated intensive tasks to catch leaks.
    """
    import psutil
    process = psutil.Process(os.getpid())

    # Force garbage collection to get a clean baseline
    import gc
    gc.collect()
    initial_memory = process.memory_info().rss

    sample_file = os.path.join(os.path.dirname(__file__), "..", "sample_products.json")
    with open(sample_file) as f:
        data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=2)
    # create heavy payload
    items = data.get("data", {}).get("products", []) * 10

    for i in range(25): # Deep iteration test
        menu_items = {str(uuid.uuid4()): items.copy()}
        processor.process_menu_data(menu_items)

    gc.collect()
    final_memory = process.memory_info().rss
    memory_growth = final_memory - initial_memory

    # threshold of 60MB growth for 25 large iterations
    assert memory_growth < 60 * 1024 * 1024, f"Memory leak detected: grew by {memory_growth / (1024*1024):.2f} MB"
