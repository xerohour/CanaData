import threading
import time
import os
import sys

# Ensure root directory is in path for imports to work during CI
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

from CanaData import CanaData  # noqa: E402


def test_stress_locking():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}
    scraper.emptyMenus = {}
    scraper.extractedStrains = {}
    scraper.menuItemsFound = 0
    scraper.totalLocations = []

    from concurrent.futures import ThreadPoolExecutor

    def worker(i):
        results = []
        for j in range(100):
            listing_id = f"{i}_{j}"
            results.append({
                'listing_id': listing_id,
                'local_menu_items': [{'id': i * 100 + j}],
                'is_empty_menu': False,
                'listing_copy': {'id': listing_id},
                'local_extracted_strains': {},
                'menu_items_count': 1
            })
            time.sleep(0.001)
        return results

    start_time = time.time()
    all_results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]
        for future in futures:
            all_results.extend(future.result())

    for res in all_results:
        scraper._aggregate_menu_result(res)

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == 1000
    assert scraper.menuItemsFound == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
