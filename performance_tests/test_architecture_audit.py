import json
import os
import sys
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_audit_scale_concurrency(benchmark):
    """
    Stress test designed for Scalability Analytics and High-Concurrency Edge Cases.
    Focuses on failure modes, stateful array contention, and lock mechanisms in distributed workflows.
    """
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}
        scraper.totalLocations = []
        scraper.emptyMenus = {}

        def heavy_worker(worker_id):
            local_items = {}
            for i in range(150):
                item_dict = {
                    'id': f"item_{worker_id}_{i}",
                    'name': 'Stress Item',
                    'price': {'amount': 15.99, 'currency': 'USD'},
                    'brand': {'name': 'Audit Brand', 'id': 999}
                }
                local_items[f"{worker_id}_{i}"] = [item_dict]

            # Critical section simulation representing noisy neighbor lock contention
            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)
                scraper.totalLocations.append({"id": worker_id})

        threads = []
        for i in range(100):  # 100 concurrent threads
            t = threading.Thread(target=heavy_worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 15000
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 15000
