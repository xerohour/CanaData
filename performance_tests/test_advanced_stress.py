import threading
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_high_concurrency_global_lock_contention(benchmark):
    # This tests the high concurrency and race conditions in distributed systems scaling as requested.
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            # We want to benchmark actual real-world processing, not artificial sleeps
            mock_menu = {
                'listing': {'id': str(worker_id), 'slug': f'test-{worker_id}', '_type': 'dispensary'},
                'categories': [{'items': [{'id': str(worker_id * 1000 + i), 'name': f'Item {i}'} for i in range(150)]}]
            }
            scraper.process_menu_json(mock_menu)

        threads = []
        for i in range(25): # 25 concurrent threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 25
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 25
