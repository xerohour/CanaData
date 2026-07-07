import threading
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_process_menu_items_json_concurrent_failure():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def worker(worker_id):
        for i in range(20):
            menu_json = {
                'data': {
                    'menu_items': [{'id': worker_id * 1000 + i, 'name': 'Item'}]
                }
            }
            location = {'slug': f'loc_{worker_id}_{i}', 'type': 'dispensary', 'id': f'loc_id_{worker_id}_{i}'}

            try:
                if i % 5 == 0:
                    raise ValueError("Simulated data format error")
                scraper.process_menu_items_json(menu_json, location)
            except Exception:
                pass

    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(scraper.allMenuItems) == 80
