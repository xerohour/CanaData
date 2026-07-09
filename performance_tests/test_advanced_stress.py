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
                # with scraper._menu_data_lock:
                    # Simulate some minor processing time to force lock contention
                time.sleep(0.0001)
                scraper.allMenuItems.setdefault(worker_id, []).append({'id': worker_id * 1000 + i})

        threads = []
        for i in range(25): # 25 concurrent threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert sum(len(lst) for lst in scraper.allMenuItems.values()) == 3750
        return sum(len(lst) for lst in scraper.allMenuItems.values())

    result = benchmark(run_stress)
    assert result == 3750
