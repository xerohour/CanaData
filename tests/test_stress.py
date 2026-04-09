import pytest
import responses
import requests
from CanaData import CanaData
import time
import os

@responses.activate
def test_rate_limit_and_timeout_resilience():
    # Setup CanaData without cache to strictly test do_request logic
    cana = CanaData(max_workers=5, rate_limit=0.1, interactive_mode=False, cache_enabled=False)

    # Mock endpoint mapping
    location_url = "https://api-g.weedmaps.com/discovery/v1/listings?offset=0&page_size=100&size=100&filter[any_retailer_services][]=storefront&filter[region_slug[dispensaries]]=stress-test&filter[any_retailer_services][]=delivery&filter[region_slug[deliveries]]=stress-test"

    # Add a mock that simulates 429 Too Many Requests
    responses.add(
        responses.GET,
        location_url,
        status=429,
        json={"error": "Rate limited"}
    )

    cana.set_city_slug("stress-test")
    cana.get_locations()

    # The current implementation of do_request does not automatically retry on 429.
    # It logs a warning and returns False.
    # We expect locations to be empty because the request fails.
    assert len(cana.locations) == 0

@responses.activate
def test_concurrent_menu_processor_stress():
    # Setup CanaData
    cana = CanaData(max_workers=20, rate_limit=0.01, interactive_mode=False)

    # Set up 50 mock locations
    cana.locations = [{"id": f"loc_{i}", "slug": f"slug_{i}", "type": "dispensary"} for i in range(50)]

    # Setup mock responses for all 50 locations
    for i in range(50):
        url = f"https://api-g.weedmaps.com/discovery/v1/listings/dispensaries/slug_{i}/menu_items?page=1&page_size=100&size=100"
        responses.add(
            responses.GET,
            url,
            status=200,
            json={
                "data": {
                    "menu_items": [{"id": f"item_{i}_{j}", "name": f"Item {j}"} for j in range(10)]
                },
                "meta": {"total_menu_items": 10}
            }
        )

    # Force using concurrent processing
    os.environ['USE_CONCURRENT_PROCESSING'] = 'true'

    start_time = time.time()
    cana.getMenus()
    end_time = time.time()

    print(f"Time to fetch 50 menus concurrently: {end_time - start_time:.2f}s")

    # Verify all 50 menus were fetched (50 * 10 = 500 items)
    assert cana.menuItemsFound == 500
    assert len(cana.allMenuItems) == 50
