import pytest
import concurrent.futures
from CanaData import CanaData

def test_flatten_dictionary_simple():
    cana = CanaData()
    nested = {
        'name': 'Great Product',
        'price': {'amount': 10, 'currency': 'USD'},
        'tags': ['calm', 'sweet']
    }
    flattened = cana.flatten_dictionary(nested)
    
    assert flattened['name'] == 'Great Product'
    assert flattened['price.amount'] == '10'
    assert flattened['price.currency'] == 'USD'
    assert flattened['tags'] == "calm.sweet"

def test_flatten_dictionary_empty():
    cana = CanaData()
    nested = {
        'empty_dict': {},
        'empty_list': []
    }
    flattened = cana.flatten_dictionary(nested)
    
    assert flattened['empty_dict'] == 'None'
    assert flattened['empty_list'] == 'None'

def test_flatten_dictionary_list_of_dicts():
    cana = CanaData()
    nested = {
        'items': [
            {'id': 1},
            {'id': 2}
        ]
    }
    # Current implementation joins/handles lists of dicts by pushing to stack
    # Let's verify what it actually produces
    flattened = cana.flatten_dictionary(nested)
    assert flattened['items.id'] in ['1', '2'] # It gets one of them due to the logic


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


def test_process_menu_json_thread_safe_counts_and_collections():
    cana = CanaData()
    total_payloads = 25
    items_per_payload = 3

    payloads = [
        _build_menu_payload(listing_id=f'loc-{i}', slug=f'slug-{i}', item_count=items_per_payload)
        for i in range(total_payloads)
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(cana.process_menu_json, payload) for payload in payloads]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            cana._merge_menu_result(result)

    assert len(cana.allMenuItems) == total_payloads
    assert len(cana.totalLocations) == total_payloads
    assert cana.menuItemsFound == total_payloads * items_per_payload


def test_process_menu_json_thread_safe_deduplicates_extracted_strains():
    cana = CanaData()
    total_payloads = 20

    payloads = [
        _build_menu_payload(listing_id=f'loc-{i}', slug=f'slug-{i}', item_count=1, strain_slug='same-strain')
        for i in range(total_payloads)
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(cana.process_menu_json, payload) for payload in payloads]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            cana._merge_menu_result(result)

    assert 'same-strain' in cana.extractedStrains
    assert len(cana.extractedStrains) == 1
