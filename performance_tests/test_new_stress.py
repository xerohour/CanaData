import threading
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_stress_locking():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def worker(i):
        # We want to benchmark actual real-world processing, not artificial sleeps
        mock_menu = {
            'listing': {'id': str(i), 'slug': f'test-{i}', '_type': 'dispensary'},
            'categories': [{'items': [{'id': str(i * 100 + j), 'name': f'Item {j}'} for j in range(100)]}]
        }
        scraper.process_menu_json(mock_menu)

    threads = []
    start_time = time.time()
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(scraper.allMenuItems) == 10
