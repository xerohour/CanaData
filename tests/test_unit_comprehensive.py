"""
Comprehensive unit tests for CanaData core functionality,
cache manager, concurrent processor, and optimized data processor.
"""

import time
import json
import pytest
from unittest.mock import Mock, patch, MagicMock

from cache_manager import CacheManager
from concurrent_processor import ConcurrentMenuProcessor, retry_with_backoff
from optimized_data_processor import OptimizedDataProcessor


# ---------------------------------------------------------------------------
# CanaData core tests
# ---------------------------------------------------------------------------

class TestCanaDataCore:
    """Tests for core CanaData initialization and helpers."""

    def test_initialization_defaults(self, canadata_instance):
        """Verify default attribute values after construction."""
        assert canadata_instance.baseUrl is not None
        assert "&page_size=" in canadata_instance.pageSize
        assert canadata_instance.locations == []
        assert canadata_instance.allMenuItems == {}
        assert canadata_instance.finishedMenuItems == []
        assert canadata_instance.NonGreenState is False
        assert canadata_instance.menuItemsFound == 0

    def test_set_city_slug(self, canadata_instance):
        """setCitySlug should update searchSlug."""
        canadata_instance.setCitySlug("los-angeles")
        assert canadata_instance.searchSlug == "los-angeles"

    def test_reset_datasets(self, canadata_instance):
        """resetDataSets should clear per-slug state."""
        canadata_instance.searchSlug = "test"
        canadata_instance.locationsFound = 5
        canadata_instance.locations = [{"slug": "x", "type": "dispensary"}]
        canadata_instance.allMenuItems = {"x": []}
        canadata_instance.NonGreenState = True

        canadata_instance.resetDataSets()

        assert canadata_instance.searchSlug is None
        assert canadata_instance.locationsFound == 0
        assert canadata_instance.locations == []
        assert canadata_instance.allMenuItems == {}
        assert canadata_instance.NonGreenState is False

    def test_test_mode_toggle(self, canadata_instance):
        """TestMode should flip the testMode flag."""
        assert canadata_instance.testMode is False
        canadata_instance.TestMode()
        assert canadata_instance.testMode is True


# ---------------------------------------------------------------------------
# flatten_dictionary tests
# ---------------------------------------------------------------------------

class TestFlattenDictionary:
    """Tests for the stack-based dictionary flattener."""

    def test_simple_nested(self, canadata_instance):
        nested = {
            "name": "Great Product",
            "price": {"amount": 10, "currency": "USD"},
            "tags": ["calm", "sweet"],
        }
        flat = canadata_instance.flatten_dictionary(nested)

        assert flat["name"] == "Great Product"
        assert flat["price.amount"] == "10"
        assert flat["price.currency"] == "USD"

    def test_empty_containers(self, canadata_instance):
        nested = {"empty_dict": {}, "empty_list": []}
        flat = canadata_instance.flatten_dictionary(nested)

        assert flat["empty_dict"] == "None"
        assert flat["empty_list"] == "None"

    def test_none_value(self, canadata_instance):
        nested = {"key": None}
        flat = canadata_instance.flatten_dictionary(nested)
        assert flat["key"] == "None"

    def test_deeply_nested(self, canadata_instance):
        nested = {"a": {"b": {"c": {"d": "deep"}}}}
        flat = canadata_instance.flatten_dictionary(nested)
        assert flat["a.b.c.d"] == "deep"

    def test_flat_dict_passthrough(self, canadata_instance):
        flat_input = {"x": "1", "y": "2"}
        flat = canadata_instance.flatten_dictionary(flat_input)
        assert flat == {"x": "1", "y": "2"}

    def test_numeric_values_become_strings(self, canadata_instance):
        nested = {"count": 42, "ratio": 3.14, "flag": True}
        flat = canadata_instance.flatten_dictionary(nested)
        assert flat["count"] == "42"
        assert flat["ratio"] == "3.14"
        assert flat["flag"] == "True"


