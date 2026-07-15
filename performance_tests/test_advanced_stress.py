import threading
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_high_concurrency_global_lock_contention(benchmark):
    def run_stress():
        scraper = CanaData(interactive_mode=False)
        scraper.allMenuItems = {}

        def worker(worker_id):
            for i in range(150):
                listing_id = f"{worker_id}_{i}"
                listing_copy = {'id': listing_id}
                local_menu_items = [{'id': i}]
                local_extracted_strains = {f"strain_{i}": {'name': 'strain'}}
                menu_items_count = 1

                with scraper._menu_data_lock:
                    scraper.allMenuItems[listing_id] = local_menu_items
                    if menu_items_count == 0:
                        scraper.emptyMenus[listing_id] = listing_copy

                    for slug, strain in local_extracted_strains.items():
                        if slug not in scraper.extractedStrains:
                            scraper.extractedStrains[slug] = strain

                    scraper.menuItemsFound += menu_items_count
                    scraper.totalLocations.append(listing_copy)

        threads = []
        for i in range(25): # 25 concurrent threads
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return len(scraper.allMenuItems)

    result = benchmark(run_stress)
    assert result == 3750
