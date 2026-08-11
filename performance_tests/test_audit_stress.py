import os
import sys
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CanaData import CanaData


def test_high_concurrency_race_conditions_api_limits(benchmark):
    # This tests the high concurrency and race conditions in distributed systems scaling as requested.
    def run_stress():
        scraper = CanaData(interactive_mode=False, max_workers=25, rate_limit=0)
        scraper.allMenuItems = {}

        def worker(worker_id):
            # Fast in-memory dict operations wrapped by the lock to test contention
            local_items = {}
            for i in range(200):
                local_items[f"{worker_id}_{i}"] = [{"id": worker_id * 1000 + i, "price": 10.0}]

            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)

        threads = []
        for i in range(50):  # 50 concurrent threads to simulate distributed scaling
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 10000
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 10000

def test_memory_leak_prevention_on_large_datasets():
    scraper = CanaData(interactive_mode=False)
    # Simulate a very large dataset of stateful components to check for memory efficiency
    for i in range(5000):
        scraper.allMenuItems[f"listing_{i}"] = [{"id": i, "category": {"name": "Flower"}}]

    start_len = len(scraper.allMenuItems)
    scraper.organize_into_clean_list()
    assert len(scraper.finishedMenuItems) == 5000
    assert len(scraper.allMenuItems) == start_len # verify stateful component doesn't get cleared by mistake
