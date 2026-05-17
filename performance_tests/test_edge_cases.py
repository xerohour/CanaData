import pytest
import responses
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CanaData import CanaData

@responses.activate
def test_mock_api_failure():
    responses.add(
        responses.GET,
        'https://api-g.weedmaps.com/discovery/v1/listings/dispensaries/test-slug/menu_items?page=1&page_size=100&size=100',
        status=500
    )
    responses.add(
        responses.GET,
        'https://weedmaps.com/api/web/v1/listings/test-slug/menu?type=dispensary',
        status=500
    )

    scraper = CanaData(interactive_mode=False)
    scraper.TestMode()
    location = {'slug': 'test-slug', 'type': 'dispensary'}

    result = scraper._fetch_and_process_menu(location)
    assert result is False
