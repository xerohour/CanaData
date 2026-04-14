import cProfile
import pstats
import io
import time
import sys
import os
import requests_mock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from concurrent_processor import ConcurrentMenuProcessor

def run_concurrent_fetch_benchmark():
    processor = ConcurrentMenuProcessor(max_workers=50, rate_limit=0.0) # Removing rate limit to test max throughput

    locations = [{"slug": f"location_{i}"} for i in range(100)]

    with requests_mock.Mocker() as m:
        for loc in locations:
            m.get(f"https://api-g.weedmaps.com/discovery/v1/listings/{loc['slug']}/menu_items?page_size=100", json={"data": {"menu_items": [{"id": 1, "name": "Test"}]}})

        def mock_process_func(location):
            import requests
            # Simulate a network call
            requests.get(f"https://api-g.weedmaps.com/discovery/v1/listings/{location['slug']}/menu_items?page_size=100")
            return {"status": "success"}

        start_time = time.time()
        pr = cProfile.Profile()
        pr.enable()

        processor.process_locations(locations, mock_process_func)

        pr.disable()
        end_time = time.time()

        print(f"Fetching 100 locations took {end_time - start_time:.4f} seconds")

        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats(20)
        print(s.getvalue())

if __name__ == "__main__":
    run_concurrent_fetch_benchmark()
