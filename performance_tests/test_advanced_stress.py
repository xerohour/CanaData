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
                menu_json = {
                    "listing": {
                        "id": f"listing_{worker_id}_{i}",
                        "slug": f"slug_{worker_id}_{i}",
                        "wmid": f"wmid_{worker_id}_{i}",
                        "_type": "dispensary"
                    },
                    "categories": [{"items": [{"id": f"item_{worker_id}_{i}"}]}]
                }
                scraper.process_menu_json(menu_json)

        threads = []
        for i in range(25): # 25 concurrent threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert sum(len(items) for items in scraper.allMenuItems.values()) == 3750
        return sum(len(items) for items in scraper.allMenuItems.values())

    result = benchmark(run_stress)
    assert result == 3750