# ---------------------------------------------------------------------------
# process_menu_json tests
# ---------------------------------------------------------------------------

class TestProcessMenuJson:
    """Tests for menu JSON processing logic."""

    def test_basic_processing(self, canadata_instance, sample_menu_json):
        """Items should be stored under the listing ID."""
        canadata_instance.process_menu_json(sample_menu_json)

        listing_id = sample_menu_json["listing"]["id"]
        assert listing_id in canadata_instance.allMenuItems
        assert len(canadata_instance.allMenuItems[listing_id]) == 3
        assert canadata_instance.menuItemsFound == 3

    def test_strain_extraction(self, canadata_instance, sample_menu_json):
        """Strain data should be extracted into extractedStrains."""
        canadata_instance.process_menu_json(sample_menu_json)

        assert "blue-dream" in canadata_instance.extractedStrains
        assert canadata_instance.extractedStrains["blue-dream"]["genetics"] == "hybrid"
        assert "og-kush" in canadata_instance.extractedStrains

    def test_empty_categories(self, canadata_instance):
        """Locations with no categories should land in emptyMenus."""
        menu_json = {
            "listing": {"id": 999, "slug": "empty-shop", "wmid": 111},
            "categories": [],
        }
        canadata_instance.process_menu_json(menu_json)

        assert 999 in canadata_instance.emptyMenus
        assert canadata_instance.allMenuItems[999] == []

    def test_total_locations_tracking(self, canadata_instance, sample_menu_json):
        """Each processed menu should append to totalLocations."""
        canadata_instance.process_menu_json(sample_menu_json)
        assert len(canadata_instance.totalLocations) == 1
        assert canadata_instance.totalLocations[0]["slug"] == "test-dispensary"


# ---------------------------------------------------------------------------
# organize_into_clean_list tests
# ---------------------------------------------------------------------------

class TestOrganizeIntoCleanList:
    """Tests for the data flattening/export pipeline."""

    def test_original_organize(self, canadata_instance, sample_menu_json):
        """Original organizer should produce uniform dicts."""
        canadata_instance.process_menu_json(sample_menu_json)
        canadata_instance._original_organize_into_clean_list()

        assert len(canadata_instance.finishedMenuItems) == 3
        # All items should share the same set of keys
        key_sets = [set(item.keys()) for item in canadata_instance.finishedMenuItems]
        assert all(ks == key_sets[0] for ks in key_sets)

    def test_optimized_organize(self, canadata_optimized, sample_menu_json):
        """Optimized organizer should also produce results."""
        canadata_optimized.process_menu_json(sample_menu_json)
        canadata_optimized.organize_into_clean_list()

        assert len(canadata_optimized.finishedMenuItems) == 3


# ---------------------------------------------------------------------------
# do_request tests
# ---------------------------------------------------------------------------

class TestDoRequest:
    """Tests for the HTTP request wrapper."""

    @patch("CanaData.requests")
    def test_success(self, mock_requests, canadata_instance):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"data": "ok"}
        mock_requests.get.return_value = mock_resp

        result = canadata_instance.do_request("http://example.com")
        assert result == {"data": "ok"}

    @patch("CanaData.requests")
    def test_422_returns_break(self, mock_requests, canadata_instance):
        mock_resp = Mock()
        mock_resp.status_code = 422
        mock_resp.text = "Validation failed"
        mock_resp.json.return_value = {"errors": [{"detail": "bad param"}]}
        mock_requests.get.return_value = mock_resp

        result = canadata_instance.do_request("http://example.com")
        assert result == "break"

    @patch("CanaData.requests")
    def test_406_returns_false(self, mock_requests, canadata_instance):
        mock_resp = Mock()
        mock_resp.status_code = 406
        mock_resp.text = "Not Acceptable"
        mock_requests.get.return_value = mock_resp

        result = canadata_instance.do_request("http://example.com")
        assert result is False

    @patch("CanaData.requests")
    def test_500_returns_false(self, mock_requests, canadata_instance):
        mock_resp = Mock()
        mock_resp.status_code = 500
        mock_resp.text = "Internal Server Error"
        mock_requests.get.return_value = mock_resp

        result = canadata_instance.do_request("http://example.com")
        assert result is False

    @patch("CanaData.requests")
    def test_network_error_returns_false(self, mock_requests, canadata_instance):
        import requests as real_requests
        mock_requests.get.side_effect = real_requests.exceptions.ConnectionError("timeout")
        mock_requests.exceptions = real_requests.exceptions

        result = canadata_instance.do_request("http://example.com")
        assert result is False


