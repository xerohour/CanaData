"""
Integration tests for complete CanaData workflows.

These tests mock external HTTP calls with the ``responses`` library and
verify that the end-to-end pipelines (Weedmaps, CannMenus) work correctly.
"""

import pytest
import responses
from unittest.mock import patch, Mock


# ---------------------------------------------------------------------------
# Weedmaps workflow
# ---------------------------------------------------------------------------

class TestWeedmapsWorkflow:
    """Integration tests for the Weedmaps scraping pipeline."""

    @responses.activate
    def test_locations_retrieval(self, canadata_instance):
        """getLocations should paginate and collect all locations."""
        canadata_instance.setCitySlug("test-city")
        canadata_instance.deliveries = False

        url_pattern = "https://api-g.weedmaps.com/discovery/v1/listings"
        resp_body = {
            "meta": {"total_listings": 2},
            "data": {
                "listings": [
                    {"slug": "shop-a", "type": "dispensary"},
                    {"slug": "shop-b", "type": "dispensary"},
                ]
            },
        }
        responses.add(responses.GET, url_pattern, json=resp_body, status=200)

        canadata_instance.getLocations()

        assert len(canadata_instance.locations) == 2
        assert canadata_instance.locationsFound == 2
        assert canadata_instance.maxLocations == 2

    @responses.activate
    def test_locations_zero_results(self, canadata_instance):
        """Zero-result slug should set NonGreenState."""
        canadata_instance.setCitySlug("empty-state")
        canadata_instance.deliveries = False

        url_pattern = "https://api-g.weedmaps.com/discovery/v1/listings"
        responses.add(
            responses.GET,
            url_pattern,
            json={"meta": {"total_listings": 0}, "data": {"listings": []}},
            status=200,
        )

        canadata_instance.getLocations()

        assert canadata_instance.NonGreenState is True
        assert "empty-state" in canadata_instance.unFriendlyStates

    @responses.activate
    def test_full_menu_pipeline(self, canadata_instance):
        """End-to-end: locations -> menus -> organize."""
        canadata_instance.setCitySlug("pipeline-city")
        canadata_instance.deliveries = False

        # Mock locations endpoint
        loc_url = "https://api-g.weedmaps.com/discovery/v1/listings"
        responses.add(
            responses.GET,
            loc_url,
            json={
                "meta": {"total_listings": 1},
                "data": {"listings": [{"slug": "test-shop", "type": "dispensary"}]},
            },
            status=200,
        )

        # Mock menu endpoint
        menu_url = "https://weedmaps.com/api/web/v1/listings/test-shop/menu"
        responses.add(
            responses.GET,
            menu_url,
            json={
                "listing": {"id": 1, "slug": "test-shop", "wmid": 100},
                "categories": [
                    {
                        "title": "Flower",
                        "items": [
                            {"name": "Strain X", "price": {"amount": 30}},
                        ],
                    }
                ],
            },
            status=200,
        )

        canadata_instance.getLocations()
        assert len(canadata_instance.locations) == 1

        # Use sequential menu fetching (no concurrent env var set)
        with patch("builtins.input", return_value="skip"):
            canadata_instance._getMenusSequential()

        assert canadata_instance.menuItemsFound == 1
        assert len(canadata_instance.finishedMenuItems) == 1

    @responses.activate
    def test_menu_503_skipped(self, canadata_instance):
        """503 responses should be skipped gracefully."""
        canadata_instance.locations = [{"slug": "unavailable-shop", "type": "dispensary"}]

        menu_url = "https://weedmaps.com/api/web/v1/listings/unavailable-shop/menu"
        responses.add(responses.GET, menu_url, status=503)

        with patch("builtins.input", return_value="skip"):
            canadata_instance._getMenusSequential()

        # No items should be recorded, and no crash
        assert canadata_instance.menuItemsFound == 0


# ---------------------------------------------------------------------------
# Brands / Strains
# ---------------------------------------------------------------------------

class TestBrandsAndStrains:
    """Integration tests for brand and strain retrieval."""

    @responses.activate
    def test_get_brands(self, canadata_instance):
        url = "https://api-g.weedmaps.com/discovery/v1/brands"
        responses.add(
            responses.GET,
            url,
            json={
                "meta": {"total_brands": 1},
                "data": {"brands": [{"id": 1, "name": "Test Brand", "slug": "test-brand"}]},
            },
            status=200,
        )

        canadata_instance.getBrands()
        assert len(canadata_instance.brands) == 1
        assert canadata_instance.brandsFound == 1

    @responses.activate
    def test_get_strains(self, canadata_instance):
        url = "https://api-g.weedmaps.com/discovery/v1/strains"
        responses.add(
            responses.GET,
            url,
            json={
                "meta": {"total_strains": 1},
                "data": {"strains": [{"id": 10, "name": "Sour Diesel", "slug": "sour-diesel"}]},
            },
            status=200,
        )

        canadata_instance.getStrains()
        assert len(canadata_instance.strains) == 1
        assert canadata_instance.strainsFound == 1


