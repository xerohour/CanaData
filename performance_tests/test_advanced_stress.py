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
            for i in range(150):
                mock_json = {
                    'listing': {
                        'id': f'worker_{worker_id}_item_{i}',
                        'slug': f'slug_{worker_id}_{i}',
                        '_type': 'dispensary',
                        'wmid': 123
                    },
                    'categories': [
                        {
                            'items': [{'id': f'item_{worker_id}_{i}'}]
                        }
                    ]
                }
                scraper.process_menu_json(mock_json)

        threads = []
        for i in range(25): # 25 concurrent threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(scraper.allMenuItems) == 3750
        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 3750
