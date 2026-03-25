import pytest
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor
from tests.test_canadata import _build_menu_payload

def build_large_payload(num_locations=20, items_per_location=50):
    all_menu_items = {}
    for i in range(num_locations):
        loc_id = f"loc-{i}"
        items = []
        for j in range(items_per_location):
            items.append({
                "id": f"item-{i}-{j}",
                "name": f"Item {j}",
                "price": {"amount": j * 10, "currency": "USD"},
                "strain_data": {"name": f"Strain {j}", "slug": f"strain-{j}"},
                "tags": ["indica", "flower", f"tag-{j}"],
                "locations_found_at": [f"/dispensaries/loc-{i}"],
                "listing_id": loc_id,
                "listing_wmid": f"wm-{loc_id}",
                "deeply_nested": {"level1": {"level2": {"level3": "value"}}},
                "images": [{"url": "url1", "size": "small"}, {"url": "url2", "size": "large"}]
            })
        all_menu_items[loc_id] = items
    return all_menu_items

@pytest.fixture
def payload():
    return build_large_payload()

def test_benchmark_custom_flattening(benchmark, payload):
    def run_custom():
        cana = CanaData(optimize_processing=False)
        cana.allMenuItems = payload
        cana.organize_into_clean_list()
        return cana.finishedMenuItems

    result = benchmark(run_custom)
    assert len(result) == 1000

def test_benchmark_optimized_flattening(benchmark, payload):
    def run_optimized():
        cana = CanaData(optimize_processing=True)
        cana.allMenuItems = payload
        cana.organize_into_clean_list()
        return cana.finishedMenuItems

    result = benchmark(run_optimized)
    assert len(result) == 1000

def test_benchmark_flatten_dictionary_single(benchmark):
    cana = CanaData()
    item = {
        "id": "item-1",
        "name": "Item Name",
        "price": {"amount": 10, "currency": "USD"},
        "tags": ["indica", "flower"],
        "deeply_nested": {"level1": {"level2": {"level3": "value"}}},
        "images": [{"url": "url1", "size": "small"}, {"url": "url2", "size": "large"}]
    }

    result = benchmark(cana.flatten_dictionary, item)
    assert "price.amount" in result

def test_benchmark_optimized_flatten_dictionary_single(benchmark):
    processor = OptimizedDataProcessor()
    item = {
        "id": "item-1",
        "name": "Item Name",
        "price": {"amount": 10, "currency": "USD"},
        "tags": ["indica", "flower"],
        "deeply_nested": {"level1": {"level2": {"level3": "value"}}},
        "images": [{"url": "url1", "size": "small"}, {"url": "url2", "size": "large"}]
    }

    result = benchmark(processor._flatten_dictionary_custom, item)
    assert "price.amount" in result
