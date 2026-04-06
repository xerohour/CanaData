import time
import cProfile
import pstats
import io
import json
import random
from memory_profiler import profile
from optimized_data_processor import OptimizedDataProcessor
from CanaData import CanaData
import pandas as pd

# Generate Mock Data
def generate_mock_data(num_locations=10, items_per_location=500):
    all_menu_items = {}
    for i in range(num_locations):
        location_id = f"loc_{i}"
        items = []
        for j in range(items_per_location):
            # Create a deeply nested item similar to Weedmaps API response
            item = {
                "id": f"item_{i}_{j}",
                "name": f"Product {j}",
                "brand": {"id": 123, "name": "BrandX"},
                "price": {"amount": random.uniform(10, 100), "currency": "USD"},
                "thc": {"amount": random.uniform(15, 30), "unit": "%"},
                "categories": [{"id": 1, "name": "Flower"}],
                "strain_data": {"slug": f"strain_{j}", "name": f"Strain {j}"},
                "locations_found_at": [f"/dispensaries/loc_{i}"]
            }
            items.append(item)
        all_menu_items[location_id] = items
    return all_menu_items

mock_data = generate_mock_data(5, 1000) # 5 locations, 1000 items each = 5000 total items
mock_data_small = generate_mock_data(1, 100) # 100 items

processor = OptimizedDataProcessor(max_workers=4)

@profile
def test_pandas_flattening():
    print("\n--- Running Pandas Flattening ---")
    start = time.time()
    result = processor.process_menu_data(mock_data)
    end = time.time()
    print(f"Pandas processing took {end - start:.4f} seconds for {len(result)} items.")

@profile
def test_custom_flattening():
    print("\n--- Running Custom Flattening ---")
    start = time.time()

    items = []
    for loc_id, loc_items in mock_data.items():
        for item in loc_items:
            items.append(item)

    # we need to fallback explicitly
    df = processor._fallback_flattening(items)

    end = time.time()
    print(f"Custom flattening took {end - start:.4f} seconds for {len(df)} items.")

def test_canadata_core():
    print("\n--- Profiling CanaData Initialization ---")
    pr = cProfile.Profile()
    pr.enable()

    app = CanaData(cache_enabled=False, optimize_processing=True, interactive_mode=False)

    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(20)
    print(s.getvalue())

if __name__ == "__main__":
    print("Starting Profiling Script...")

    # Run memory profiling
    test_pandas_flattening()
    test_custom_flattening()

    # Run CPU profiling
    test_canadata_core()

    # Profile full pandas run with cProfile
    pr = cProfile.Profile()
    pr.enable()
    processor.process_menu_data(mock_data_small)
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    print("\n--- Pandas Run cProfile ---")
    ps.print_stats(15)
    print(s.getvalue())

    # Profile custom run with cProfile
    items = []
    for loc_id, loc_items in mock_data_small.items():
        for item in loc_items:
            items.append(item)

    pr2 = cProfile.Profile()
    pr2.enable()
    processor._fallback_flattening(items)
    pr2.disable()
    s2 = io.StringIO()
    ps2 = pstats.Stats(pr2, stream=s2).sort_stats('cumulative')
    print("\n--- Custom Flattening Run cProfile ---")
    ps2.print_stats(15)
    print(s2.getvalue())
