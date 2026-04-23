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

    def worker(i):
        results = []
        for j in range(100):
            # simulate process map
            results.append({
                'listing_id': f'loc-{i}-{j}',
                'local_menu_items': [{'id': i * 100 + j}],
                'is_empty_menu': False,
                'listing_copy': {'id': f'loc-{i}-{j}', 'num_menu_items': '1'},
                'local_extracted_strains': {},
                'menu_items_count': 1
            })
            time.sleep(0.001)
        return results

    start_time = time.time()
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]
        for future in concurrent.futures.as_completed(futures):
            results = future.result()
            # simulate process reduce/merge
            for res in results:
                scraper._merge_menu_result(res)

    duration = time.time() - start_time

    assert sum(len(items) for items in scraper.allMenuItems.values()) == 1000
    print(f"Concurrency stress test completed successfully in {duration:.2f} seconds.")
