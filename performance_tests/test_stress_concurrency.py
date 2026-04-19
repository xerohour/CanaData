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
        # Simulate processing that returns a parsed dictionary instead of locking
        results = []
        for j in range(100):
            time.sleep(0.001)
            results.append({'id': i * 100 + j})
        return {
            'listing_id': f'worker_{i}',
            'local_menu_items': results,
            'listing_copy': {'id': f'worker_{i}'},
            'menu_items_count': 100
        }

    start_time = time.time()

    # Process concurrently
    accumulated_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]
        for future in concurrent.futures.as_completed(futures):
            accumulated_results.append(future.result())

    # Merge sequentially
    for result in accumulated_results:
        scraper._merge_menu_result(result)

    duration = time.time() - start_time

    total_items = sum(len(items) for items in scraper.allMenuItems.values())
    assert total_items == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
