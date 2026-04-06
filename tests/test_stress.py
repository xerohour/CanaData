import pytest
import threading
import time
from CanaData import CanaData

def test_menu_data_lock_concurrency():
    """
    Test the self._menu_data_lock inside process_menu_items_json
    to ensure it avoids race conditions when updating shared dicts/lists.
    """
    app = CanaData(cache_enabled=False, optimize_processing=False, interactive_mode=False)
    app.searchSlug = "test-slug"

    # Simulate processing multiple locations concurrently
    num_threads = 50
    items_per_thread = 20

    def simulate_processing(thread_id):
        location = {"slug": f"loc-{thread_id}", "type": "dispensary", "id": thread_id}
        # Simulate a Weedmaps discovery API response
        menu_json = {
            "data": {
                "menu_items": [
                    {"name": f"Item {j}", "strain_data": {"slug": f"strain-{thread_id}-{j}"}}
                    for j in range(items_per_thread)
                ]
            }
        }

        # This calls the lock internally
        app.process_menu_items_json(menu_json, location)

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=simulate_processing, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Verify counts reflect atomic operations
    assert app.menuItemsFound == num_threads * items_per_thread
    assert len(app.totalLocations) == num_threads
    assert len(app.allMenuItems.keys()) == num_threads
    assert len(app.extractedStrains.keys()) == num_threads * items_per_thread

def test_api_422_validation_break():
    """
    Test how the app handles a 422 validation error
    """
    app = CanaData(cache_enabled=False, optimize_processing=False, interactive_mode=False)

    # We will mock the do_request to return 'break' on 422
    import responses
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            'https://api-g.weedmaps.com/discovery/v1/listings/dispensaries/test-loc/menu_items?page=1&page_size=100&size=100',
            json={'errors': [{'detail': 'Invalid Page'}]},
            status=422
        )

        # Test how _fetch_discovery_menu_items handles the 'break'
        result = app._fetch_discovery_menu_items('test-loc', 'dispensaries')
        assert result is None # Should gracefully return None when hitting 'break'
