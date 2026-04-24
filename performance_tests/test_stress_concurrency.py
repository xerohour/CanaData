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

    def worker(i):
        results = []
        for j in range(100):
            result_id = i * 100 + j
            # Simulate worker producing isolated data
            results.append({
                'listing_id': result_id,
                'local_menu_items': [{'id': result_id}],
                'is_empty_menu': False,
                'listing_copy': {'id': result_id},
                'local_extracted_strains': {},
                'menu_items_count': 1,
                'listing_slug': f'slug-{result_id}',
                'discovery': False
            })
            time.sleep(0.001)
        return results

    import concurrent.futures
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]

        # Sequentially merge lock-free map-reduce results
        for future in concurrent.futures.as_completed(futures):
            worker_results = future.result()
            for result in worker_results:
                scraper._merge_menu_result(result)

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
