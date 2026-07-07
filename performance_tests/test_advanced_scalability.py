import threading
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_horizontal_scalability_benchmark(benchmark):
    def run_scalable_load():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            for i in range(100):
                menu_json = {
                    'data': {
                        'menu_items': [{'id': worker_id * 1000 + i, 'price': 20.0}]
                    }
                }
                location = {'slug': f'loc_{worker_id}_{i}', 'type': 'dispensary', 'id': f'loc_id_{worker_id}_{i}'}
                scraper.process_menu_items_json(menu_json, location)

        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return len(scraper.allMenuItems)

    result = benchmark(run_scalable_load)
    assert result == 1000