# ---------------------------------------------------------------------------
# CacheManager tests
# ---------------------------------------------------------------------------

class TestCacheManager:
    """Tests for the multi-tier caching system."""

    def test_memory_cache_set_and_get(self, cache_manager):
        cache_manager.set("http://api.test/data", {"value": 42})
        result = cache_manager.get("http://api.test/data")
        assert result == {"value": 42}
        assert cache_manager.stats["memory_hits"] == 1

    def test_memory_cache_miss(self, cache_manager):
        result = cache_manager.get("http://api.test/missing")
        assert result is None
        assert cache_manager.stats["memory_misses"] == 1

    def test_disk_cache_persistence(self, temp_cache_dir):
        """Data cached to disk should survive a new CacheManager instance."""
        cm1 = CacheManager(cache_dir=temp_cache_dir)
        cm1.set("http://api.test/persist", {"persisted": True})

        cm2 = CacheManager(cache_dir=temp_cache_dir)
        result = cm2.get("http://api.test/persist")
        assert result == {"persisted": True}
        assert cm2.stats["disk_hits"] == 1

    def test_memory_cache_expiration(self):
        cm = CacheManager(
            cache_dir="/tmp/canadata_test_expire",
            memory_cache_ttl=1,
            enable_disk_cache=False,
        )
        cm.set("http://api.test/expire", {"temp": True})
        assert cm.get("http://api.test/expire") == {"temp": True}

        time.sleep(1.1)
        assert cm.get("http://api.test/expire") is None

    def test_invalidate_all(self, cache_manager):
        cache_manager.set("http://a", {"a": 1})
        cache_manager.set("http://b", {"b": 2})
        cache_manager.invalidate()

        assert cache_manager.get("http://a") is None
        assert cache_manager.get("http://b") is None

    def test_cache_with_params(self, cache_manager):
        """Different params should produce different cache keys."""
        cache_manager.set("http://api.test", {"page": 1}, params={"page": "1"})
        cache_manager.set("http://api.test", {"page": 2}, params={"page": "2"})

        assert cache_manager.get("http://api.test", params={"page": "1"}) == {"page": 1}
        assert cache_manager.get("http://api.test", params={"page": "2"}) == {"page": 2}

    def test_get_stats(self, cache_manager):
        cache_manager.set("http://test", {"x": 1})
        cache_manager.get("http://test")
        cache_manager.get("http://miss")

        stats = cache_manager.get_stats()
        assert stats["memory_hits"] == 1
        assert "hit_rate_percent" in stats
        assert "memory_cache_size" in stats


# ---------------------------------------------------------------------------
# ConcurrentMenuProcessor tests
# ---------------------------------------------------------------------------

