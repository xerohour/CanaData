import json
import os
import sys
import pytest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

from CanaData import CanaData

def test_map_reduce_throughput(benchmark):
    scraper = CanaData(interactive_mode=False)

    mock_results = [{
        'listing_id': i,
        'local_menu_items': [{'id': i}],
        'is_empty_menu': False,
        'listing_copy': {'id': i},
        'local_extracted_strains': {},
        'menu_items_count': 1,
        'listing_slug': f'slug-{i}',
        'discovery': False
    } for i in range(1000)]

    def process_data():
        scraper.allMenuItems = {}
        for result in mock_results:
            scraper._merge_menu_result(result)

    benchmark(process_data)
    assert len(scraper.allMenuItems) == 1000
