import sys
import os
from memory_profiler import profile
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

@profile
def profile_memory_processing():
    scraper = CanaData(interactive_mode=False)

    # Load sample data
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    if not os.path.exists(sample_file):
        print("Sample file not found")
        return

    with open(sample_file) as f:
        data = json.load(f)

    products = data.get('data', {}).get('products', [])

    mock_location = {"slug": "test-slug", "type": "dispensary", "id": "123", "wmid": 123}
    mock_menu_json = {
        "listing": mock_location,
        "categories": [
            {
                "title": "Flower",
                "items": products * 10 # Artificially inflate
            }
        ]
    }

    for i in range(10): # 10 locations
        # Modify ID so it aggregates to different keys
        mock_menu_json["listing"]["id"] = f"123_{i}"
        result = scraper.process_menu_json(mock_menu_json)
        scraper._aggregate_menu_result(result)

    assert len(scraper.allMenuItems) == 10

if __name__ == '__main__':
    profile_memory_processing()
