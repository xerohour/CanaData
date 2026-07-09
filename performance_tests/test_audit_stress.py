import threading
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_high_concurrency_real_logic(benchmark):
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}
        scraper.emptyMenus = {}
        scraper.extractedStrains = {}
        scraper.menuItemsFound = 0
        scraper.totalLocations = []

        def worker(worker_id):
            for i in range(150):
                menu_json = {
                    'listing': {
                        'id': f'{worker_id}_{i}',
                        'slug': f'slug_{worker_id}_{i}',
                        'wmid': f'wmid_{worker_id}_{i}',
                        '_type': 'dispensary'
                    },
                    'categories': [
                        {
                            'items': [{'id': 'item1', 'name': 'weed'}]
                        }
                    ]
                }
                scraper.process_menu_json(menu_json)

        threads = []
        for i in range(25):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 3750
