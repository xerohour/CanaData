import cProfile
import pstats
import io
import time
from unittest.mock import patch
from CanaData import CanaData

def run_profile():
    cana = CanaData()
    cana.max_workers = 10
    cana.rate_limit = 0 # No rate limit for fast profiling

    # We will provide 50 fake locations
    locations_to_process = [{"slug": f"test-loc-{i}", "type": "dispensary"} for i in range(50)]
    cana.locations = locations_to_process

    print(f"Profiling sequential vs concurrent processing of {len(locations_to_process)} locations...")

    # Mock the actual fetch to simulate network I/O
    def mock_fetch_and_process(location):
        # Simulate network latency
        time.sleep(0.05)
        # We don't return anything since `_fetch_and_process_menu` typically populates
        # the internal `allMenuItems` and doesn't return anything itself,
        # but in concurrent mode it might return a dictionary.
        # The logic handles it either way.
        return {"items": [{"name": f"Mock Item {i}"} for i in range(10)]}

    pr = cProfile.Profile()
    pr.enable()

    with patch.object(CanaData, '_fetch_and_process_menu', side_effect=mock_fetch_and_process):
        # Profile Concurrent Mode First
        start = time.time()
        print("Starting concurrent execution...")
        cana._getMenusConcurrent()
        end_conc = time.time()
        print(f"Concurrent execution completed in {end_conc - start:.2f} seconds.")

        # Profile Sequential Mode Second
        start = time.time()
        print("Starting sequential execution...")
        cana._getMenusSequential()
        end_seq = time.time()
        print(f"Sequential execution completed in {end_seq - start:.2f} seconds.")

    pr.disable()

    print("\n--- Profiling Results ---")
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(30)
    print(s.getvalue())

if __name__ == '__main__':
    run_profile()
