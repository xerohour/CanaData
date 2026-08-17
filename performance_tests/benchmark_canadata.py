import cProfile
import io
import json
import pstats
import time

from memory_profiler import profile

from CanaData import CanaData

# Setup mock data for performance testing
mock_data = []
with open("sample_products.json", "r") as f:
    mock_data = json.load(f)

# Mock location data
mock_location = {"slug": "test-slug", "name": "Test Location", "type": "dispensary"}


def run_flatten_benchmark():
    scraper = CanaData()
    start_time = time.time()
    for item in mock_data.get("data", {}).get("menu_items", []):
        scraper.flatten_dictionary(item)
    print(f"Flattening took {time.time() - start_time:.4f}s")


@profile
def run_memory_benchmark():
    scraper = CanaData()
    # add a bunch of items to self.allMenuItems
    items = mock_data.get("data", {}).get("menu_items", []) * 10  # duplicate for scale
    scraper.allMenuItems["test-listing"] = items

    # Process
    scraper.organize_into_clean_list()


if __name__ == "__main__":
    print("Running flattening benchmark...")
    pr = cProfile.Profile()
    pr.enable()
    run_flatten_benchmark()
    pr.disable()

    s = io.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(20)
    print(s.getvalue())

    print("Running memory benchmark...")
    run_memory_benchmark()
