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

def test_map_reduce_concurrency():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def worker(i):
        result = {'listing_id': f'listing-{i}', 'local_menu_items': []}
        for j in range(100):
            result['local_menu_items'].append({'id': i * 100 + j})
            time.sleep(0.001)
        return result

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            scraper._merge_menu_result(result)

    duration = time.time() - start_time

    assert len(scraper.allMenuItems.keys()) == 10

    total_items = 0
    for listing_id in scraper.allMenuItems:
        total_items += len(scraper.allMenuItems[listing_id])

    assert total_items == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
