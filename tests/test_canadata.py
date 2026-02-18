"""Tests for the core CanaData class: initialization, caching, requests, flattening, and CSV export."""

import os
import time
import pickle
import hashlib
import json
import csv
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime

import pytest
import responses

from CanaData import CanaData


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

class TestInit:
    def test_default_attributes(self, cana):
        assert cana.baseUrl == 'https://api-g.weedmaps.com/discovery/v1/listings'
        assert cana.pageSize == '&page_size=100&size=100'
        assert cana.searchSlug is None
        assert cana.storefronts is True
        assert cana.deliveries is True
        assert cana.locationsFound == 0
        assert cana.testMode is False
        assert cana.menuItemsFound == 0
        assert cana.maxLocations is None
        assert cana.locations == []
        assert cana.emptyMenus == {}
        assert cana.allMenuItems == {}
        assert cana.finishedMenuItems == []
        assert cana.totalLocations == []
        assert cana.unFriendlyStates == []
        assert cana.NonGreenState is False
        assert cana.slugGrab is False

    def test_concurrency_defaults(self, cana):
        assert cana.maxWorkers == 5
        assert cana.rateLimitDelay == 0  # overridden in fixture
        assert cana.cacheExpiry == 86400

    def test_cache_dir_created(self, cana):
        assert os.path.isdir(cana.cacheDir)


# ---------------------------------------------------------------------------
# Disk caching
# ---------------------------------------------------------------------------

class TestCaching:
    def test_set_and_get_cache(self, cana):
        key = 'https://example.com/api?page=1'
        data = {'meta': {'total': 5}, 'data': [1, 2, 3]}
        cana._set_cache(key, data)
        result = cana._get_cache(key)
        assert result == data

    def test_get_cache_miss(self, cana):
        assert cana._get_cache('https://nonexistent.example.com') is None

    def test_cache_expiry(self, cana):
        key = 'https://example.com/expired'
        data = {'expired': True}
        cana._set_cache(key, data)

        cache_file = os.path.join(cana.cacheDir, hashlib.md5(key.encode()).hexdigest())
        # Backdate the file modification time to exceed the expiry window
        old_time = time.time() - cana.cacheExpiry - 100
        os.utime(cache_file, (old_time, old_time))

        assert cana._get_cache(key) is None

    def test_cache_corrupt_file(self, cana):
        key = 'https://example.com/corrupt'
        cache_file = os.path.join(cana.cacheDir, hashlib.md5(key.encode()).hexdigest())
        with open(cache_file, 'wb') as f:
            f.write(b'not-valid-pickle')
        assert cana._get_cache(key) is None


# ---------------------------------------------------------------------------
# do_request
# ---------------------------------------------------------------------------

class TestDoRequest:
    @responses.activate
    def test_success_200(self, cana):
        url = 'https://api-g.weedmaps.com/discovery/v1/test'
        payload = {'data': 'ok'}
        responses.add(responses.GET, url, json=payload, status=200)

        result = cana.do_request(url)
        assert result == payload

    @responses.activate
    def test_success_caches_result(self, cana):
        url = 'https://api-g.weedmaps.com/discovery/v1/cached'
        payload = {'cached': True}
        responses.add(responses.GET, url, json=payload, status=200)

        cana.do_request(url)
        # Second call should return cached data without making a request
        result = cana.do_request(url)
        assert result == payload
        # Only one actual HTTP call should have been made
        assert len(responses.calls) == 1

    @responses.activate
    def test_422_returns_break(self, cana):
        url = 'https://api-g.weedmaps.com/discovery/v1/bad'
        responses.add(responses.GET, url, json={'error': 'bad'}, status=422)

        result = cana.do_request(url)
        assert result == 'break'

    @responses.activate
    def test_503_retries_then_fails(self, cana):
        url = 'https://api-g.weedmaps.com/discovery/v1/unavail'
        responses.add(responses.GET, url, body='Service Unavailable', status=503)
        responses.add(responses.GET, url, body='Service Unavailable', status=503)
        responses.add(responses.GET, url, body='Service Unavailable', status=503)

        result = cana.do_request(url, retry_count=3)
        assert result is False
        assert len(responses.calls) == 3

    @responses.activate
    def test_503_retries_then_succeeds(self, cana):
        url = 'https://api-g.weedmaps.com/discovery/v1/retry-ok'
        responses.add(responses.GET, url, body='Service Unavailable', status=503)
        responses.add(responses.GET, url, json={'data': 'recovered'}, status=200)

        result = cana.do_request(url, retry_count=3)
        assert result == {'data': 'recovered'}
        assert len(responses.calls) == 2

    @responses.activate
    def test_other_error_returns_false(self, cana):
        url = 'https://api-g.weedmaps.com/discovery/v1/err'
        responses.add(responses.GET, url, body='Internal Server Error', status=500)

        result = cana.do_request(url)
        assert result is False

    def test_network_exception_retries(self, cana):
        import requests as req_lib
        url = 'https://api-g.weedmaps.com/discovery/v1/timeout'

        with patch.object(req_lib, 'get', side_effect=req_lib.exceptions.ConnectionError('fail')):
            result = cana.do_request(url, retry_count=2)
        assert result is False


