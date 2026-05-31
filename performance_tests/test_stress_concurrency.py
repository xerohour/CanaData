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

    def worker(i):
        for j in range(100):
            scraper.menu_update_queue.put({
                'listing_id': f'listing_{i * 100 + j}',
                'local_menu_items': [{'id': i * 100 + j}],
                'is_empty_menu': False,
                'listing_copy': {},
                'local_extracted_strains': {},
                'menu_items_count': 1
            })
            time.sleep(0.001)

    threads = []
    start_time = time.time()
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    scraper.flush_queue()
    duration = time.time() - start_time

    total_items = sum(len(items) for items in scraper.allMenuItems.values())
    assert total_items == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
