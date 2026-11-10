import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

import psutil
import pytest

from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

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

def test_audit_race_conditions():
    cana = CanaData()
    num_threads = 100
    items_per_thread = 200

    def worker_task(thread_id):
        for i in range(items_per_thread):
            item_id = f"item_{i}" # Deliberate collision
            with cana._menu_data_lock:
                existing = cana.allMenuItems.get(item_id, [])
                existing.append({"name": f"Test {i}", "thread": thread_id})
                cana.allMenuItems[item_id] = existing

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker_task, i) for i in range(num_threads)]
        for f in futures:
            f.result()

    duration = time.time() - start_time
    assert len(cana.allMenuItems) == items_per_thread

    for item_id, updates in cana.allMenuItems.items():
        assert len(updates) == num_threads

    print(f"\nRace Condition Test: Processed in {duration:.2f}s")


def test_audit_memory_leak_intensive(sample_data):
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    processor = OptimizedDataProcessor()

    for _ in range(50):
        _ = processor.process_menu_data(sample_data)

    final_memory = process.memory_info().rss
    memory_growth_mb = (final_memory - initial_memory) / (1024 * 1024)

    print(f"\nMemory Leak Test Intensive: Growth was {memory_growth_mb:.2f} MB after 50 iterations")
    assert memory_growth_mb < 100.0
