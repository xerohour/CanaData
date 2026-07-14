import threading
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_genuine_processing_stress(benchmark):
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}
        scraper.emptyMenus = {}
        scraper.extractedStrains = {}
        scraper.menuItemsFound = 0
        scraper.totalLocations = []

        def worker(worker_id):
            for i in range(50):
                menu_json = {
                    "data": {
                        "menu_items": [
                            {"id": f"item_{worker_id}_{i}_{j}", "name": "Test Item", "brand": {"name": "Brand A"}}
                            for j in range(10)
                        ]
                    }
                }
                location = {
                    "id": f"loc_{worker_id}_{i}",
                    "slug": f"loc-slug-{worker_id}-{i}",
                    "name": "Test Dispensary",
                    "state": "CA",
                    "city": "Los Angeles",
                    "type": "dispensary"
                }
                scraper.process_menu_items_json(menu_json, location)

        threads = []
        for i in range(10): # 10 concurrent threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return scraper.menuItemsFound

    result = benchmark(run_stress)
    assert result == 5000
