import pytest
import threading
import time
from CanaData import CanaData

def test_distributed_workload_stress(benchmark):
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            local_items = {f"{worker_id}_{i}": [{'id': i}] for i in range(200)}
            with scraper._menu_data_lock:
                scraper.allMenuItems.update(local_items)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
        for t in threads: t.start()
        for t in threads: t.join()

        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 10000
