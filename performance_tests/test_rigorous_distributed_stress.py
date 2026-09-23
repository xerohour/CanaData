import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_rigorous_distributed_stress(benchmark):
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            local_items = {}
            for i in range(1000):
                # Simulating heavy distributed batch update
                local_items[f"{worker_id}_{i}"] = [{'id': worker_id * 10000 + i, 'name': f'test_dist_{worker_id}_{i}'}]

            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)

        threads = []
        for i in range(100): # 100 concurrent workers
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 100000
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 100000
