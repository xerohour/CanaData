import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_throughput_batch_size(benchmark):
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems['test_listing'] = []

    # Simulate a small payload of menu items to append
    items = [{'id': i, 'name': f'item_{i}'} for i in range(500)]

    def worker_action():
        with scraper._menu_data_lock:
            scraper.allMenuItems['test_listing'].extend(items)

    result = benchmark(worker_action)
    assert len(scraper.allMenuItems['test_listing']) > 0
