import threading
import time
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
                # Simulate some minor processing time
                time.sleep(0.0001)
                scraper._menu_data_queue.put({
                    'listing_id': f"{worker_id}_{i}",
                    'local_menu_items': [{'id': worker_id * 1000 + i}],
                    'is_empty_menu': False,
                    'listing_copy': {},
                    'local_extracted_strains': {},
                    'menu_items_count': 1
                })

        threads = []
        for i in range(25): # 25 concurrent threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        scraper._drain_menu_data_queue()

        assert len(scraper.allMenuItems) == 3750
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 3750
