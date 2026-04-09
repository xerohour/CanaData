import cProfile
import pstats
import io
import time
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def generate_mock_data(num_locations=50, items_per_loc=100):
    all_menu_items = {}
    for i in range(num_locations):
        loc_id = f"loc_{i}"
        items = []
        for j in range(items_per_loc):
            items.append({
                "id": f"item_{i}_{j}",
                "name": f"Product {i}-{j}",
                "price": {"amount": 50, "currency": "USD"},
                "thc": "20%",
                "brand": {"name": "Test Brand", "slug": "test-brand"},
                "category": "Flower",
                "nested": {
                    "level1": {
                        "level2": {
                            "value": 123
                        }
                    }
                }
            })
        all_menu_items[loc_id] = items
    return all_menu_items

def profile_custom_flatten(data):
    processor = OptimizedDataProcessor(max_workers=4)
    # Using fallback logic which calls _flatten_dictionary_custom
    processor._fallback_flattening([item for items in data.values() for item in items])

def profile_pandas_flatten(data):
    processor = OptimizedDataProcessor(max_workers=4)
    processor._flatten_all_items(data)

def main():
    print("Generating mock data...")
    data = generate_mock_data()
    print(f"Generated {sum(len(items) for items in data.values())} items")

    print("\nProfiling Custom Flattening (Stack-based)")
    pr_custom = cProfile.Profile()
    pr_custom.enable()
    profile_custom_flatten(data)
    pr_custom.disable()

    s_custom = io.StringIO()
    ps_custom = pstats.Stats(pr_custom, stream=s_custom).sort_stats('tottime')
    ps_custom.print_stats(10)
    print(s_custom.getvalue())

    print("\nProfiling Pandas Flattening")
    pr_pandas = cProfile.Profile()
    pr_pandas.enable()
    profile_pandas_flatten(data)
    pr_pandas.disable()

    s_pandas = io.StringIO()
    ps_pandas = pstats.Stats(pr_pandas, stream=s_pandas).sort_stats('tottime')
    ps_pandas.print_stats(10)
    print(s_pandas.getvalue())

if __name__ == "__main__":
    main()
