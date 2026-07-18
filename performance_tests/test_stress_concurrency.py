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
        # We want to benchmark actual real-world processing, not artificial sleeps
        mock_menu = {
            'listing': {'id': str(i), 'slug': f'test-{i}', '_type': 'dispensary'},
            'categories': [{'items': [{'id': str(i * 100 + j), 'name': f'Item {j}'} for j in range(100)]}]
        }
        scraper.process_menu_json(mock_menu)

    threads = []
    start_time = time.time()
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == 10
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
