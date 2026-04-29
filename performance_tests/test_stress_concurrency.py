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


import concurrent.futures

def test_stress_locking():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def worker(i):
        # Simulate processing logic returning a dictionary
        time.sleep(0.001)
        return {
            'listing_id': str(i),
            'menu_items': [{'id': i * 100 + j} for j in range(100)],
            'is_empty_menu': False,
            'listing_copy': {},
            'extracted_strains': {},
            'menu_items_count': 100
        }

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]
        for future in concurrent.futures.as_completed(futures):
            scraper._merge_menu_result(future.result())

    duration = time.time() - start_time

    total_items = sum(len(items) for items in scraper.allMenuItems.values())
    assert total_items == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
