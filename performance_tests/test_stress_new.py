import pytest
import threading
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_stress_high_concurrency_race_condition():
    cana = CanaData(optimize_processing=False, interactive_mode=False)
    # Testing for noisy neighbor and lock contention
    num_threads = 50
    items_per_thread = 50

    def worker(thread_id):
        listing_id = f"listing-{thread_id}"
        with cana._menu_data_lock:
            cana.allMenuItems[listing_id] = []

        for i in range(items_per_thread):
            with cana._menu_data_lock:
                cana.allMenuItems[listing_id].append({'id': f"{thread_id}-{i}"})
            # small sleep to increase overlap chance without making test too slow
            time.sleep(0.0001)

    start_time = time.time()
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time.time() - start_time
    total_items = sum(len(items) for items in cana.allMenuItems.values())
    assert total_items == num_threads * items_per_thread
    print(f"High concurrency test with {num_threads} threads completed in {duration:.3f}s")