class TestConcurrentMenuProcessor:
    """Tests for the thread-pool based concurrent processor."""

    def test_processes_all_locations(self, concurrent_processor):
        locations = [{"slug": f"loc-{i}", "type": "dispensary"} for i in range(5)]

        def process_fn(loc):
            return {"items": [f"item-{loc['slug']}"]}

        results = concurrent_processor.process_locations(locations, process_fn)
        assert len(results) == 5
        for loc in locations:
            assert loc["slug"] in results
            assert "items" in results[loc["slug"]]

    def test_error_handling(self, concurrent_processor):
        locations = [
            {"slug": "good", "type": "dispensary"},
            {"slug": "bad", "type": "dispensary"},
        ]

        def process_fn(loc):
            if loc["slug"] == "bad":
                raise ValueError("simulated failure")
            return {"ok": True}

        results = concurrent_processor.process_locations(locations, process_fn)
        assert "good" in results
        assert "bad" not in results
        assert len(concurrent_processor.errors) == 1
        assert "simulated failure" in concurrent_processor.errors[0]["error"]

    def test_results_reset_between_runs(self, concurrent_processor):
        """Each call to process_locations should start fresh."""
        locs1 = [{"slug": "a", "type": "dispensary"}]
        locs2 = [{"slug": "b", "type": "dispensary"}]

        concurrent_processor.process_locations(locs1, lambda l: "r1")
        concurrent_processor.process_locations(locs2, lambda l: "r2")

        assert "a" not in concurrent_processor.results
        assert "b" in concurrent_processor.results


class TestRetryWithBackoff:
    """Tests for the retry decorator."""

    def test_retries_on_failure(self):
        call_count = 0

        @retry_with_backoff(max_retries=3, base_delay=0.01)
        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError("not yet")
            return "success"

        assert flaky() == "success"
        assert call_count == 3

    def test_raises_after_max_retries(self):
        @retry_with_backoff(max_retries=2, base_delay=0.01)
        def always_fails():
            raise RuntimeError("permanent")

        with pytest.raises(RuntimeError, match="permanent"):
            always_fails()


# ---------------------------------------------------------------------------
# OptimizedDataProcessor tests
# ---------------------------------------------------------------------------

class TestOptimizedDataProcessor:
    """Tests for the pandas-based data processing pipeline."""

    def test_basic_processing(self, optimized_processor, sample_menu_items_dict):
        result = optimized_processor.process_menu_data(sample_menu_items_dict)
        assert len(result) == 3
        names = {item.get("name") for item in result}
        assert names == {"Product A", "Product B", "Product C"}

    def test_empty_input(self, optimized_processor):
        result = optimized_processor.process_menu_data({})
        assert result == []

    def test_single_location_empty_items(self, optimized_processor):
        result = optimized_processor.process_menu_data({"loc": []})
        assert result == []

    def test_nested_price_flattened(self, optimized_processor):
        data = {
            "loc1": [{"name": "Item", "price": {"amount": 10, "currency": "USD"}}]
        }
        result = optimized_processor.process_menu_data(data)
        assert len(result) == 1
        item = result[0]
        assert item.get("price.amount") == 10 or item.get("price.amount") == "10"
        assert item.get("price.currency") == "USD"

    def test_handles_none_values(self, optimized_processor):
        data = {"loc1": [{"name": "Nullable", "description": None}]}
        result = optimized_processor.process_menu_data(data)
        assert len(result) == 1

    def test_handles_list_values(self, optimized_processor):
        data = {"loc1": [{"name": "Tagged", "tags": ["a", "b", "c"]}]}
        result = optimized_processor.process_menu_data(data)
        assert len(result) == 1
        # tags should be serialized somehow (string or JSON)
        assert "tags" in result[0] or any("tags" in k for k in result[0])

    def test_fallback_flattening(self, optimized_processor):
        """_fallback_flattening should work as an alternative path."""
        items = [
            {"name": "A", "nested": {"x": 1}},
            {"name": "B", "nested": {"x": 2}},
        ]
        df = optimized_processor._fallback_flattening(items)
        assert len(df) == 2

    def test_normalize_data_fills_none(self, optimized_processor):
        """_normalize_data should fill NaN with 'None'."""
        import pandas as pd
        df = pd.DataFrame([{"a": 1, "b": None}, {"a": 2, "c": "x"}])
        result = optimized_processor._normalize_data(df)
        assert "None" in result.values.flatten().tolist()