# ---------------------------------------------------------------------------
# CannMenus integration
# ---------------------------------------------------------------------------

class TestCannMenusIntegration:
    """Integration tests for CannMenus data retrieval."""

    @responses.activate
    def test_get_retailers(self, monkeypatch):
        monkeypatch.setenv("CANNMENUS_API_TOKEN", "dummy-token")
        from CannMenusClient import CannMenusClient

        client = CannMenusClient()
        url = "https://api.cannmenus.com/v1/retailers"
        responses.add(
            responses.GET,
            url,
            json={"data": [{"id": "r1", "name": "Shop One"}]},
            status=200,
        )

        retailers = client.get_retailers("NY")
        assert len(retailers) == 1
        assert retailers[0]["name"] == "Shop One"

    @responses.activate
    def test_get_menu(self, monkeypatch):
        monkeypatch.setenv("CANNMENUS_API_TOKEN", "dummy-token")
        from CannMenusClient import CannMenusClient

        client = CannMenusClient()
        url = "https://api.cannmenus.com/v1/retailers/r1/menu"
        responses.add(
            responses.GET,
            url,
            json={"data": [{"name": "Edible", "price": 20}]},
            status=200,
        )

        menu = client.get_menu("r1")
        assert len(menu) == 1
        assert menu[0]["name"] == "Edible"

    def test_missing_token_returns_empty(self, monkeypatch):
        monkeypatch.delenv("CANNMENUS_API_TOKEN", raising=False)
        from CannMenusClient import CannMenusClient

        client = CannMenusClient()
        assert client.get_retailers("NY") == []


# ---------------------------------------------------------------------------
# CachedAPIClient integration
# ---------------------------------------------------------------------------

class TestCachedAPIClientIntegration:
    """Integration tests for the cached API client layer."""

    @responses.activate
    def test_caches_response(self, cache_manager):
        from cached_api_client import CachedAPIClient

        client = CachedAPIClient(cache_manager)
        url = "https://api.test/data"
        responses.add(responses.GET, url, json={"result": 1}, status=200)

        # First call hits the network
        result1 = client.get(url)
        assert result1 == {"result": 1}
        assert cache_manager.stats["api_requests"] == 1

        # Second call should come from cache (no new network request)
        result2 = client.get(url)
        assert result2 == {"result": 1}
        assert cache_manager.stats["api_requests"] == 1  # unchanged

    @responses.activate
    def test_force_refresh(self, cache_manager):
        from cached_api_client import CachedAPIClient

        client = CachedAPIClient(cache_manager)
        url = "https://api.test/refresh"
        responses.add(responses.GET, url, json={"v": 1}, status=200)
        responses.add(responses.GET, url, json={"v": 2}, status=200)

        client.get(url)
        result = client.get(url, force_refresh=True)
        assert result == {"v": 2}
        assert cache_manager.stats["api_requests"] == 2

    @responses.activate
    def test_retry_logic(self, cache_manager):
        from cached_api_client import CachedAPIClient
        import requests as req_lib

        client = CachedAPIClient(cache_manager)
        url = "https://api.test/flaky"

        # First two calls fail, third succeeds
        responses.add(responses.GET, url, body=req_lib.exceptions.ConnectionError("fail"))
        responses.add(responses.GET, url, body=req_lib.exceptions.ConnectionError("fail"))
        responses.add(responses.GET, url, json={"ok": True}, status=200)

        result = client.get_with_retry(url, max_retries=3, use_cache=False)
        assert result == {"ok": True}


# ---------------------------------------------------------------------------
# Concurrent menu fetching integration
# ---------------------------------------------------------------------------

class TestConcurrentMenuIntegration:
    """Integration test for the concurrent menu fetching path."""

    @responses.activate
    def test_concurrent_fetching(self, canadata_instance):
        """_getMenusConcurrent should fetch menus in parallel."""
        canadata_instance.locations = [
            {"slug": "shop-1", "type": "dispensary"},
            {"slug": "shop-2", "type": "dispensary"},
        ]

        for slug in ["shop-1", "shop-2"]:
            url = f"https://weedmaps.com/api/web/v1/listings/{slug}/menu"
            responses.add(
                responses.GET,
                url,
                json={
                    "listing": {"id": hash(slug) % 10000, "slug": slug, "wmid": 1},
                    "categories": [
                        {"title": "Flower", "items": [{"name": f"Item from {slug}"}]}
                    ],
                },
                status=200,
            )

        canadata_instance._getMenusConcurrent()

        assert canadata_instance.menuItemsFound == 2
        assert len(canadata_instance.finishedMenuItems) == 2
