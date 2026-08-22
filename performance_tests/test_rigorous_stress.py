import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CanaData import CanaData


def test_rigorous_stress_concurrency(benchmark):
    """
    Rigorous stress test focusing on high-concurrency scenarios, race conditions,
    and failure modes in distributed systems as requested.
    """
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}
        error_count = [0]

        def worker(worker_id):
            local_items = {}
            # Simulate processing of items with a slight delay to trigger race conditions if lock isn't held correctly
            try:
                for i in range(250):
                    local_items[f"{worker_id}_{i}"] = [{"id": worker_id * 1000 + i, "name": f"Item {worker_id}_{i}"}]

                # Critical section testing: high contention on global lock
                with scraper._menu_data_lock:
                    # In a real distributed system, this monolithic state update would be the bottleneck.
                    # We are testing the current architecture's resilience under high contention.
                    time.sleep(0.001)  # tiny simulated network/disk overhead while holding lock to stress contention
                    scraper.allMenuItems.update(local_items)
            except Exception as e:
                # Capture failure modes
                error_count[0] += 1

        threads = []
        for i in range(50):  # 50 concurrent threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert error_count[0] == 0, f"Encountered {error_count[0]} errors during concurrent execution"
        assert len(scraper.allMenuItems) == 12500, f"Expected 12500 items, got {len(scraper.allMenuItems)}"
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 12500
