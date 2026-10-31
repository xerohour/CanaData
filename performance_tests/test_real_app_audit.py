import os
import sys
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cache_manager import CacheManager
from optimized_data_processor import OptimizedDataProcessor


def test_cache_manager_concurrency(benchmark):
    cache = CacheManager(memory_cache_size=5000, enable_disk_cache=False)
    def workload():
        def worker(w_id):
            for i in range(200):
                cache.set(f"url_{w_id}_{i}", {"data": "test"})
                cache.get(f"url_{w_id}_{i}")
        threads = []
        for i in range(20):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return cache.get_stats()
    stats = benchmark(workload)
    assert isinstance(stats, dict)

def test_optimized_processor_flattening(benchmark):
    processor = OptimizedDataProcessor(max_workers=4)
    items = []
    for i in range(500):
        items.append({
            "id": i,
            "name": f"Product {i}",
            "price": {"amount": 25.0, "currency": "USD"},
            "strain": {"name": "OG Kush", "type": "indica"},
            "categories": [{"id": 1, "name": "Flower"}, {"id": 2, "name": "Premium"}]
        })
    menu_data = {"test_loc_1": items, "test_loc_2": items}

    def workload():
        return processor.process_menu_data(menu_data)

    result = benchmark(workload)
    assert len(result) == 1000
