import threading
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_high_concurrency_global_lock_contention(benchmark):
    # This tests the high concurrency and race conditions in distributed systems scaling as requested.
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            for i in range(150):
                menu_json = {'data': {'menu_items': [{'id': worker_id * 1000 + i}]}}
                location = {'id': f'loc_{worker_id}_{i}', 'slug': f'test-loc-{worker_id}-{i}'}
                scraper.process_menu_items_json(menu_json, location)

        threads = []
        for i in range(25): # 25 concurrent threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        total_items = sum(len(items) for items in scraper.allMenuItems.values())
        assert total_items == 3750
        return total_items

    result = benchmark(run_stress)
    assert result == 3750
