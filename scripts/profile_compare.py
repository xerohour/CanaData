import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimized_data_processor import OptimizedDataProcessor

MOCK_MENU_ITEMS = {
    "loc-1": [
        {
            "id": f"item-{i}",
            "name": f"Product {i}",
            "price": {"amount": 50.0 + i, "currency": "USD"},
            "brand": {"name": "Brand X", "id": "brand-1"},
            "categories": [{"id": "c1", "name": "Flower"}, {"id": "c2", "name": "Indica"}],
            "strain": {"slug": "og-kush", "name": "OG Kush"},
            "test_results": {"thc": {"value": 20.0, "unit": "%"}, "cbd": {"value": 0.5, "unit": "%"}}
        } for i in range(1000)
    ] * 5
} # 5000 items

def run_profiling():
    processor = OptimizedDataProcessor()

    print("Profiling Pandas json_normalize...")
    start = time.time()
    processor._flatten_all_items(MOCK_MENU_ITEMS)
    print(f"Pandas took: {time.time() - start:.4f}s")

    print("Profiling Custom fallback...")
    items_with_location = []
    for loc_id, items in MOCK_MENU_ITEMS.items():
        for item in items:
            item_copy = item.copy()
            item_copy['_location_id'] = loc_id
            items_with_location.append(item_copy)

    start = time.time()
    processor._fallback_flattening(items_with_location)
    print(f"Fallback took: {time.time() - start:.4f}s")

if __name__ == "__main__":
    run_profiling()