# ---------------------------------------------------------------------------
# flatten_dictionary
# ---------------------------------------------------------------------------

class TestFlattenDictionary:
    def test_simple_dict(self, cana):
        nested = {
            'name': 'Great Product',
            'price': {'amount': 10, 'currency': 'USD'},
        }
        flat = cana.flatten_dictionary(nested)
        assert flat['name'] == 'Great Product'
        assert flat['price.amount'] == '10'
        assert flat['price.currency'] == 'USD'

    def test_list_of_strings(self, cana):
        nested = {'tags': ['calm', 'sweet']}
        flat = cana.flatten_dictionary(nested)
        assert flat['tags'] == "['calm', 'sweet']"

    def test_empty_dict_value(self, cana):
        nested = {'empty_dict': {}}
        flat = cana.flatten_dictionary(nested)
        assert flat['empty_dict'] == 'None'

    def test_empty_list_value(self, cana):
        nested = {'empty_list': []}
        flat = cana.flatten_dictionary(nested)
        assert flat['empty_list'] == 'None'

    def test_nested_dict_in_list(self, cana):
        nested = {
            'items': [
                {'id': 1},
                {'id': 2},
            ]
        }
        flat = cana.flatten_dictionary(nested)
        # The stack-based algorithm processes dicts in a list by pushing them
        assert 'items.id' in flat

    def test_deeply_nested(self, cana):
        nested = {
            'a': {
                'b': {
                    'c': 'deep_value'
                }
            }
        }
        flat = cana.flatten_dictionary(nested)
        assert flat['a.b.c'] == 'deep_value'

    def test_none_value(self, cana):
        nested = {'val': None}
        flat = cana.flatten_dictionary(nested)
        assert flat['val'] == 'None'

    def test_numeric_value(self, cana):
        nested = {'count': 42}
        flat = cana.flatten_dictionary(nested)
        assert flat['count'] == '42'


# ---------------------------------------------------------------------------
# organize_into_clean_list
# ---------------------------------------------------------------------------

class TestOrganizeIntoCleanList:
    def test_basic_organization(self, cana):
        cana.allMenuItems = {
            1: [
                {'name': 'Item A', 'price': {'amount': 10}},
                {'name': 'Item B', 'price': {'amount': 20}, 'extra': 'field'},
            ]
        }
        cana.organize_into_clean_list()

        assert len(cana.finishedMenuItems) == 2
        # All items should have all keys, with 'None' for missing
        keys_0 = set(cana.finishedMenuItems[0].keys())
        keys_1 = set(cana.finishedMenuItems[1].keys())
        assert keys_0 == keys_1

    def test_empty_menu_items(self, cana):
        cana.allMenuItems = {}
        cana.organize_into_clean_list()
        assert cana.finishedMenuItems == []


# ---------------------------------------------------------------------------
# setCitySlug and resetDataSets
# ---------------------------------------------------------------------------

class TestStateManagement:
    def test_set_city_slug(self, cana):
        cana.setCitySlug('colorado')
        assert cana.searchSlug == 'colorado'

    def test_reset_datasets(self, cana):
        cana.searchSlug = 'test'
        cana.locationsFound = 10
        cana.maxLocations = 100
        cana.locations = [{'slug': 'a', 'type': 'dispensary'}]
        cana.allMenuItems = {1: [{'name': 'item'}]}
        cana.finishedMenuItems = [{'name': 'item'}]
        cana.totalLocations = [{'id': 1}]
        cana.NonGreenState = True

        cana.resetDataSets()

        assert cana.searchSlug is None
        assert cana.locationsFound == 0
        assert cana.maxLocations is None
        assert cana.locations == []
        assert cana.allMenuItems == {}
        assert cana.finishedMenuItems == []
        assert cana.totalLocations == []
        assert cana.NonGreenState is False

    def test_slugs_mode(self, cana):
        cana.slugs()
        assert cana.slugGrab is True

    def test_test_mode(self, cana):
        cana.TestMode()
        assert cana.testMode is True


# ---------------------------------------------------------------------------
# identifyNaughtyStates
# ---------------------------------------------------------------------------

class TestIdentifyNaughtyStates:
    def test_with_unfriendly_states(self, cana, capsys):
        cana.unFriendlyStates = ['idaho', 'wyoming']
        cana.identifyNaughtyStates()
        captured = capsys.readouterr()
        assert 'idaho' in captured.out
        assert 'wyoming' in captured.out

    def test_no_unfriendly_states(self, cana, capsys):
        cana.unFriendlyStates = []
        cana.identifyNaughtyStates()
        captured = capsys.readouterr()
        assert captured.out == ''


# ---------------------------------------------------------------------------
# csv_maker and dataToCSV
# ---------------------------------------------------------------------------

