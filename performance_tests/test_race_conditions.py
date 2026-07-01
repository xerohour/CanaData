import pytest
import os
import sys
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_high_concurrency_race_conditions(benchmark):
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = []

        def worker(worker_id):
            for i in range(200):
                with scraper._menu_data_lock:
                    scraper.allMenuItems.append({'id': worker_id * 1000 + i})

        threads = []
        for i in range(20):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 4000
