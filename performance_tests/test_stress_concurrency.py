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

    def worker(i):
        # Workers no longer lock; they just return data
        results = []
        for j in range(100):
            item = {'id': i * 100 + j}
            results.append({
                'listing_id': str(i * 100 + j),
                'menu_items': [item],
                'empty_menu': None,
                'extracted_strains': {},
                'menu_items_count': 1,
                'listing_copy': {'id': i * 100 + j}
            })
            time.sleep(0.001)
        return results

    # Main thread aggregates
    from concurrent.futures import ThreadPoolExecutor
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]
        for future in futures:
            for result in future.result():
                scraper._aggregate_menu_result(result)

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == 1000
    assert scraper.menuItemsFound == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