class TestCSVExport:
    def test_csv_maker(self, cana, tmp_path):
        # Override path[0] so the CSV goes to our temp dir
        with patch('CanaData.path', [str(tmp_path)]):
            data = [
                {'name': 'Item 1', 'price': '10'},
                {'name': 'Item 2', 'price': '20'},
            ]
            cana.searchSlug = 'test-city'
            cana.csv_maker('test_output', data)

            today = datetime.today().strftime('%m-%d-%Y')
            csv_path = tmp_path / f'CanaData_{today}' / 'test_output.csv'
            assert csv_path.exists()

            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
            assert rows[0] == ['name', 'price']
            assert len(rows) == 3  # header + 2 data rows

    def test_data_to_csv_skips_non_green_state(self, cana):
        cana.NonGreenState = True
        # Should return early without error
        cana.dataToCSV()


# ---------------------------------------------------------------------------
# getMenus (concurrent processing)
# ---------------------------------------------------------------------------

class TestGetMenus:
    def test_skips_non_green_state(self, cana):
        cana.NonGreenState = True
        cana.getMenus()
        # Should return immediately without errors

    @responses.activate
    def test_concurrent_menu_fetch(self, cana):
        """Test that getMenus processes multiple locations concurrently."""
        cana.locations = [
            {'slug': 'dispensary-a', 'type': 'dispensary'},
            {'slug': 'dispensary-b', 'type': 'dispensary'},
        ]

        menu_a = {
            'listing': {
                'id': 1, 'slug': 'dispensary-a', 'wmid': 100,
                '_type': 'dispensary', 'name': 'Dispensary A',
            },
            'categories': [
                {
                    'title': 'Flower',
                    'items': [
                        {'id': 10, 'name': 'Blue Dream', 'price': 30},
                        {'id': 11, 'name': 'OG Kush', 'price': 35},
                    ]
                }
            ]
        }
        menu_b = {
            'listing': {
                'id': 2, 'slug': 'dispensary-b', 'wmid': 200,
                '_type': 'delivery', 'name': 'Delivery B',
            },
            'categories': []
        }

        responses.add(
            responses.GET,
            'https://weedmaps.com/api/web/v1/listings/dispensary-a/menu',
            json=menu_a, status=200,
        )
        responses.add(
            responses.GET,
            'https://weedmaps.com/api/web/v1/listings/dispensary-b/menu',
            json=menu_b, status=200,
        )

        cana.getMenus()

        # dispensary-a had 2 items
        assert cana.menuItemsFound == 2
        assert 1 in cana.allMenuItems
        assert len(cana.allMenuItems[1]) == 2

        # dispensary-b had empty menu, should be in emptyMenus
        assert 2 in cana.emptyMenus
        assert len(cana.totalLocations) == 2

    @responses.activate
    def test_menu_fetch_failure_skips_location(self, cana):
        """Locations that fail to fetch should be skipped gracefully."""
        cana.locations = [
            {'slug': 'bad-shop', 'type': 'dispensary'},
        ]
        responses.add(
            responses.GET,
            'https://weedmaps.com/api/web/v1/listings/bad-shop/menu',
            body='Internal Server Error', status=500,
        )

        cana.getMenus()
        assert cana.menuItemsFound == 0
        assert len(cana.allMenuItems) == 0


# ---------------------------------------------------------------------------
# getLocations
# ---------------------------------------------------------------------------

class TestGetLocations:
    @responses.activate
    def test_get_locations_success(self, cana):
        cana.setCitySlug('colorado')
        api_response = {
            'meta': {'total_listings': 2},
            'data': {
                'listings': [
                    {'slug': 'shop-1', 'type': 'dispensary'},
                    {'slug': 'shop-2', 'type': 'delivery'},
                ]
            }
        }
        responses.add(
            responses.GET,
            'https://api-g.weedmaps.com/discovery/v1/listings',
            json=api_response, status=200,
        )

        cana.getLocations()

        assert cana.locationsFound == 2
        assert cana.maxLocations == 2
        assert len(cana.locations) == 2
        assert cana.locations[0]['slug'] == 'shop-1'

    @responses.activate
    def test_get_locations_zero_results(self, cana):
        cana.setCitySlug('unfriendly-state')
        api_response = {
            'meta': {'total_listings': 0},
            'data': {'listings': []}
        }
        responses.add(
            responses.GET,
            'https://api-g.weedmaps.com/discovery/v1/listings',
            json=api_response, status=200,
        )

        cana.getLocations()

        assert cana.NonGreenState is True
        assert 'unfriendly-state' in cana.unFriendlyStates

    @responses.activate
    def test_get_locations_422_break(self, cana):
        cana.setCitySlug('broken')
        responses.add(
            responses.GET,
            'https://api-g.weedmaps.com/discovery/v1/listings',
            json={'error': 'unprocessable'}, status=422,
        )

        cana.getLocations()
        assert cana.locationsFound == 0
