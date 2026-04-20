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
    scraper.allMenuItems = []

    def worker(i):
        results = []
        for j in range(100):
            # Mock parsed result
            result = {
                'listing_id': 'mock_wmid',
                'local_menu_items': [{'id': i * 100 + j}],
                'is_empty_menu': False,
                'listing_copy': {'slug': 'mock_slug'},
                'local_extracted_strains': {},
                'menu_items_count': 1
            }
            results.append(result)
            time.sleep(0.001)
        return results

    # Mock allMenuItems initialization
    scraper.allMenuItems = {'mock_wmid': []}

    start_time = time.time()

    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]
        for future in concurrent.futures.as_completed(futures):
            results = future.result()
            for result in results:
                # Merge into existing list or create new
                if result['listing_id'] in scraper.allMenuItems:
                    scraper.allMenuItems[result['listing_id']].extend(result['local_menu_items'])
                else:
                    scraper._merge_menu_result(result)

    duration = time.time() - start_time

    assert len(scraper.allMenuItems['mock_wmid']) == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
