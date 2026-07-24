from CanaData import CanaData


def test_api_calls_efficiency():
    # Looking for N+1 queries by tracing API requests
    scraper = CanaData(optimize_processing=True)
    scraper.testMode = True
    scraper.city_slug = "test-city"
    scraper.state_slug = "test-state"
    scraper.allLocations = [{"slug": "loc1", "type": "dispensary"}, {"slug": "loc2", "type": "delivery"}]

    # We will mock the request method to see how many requests it makes
    request_count = 0
    def mock_fetch(url, *args, **kwargs):
        nonlocal request_count
        request_count += 1
        return {"data": {"menu_items": [{"id": "1", "name": "l1"}]}}

    scraper._fetch_discovery_menu_items = lambda slug, t: mock_fetch(slug)

    # This might fetch menus for each location
    scraper.getMenus()

    print(f"Total API requests for {len(scraper.allLocations)} locations: {request_count}")
    assert request_count <= len(scraper.allLocations)
