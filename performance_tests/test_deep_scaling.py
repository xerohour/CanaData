import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CanaData import CanaData


def test_deep_scaling_stress(benchmark):
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            local_items = {}
            for i in range(1000):
                # Real dictionary updates without artificial sleep
                local_items[f"{worker_id}_{i}"] = [{"id": worker_id * 1000 + i, "name": "stress_test"}]

            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)

        threads = []
        for i in range(100):  # 100 threads for heavy load
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 100000
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 100000


def test_failure_mode_distributed(benchmark):
    def run_failure():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        # Simulating external failure
        scraper.errors = []

        def failing_worker(worker_id):
            try:
                if worker_id % 2 == 0:
                    raise Exception(f"Simulated network failure on worker {worker_id}")
                else:
                    local_items = {}
                    for i in range(100):
                        local_items[f"{worker_id}_{i}"] = [{"id": worker_id * 1000 + i, "name": "success_test"}]
                    with scraper._menu_data_lock:
                        scraper.allMenuItems.update(local_items)
            except Exception as e:
                # Need a lock for errors array in distributed systems, simulating it here
                with scraper._menu_data_lock: # Using same lock for simplicity in this mock
                    scraper.errors.append({"worker": worker_id, "error": str(e)})

        threads = []
        for i in range(50):
            t = threading.Thread(target=failing_worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 25 * 100
        assert len(scraper.errors) == 25
        return len(scraper.allMenuItems)

    result = benchmark(run_failure)
    assert result == 2500
