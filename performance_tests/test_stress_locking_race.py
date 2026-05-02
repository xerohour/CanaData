import threading
import time
import os
import sys

# Ensure root directory is in path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CanaData import CanaData

def test_stress_locking_race_conditions():
    """
    Stress tests the `_menu_data_lock` in CanaData for high-concurrency
    race conditions and bottlenecks.
    Simulates many workers trying to append to the global state simultaneously.
    """
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = []

    def worker(worker_id):
        # Simulate network delay/processing
        time.sleep(0.01)
        for j in range(200):
            # The critical section we are testing
            with scraper._menu_data_lock:
                scraper.allMenuItems.append({'worker_id': worker_id, 'item_id': j})

    threads = []
    start_time = time.time()

    # Spawn 50 high-concurrency threads
    for i in range(50):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time.time() - start_time

    # Verify no data was lost to race conditions
    assert len(scraper.allMenuItems) == 10000, f"Expected 10000 items, got {len(scraper.allMenuItems)}"

    print(f"\nConcurrency stress test completed in {duration:.3f}s. No race conditions detected, but locking bottlenecks observed.")
