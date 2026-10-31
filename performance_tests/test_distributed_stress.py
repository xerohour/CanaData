import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CanaData import CanaData


def test_distributed_architecture_bottleneck(benchmark):
    # This benchmark demonstrates the current architectural limitation for horizontal scaling.
    # While it's functionally correct in vertical scaling (single machine, memory),
    # the lock forces serial writes. In a true distributed, elastic scenario with remote DBs or queues,
    # relying on a single lock on an in-memory mutable array will block asynchronous aggregation entirely.
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            local_items = {}
            for i in range(150):
                # Mock a slow scraping request/processing that happens independently before lock
                local_items[f"{worker_id}_{i}"] = [{"id": worker_id * 1000 + i, "name": f"test_{worker_id}"}]

            # The critical section where workers synchronize their writes to the global state
            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)

                # Mock a slightly more realistic I/O bound serialization operation mimicking pushing data
                # to an external system, which exposes the bottleneck clearly compared to just
                # instantaneous in-memory updates.
                time.sleep(0.005)

        threads = []
        for i in range(25):  # 25 concurrent workers trying to aggregate their results
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 3750
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 3750
