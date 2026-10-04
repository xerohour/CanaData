import os
import sys
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CanaData import CanaData

def test_stress_concurrency():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def worker(worker_id):
        local_items = {}
        for i in range(150):
            local_items[f"{worker_id}_{i}"] = [{"id": worker_id * 1000 + i}]
        with scraper._menu_data_lock:
            scraper.allMenuItems.update(local_items)

    threads = []
    for i in range(25):  # 25 concurrent workers
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(scraper.allMenuItems) == 3750, f"Expected 3750, got {len(scraper.allMenuItems)}"
    print(f"Stress test passed, items processed: {len(scraper.allMenuItems)}")
