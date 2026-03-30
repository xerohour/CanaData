import pytest
import concurrent.futures
from CanaData import CanaData

def _build_menu_payload(listing_id, slug, item_count=2, strain_slug='strain-a'):
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

def test_concurrent_state_mutation():
    cana = CanaData()
    total_payloads = 100
    items_per_payload = 3

    payloads = [
        _build_menu_payload(listing_id=f'loc-{i}', slug=f'slug-{i}', item_count=items_per_payload)
        for i in range(total_payloads)
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(cana.process_menu_json, payload) for payload in payloads]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    assert len(cana.allMenuItems) == total_payloads
    assert cana.menuItemsFound == total_payloads * items_per_payload
