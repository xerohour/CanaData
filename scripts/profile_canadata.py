import cProfile
import pstats
import io
import time
import os
import sys

# Add root directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CanaData import CanaData
from unittest.mock import patch

# Create mock data
MOCK_LOCATIONS = [
    {"id": "1", "slug": "loc-1", "type": "dispensary", "wmid": "wmid-1", "name": "Loc 1"},
    {"id": "2", "slug": "loc-2", "type": "delivery", "wmid": "wmid-2", "name": "Loc 2"}
] * 10 # 20 locations

MOCK_MENU_ITEMS = [
    {
        "id": f"item-{i}",
        "name": f"Product {i}",
        "price": {"amount": 50.0 + i, "currency": "USD"},
        "brand": {"name": "Brand X"},
        "categories": [{"id": "c1", "name": "Flower"}],
        "strain": {"slug": "og-kush", "name": "OG Kush"},
        "test_results": {"thc": {"value": 20.0, "unit": "%"}}
    } for i in range(100)
] # 100 items per location

def mock_do_request(self, url, use_cache=True):
    # Simulate network latency
    time.sleep(0.01)

    if "menu_items" in url:
        # Mock discovery menu items
        return {
            "meta": {"total_menu_items": len(MOCK_MENU_ITEMS)},
            "data": {"menu_items": MOCK_MENU_ITEMS}
        }
    return None

def run_profiling():
    print("Initializing CanaData for profiling...")
    os.environ['MAX_WORKERS'] = '5'
    os.environ['RATE_LIMIT'] = '0'
    os.environ['USE_CONCURRENT_PROCESSING'] = 'true'

    cana = CanaData(max_workers=5, rate_limit=0, cache_enabled=False, optimize_processing=True, interactive_mode=False)
    cana.searchSlug = "test-slug"
    cana.locations = MOCK_LOCATIONS

    print(f"Processing {len(MOCK_LOCATIONS)} locations with {len(MOCK_MENU_ITEMS)} items each...")

    pr = cProfile.Profile()
    pr.enable()

    with patch('CanaData.CanaData.do_request', new=mock_do_request):
        cana.getMenus()

    pr.disable()

    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(30)

    print(s.getvalue())

if __name__ == "__main__":
    run_profiling()
