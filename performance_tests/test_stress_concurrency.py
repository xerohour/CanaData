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
        local_results = []
        for j in range(100):
            local_results.append({'id': i * 100 + j})
            time.sleep(0.001)
        return local_results

    import concurrent.futures
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            # Simulate aggregation on main thread
            scraper.allMenuItems.extend(res)

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
