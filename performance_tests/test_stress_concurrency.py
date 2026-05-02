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
    """
    Stress test verifying the new lock-free map-reduce model allows
    workers to generate data and the main thread to merge it safely.
    """
    scraper = CanaData(interactive_mode=False)

    import queue
    results_queue = queue.Queue()

    def worker(i):
        for j in range(100):
            # Simulate worker processing and returning a map dictionary
            result = {
                'listing_id': f'listing_{i}_{j}',
                'local_menu_items': [{'id': i * 100 + j}],
                'is_empty_menu': False,
                'listing_copy': {'id': f'listing_{i}_{j}'},
                'local_extracted_strains': {},
                'menu_items_count': 1
            }
            results_queue.put(result)
            time.sleep(0.001)

    threads = []
    start_time = time.time()

    # Start workers
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    # Join threads
    for t in threads:
        t.join()

    # Main thread sequentially merges results (lock-free)
    while not results_queue.empty():
        result = results_queue.get()
        scraper._merge_menu_result(result)

    duration = time.time() - start_time

    # Each of 10 workers produced 100 results, total 1000 listings processed
    assert len(scraper.allMenuItems) == 1000
    assert scraper.menuItemsFound == 1000
    print(f"Map-reduce stress test completed successfully in {duration:.2f} seconds.")
