import os
import time
from unittest.mock import patch, MagicMock
from CanaData import CanaData

def _build_menu_payload(listing_id, slug, item_count=50, strain_slug='strain-a'):
    items = []
    for i in range(item_count):
        items.append({
            'id': f'item-{listing_id}-{i}',
            'name': f'Item {i}',
            'strain_data': {'slug': strain_slug, 'name': 'Shared Strain'}
        })

    return {
        'listing': {
            'id': listing_id,
            'slug': slug,
            '_type': 'dispensary',
            'wmid': f'wm-{listing_id}'
        },
        'categories': [
            {
                'name': 'Flower',
                'items': items
            }
        ]
    }

def simulate_network_delay(*args, **kwargs):
    time.sleep(0.01) # Simulate 10ms network latency

    # We return different data based on the URL to mock the menu request
    # If the URL is for discovery items, return None to trigger fallback
    # The fallback to legacy_url will trigger a mock response.
    mock_resp = MagicMock()
    mock_resp.status_code = 200

    # Extract url to generate a unique response
    url = args[0] if args else kwargs.get('url', '')
    if 'discovery' in url:
        return 'break' # Fail discovery to force fallback

    # Fallback response
    slug = url.split('/')[-2] if '/' in url else 'unknown'
    mock_resp.json.return_value = _build_menu_payload(listing_id=f'loc-{slug}', slug=slug, item_count=20)
    return mock_resp

def run_concurrent_menus():
    # Disable rate limiting for the test to isolate application logic
    os.environ['RATE_LIMIT'] = '0'
    os.environ['USE_CONCURRENT_PROCESSING'] = 'true'
    os.environ['MAX_WORKERS'] = '10'

    cana = CanaData()
    cana.searchSlug = 'test-slug'

    # Create 50 mock locations
    cana.locations = [
        {
            'id': f'loc-{i}',
            'wmid': f'wmid-{i}',
            'name': f'Store {i}',
            'slug': f'store-{i}',
            'type': 'dispensary',
            'state': 'CA',
            'city': 'LA'
        }
        for i in range(50)
    ]

    cana._getMenusConcurrent()
    return cana

@patch('requests.get', side_effect=simulate_network_delay)
@patch('requests.Session.get', side_effect=simulate_network_delay)
@patch('CanaData.CanaData._fetch_discovery_menu_items', return_value=None)
def test_thread_safety_and_latency(mock_discovery, mock_session_get, mock_get, benchmark):
    # The benchmark will run this multiple times to measure latency
    result = benchmark(run_concurrent_menus)

    # Verify thread safety and data integrity
    assert len(result.allMenuItems) == 50
    assert result.menuItemsFound == 50 * 20 # 50 locations * 20 items

    # We assign result to _ to avoid F841 if we didn't assert, but we just asserted so we're good.
    _ = result
