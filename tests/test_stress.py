import pytest
import concurrent.futures
from CanaData import CanaData
from concurrent_processor import ConcurrentMenuProcessor

def test_concurrent_processor_stress():
    processor = ConcurrentMenuProcessor(max_workers=50, rate_limit=0)

    locations = [{"slug": f"loc-{i}", "type": "dispensary"} for i in range(200)]

    def process_func(loc):
        return {"items": [1, 2, 3]}

    results = processor.process_locations(locations, process_func)

    assert len(results) == 200

def test_canadata_concurrent_stress():
    cana = CanaData(max_workers=20, rate_limit=0, interactive_mode=False)
    total_payloads = 100

    def process_payload(i):
        payload = {
            'listing': {'id': f'loc-{i}', 'slug': f'slug-{i}', 'wmid': f'wm-{i}'},
            'categories': [{'items': [{'name': 'Item A'}, {'name': 'Item B'}]}]
        }
        cana.process_menu_json(payload)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        list(executor.map(process_payload, range(total_payloads)))

    assert len(cana.allMenuItems) == total_payloads
