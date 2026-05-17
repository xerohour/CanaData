import pytest
import threading
import time
import os
import sys

# Ensure root directory is in path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CanaData import CanaData

def test_high_concurrency_stress():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    # Simulate a high number of workers (e.g. 100 threads) to expose locking bottlenecks
    num_threads = 100
    items_per_thread = 50

    def worker(thread_id):
        # We simulate the _menu_data_lock locking
        for i in range(items_per_thread):
            with scraper._menu_data_lock:
                scraper.allMenuItems[f"{thread_id}_{i}"] = [{"id": i}]
            # small sleep to mimic processing
            time.sleep(0.001)

    threads = []
    start_time = time.time()

    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == num_threads * items_per_thread
    print(f"\nCompleted {num_threads * items_per_thread} concurrent inserts across {num_threads} threads in {duration:.4f}s")

if __name__ == "__main__":
    test_high_concurrency_stress()
