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
        for j in range(100):
            with scraper._menu_data_lock:
                scraper.allMenuItems.append({'id': i * 100 + j})
            time.sleep(0.001)

    threads = []
    start_time = time.time()
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")


def test_stress_map_reduce_concurrency():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def worker_map(i):
        # Map phase: Return isolated dict instead of locking
        isolated_dict = {}
        for j in range(100):
            isolated_dict[f"{i*100+j}"] = {'id': i * 100 + j}
        time.sleep(0.001)
        return isolated_dict

    def _merge_menu_result(result):
        # Reduce phase: Merge into global state sequentially
        scraper.allMenuItems.update(result)

    start_time = time.time()

    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker_map, i) for i in range(10)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            _merge_menu_result(result)

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == 1000
    print(f"Map-Reduce Stress test completed successfully in {duration:.2f} seconds.")
