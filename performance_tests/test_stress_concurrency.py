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
            listing_id = f"loc-{i}-{j}"
            results.append({
                'listing_id': listing_id,
                'local_menu_items': [{'id': i * 100 + j}],
                'is_empty_menu': False,
                'listing_copy': {'id': listing_id},
                'local_extracted_strains': {},
                'menu_items_count': 1,
                'listing_slug': f'slug-{j}'
            })
            time.sleep(0.001)
        return results

    threads = []
    thread_results = []

    def thread_runner(i):
        thread_results.append(worker(i))

    start_time = time.time()
    for i in range(10):
        t = threading.Thread(target=thread_runner, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    for results in thread_results:
        for result in results:
            scraper._merge_menu_result(result)

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
