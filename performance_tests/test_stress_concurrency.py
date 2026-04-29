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


def test_stress_map_reduce():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}
    scraper.emptyMenus = {}
    scraper.extractedStrains = {}
    scraper.menuItemsFound = 0
    scraper.totalLocations = []

    results_list = []
    results_lock = threading.Lock()

    def worker(i):
        for j in range(100):
            # Simulate mapping phase: producing dictionary results independently without global state lock
            mapped_result = {
                'listing_id': f"loc-{i}-{j}",
                'local_menu_items': [{'id': i * 100 + j}],
                'is_empty_menu': False,
                'listing_copy': {'id': f"loc-{i}-{j}"},
                'local_extracted_strains': {f"strain-{i}-{j}": {"name": "test"}},
                'menu_items_count': 1
            }
            # Simulating ThreadPoolExecutor collecting the returned maps
            with results_lock:
                results_list.append(mapped_result)
            time.sleep(0.001)

    threads = []
    start_time = time.time()
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Sequential reduce step
    for res in results_list:
        scraper._merge_menu_result(res)

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == 1000
    assert scraper.menuItemsFound == 1000
    print(f"Stress test map-reduce completed successfully in {duration:.2f} seconds.")
