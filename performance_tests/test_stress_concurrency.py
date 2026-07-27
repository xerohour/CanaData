import os
import sys
import threading
import time

# Ensure root directory is in path for imports to work during CI
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

from CanaData import CanaData


def test_stress_locking():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def worker(i):
        for j in range(100):
            with scraper._menu_data_lock:
                scraper.allMenuItems[f"{i}_{j}"] = [{'id': i * 100 + j}]

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
