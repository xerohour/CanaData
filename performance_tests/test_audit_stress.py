import pytest
import threading
import time
import sys
import os
import queue

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_high_concurrency_state_write(benchmark):
    scraper = CanaData(optimize_processing=False, interactive_mode=False)

    # 25 Threads, 500 operations each
    NUM_THREADS = 25
    OPS_PER_THREAD = 500

    def worker():
        for i in range(OPS_PER_THREAD):
            # Simulate O(1) dictionary assignment inside the lock
            with scraper._menu_data_lock:
                shop_id = f"shop_{threading.get_ident()}"
                if shop_id not in scraper.allMenuItems:
                    scraper.allMenuItems[shop_id] = []
                scraper.allMenuItems[shop_id].append({"id": i, "name": "test"})

    def run_stress():
        scraper.allMenuItems.clear()
        threads = []
        for _ in range(NUM_THREADS):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return scraper.allMenuItems

    result = benchmark(run_stress)
    total_items = sum(len(items) for items in result.values())
    assert total_items == NUM_THREADS * OPS_PER_THREAD
