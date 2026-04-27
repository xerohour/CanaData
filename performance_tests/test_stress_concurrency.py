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


def test_stress_concurrency():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def worker(i):
        state = {
            'allMenuItems': {},
            'emptyMenus': {},
            'extractedStrains': {},
            'menuItemsFound': 0,
            'totalLocations': []
        }
        for j in range(100):
            listing_id = f"listing_{i}_{j}"
            state['allMenuItems'][listing_id] = [{'id': i * 100 + j}]
            time.sleep(0.001)
        return state

    from concurrent.futures import ThreadPoolExecutor, as_completed

    start_time = time.time()
    states = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]
        for future in as_completed(futures):
            states.append(future.result())

    for state in states:
        scraper._merge_menu_result(state)

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
