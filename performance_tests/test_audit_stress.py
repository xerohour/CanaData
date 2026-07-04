import threading
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from concurrent_processor import ConcurrentMenuProcessor

def test_high_concurrency_race_condition():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def concurrent_writer(worker_id):
        for i in range(200):
            # Explicitly force race condition on the dictionary to test the lock
            with scraper._menu_data_lock:
                if 'listing' not in scraper.allMenuItems:
                    scraper.allMenuItems['listing'] = []
                # Slight sleep to exaggerate contention
                time.sleep(0.0001)
                scraper.allMenuItems['listing'].append({'id': worker_id * 1000 + i})

    threads = []
    for i in range(30):
        t = threading.Thread(target=concurrent_writer, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(scraper.allMenuItems['listing']) == 6000

def test_concurrent_processor_rate_limit():
    processor = ConcurrentMenuProcessor(max_workers=5, rate_limit=0.05)
    locations = [{'slug': f'loc_{i}'} for i in range(20)]

    def process_func(loc):
        return {"processed": True}

    start_time = time.time()
    results = processor.process_locations(locations, process_func)
    end_time = time.time()

    assert len(results) == 20
    # Minimum time should be approx (20 locations / 5 workers) * 0.05 limit = 0.2s minimum
    assert (end_time - start_time) > 0.1
