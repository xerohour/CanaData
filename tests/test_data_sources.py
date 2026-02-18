"""
Tests for the data_sources pluggable framework.

Covers:
  - DataSourceBase ABC contract
  - DataSourceManager registration, dispatch, and introspection
  - CannMenusAdapter and LeaflyAdapter wiring (mocked)
"""

import pytest
from unittest.mock import patch, MagicMock
from data_sources.base import DataSourceBase, DataSourceType
from data_sources.manager import DataSourceManager


# ---------------------------------------------------------------------------
# Concrete stub used across multiple tests
# ---------------------------------------------------------------------------
class StubAPISource(DataSourceBase):
    name = "stub_api"
    source_type = DataSourceType.API

    def get_locations(self, slug):
        return [
            {"id": "loc1", "name": "Store A"},
            {"id": "loc2", "name": "Store B"},
        ]

    def get_menu(self, location_id):
        return [
            {"product": f"Item from {location_id}", "price": 9.99},
        ]


class StubScraperSource(DataSourceBase):
    name = "stub_scraper"
    source_type = DataSourceType.SCRAPER

    def get_locations(self, slug):
        return [{"id": f"scrape_{slug}", "name": f"Scraper: {slug}"}]

    def get_menu(self, location_id):
        return [{"product": "Scraped item", "thc": "22%"}]


class UnavailableSource(DataSourceBase):
    name = "unavailable"
    source_type = DataSourceType.API

    def is_available(self):
        return False

    def get_locations(self, slug):
        return []

    def get_menu(self, location_id):
        return []


# ---------------------------------------------------------------------------
# DataSourceBase tests
# ---------------------------------------------------------------------------
class TestDataSourceBase:
    def test_cannot_instantiate_abc_directly(self):
        """DataSourceBase should not be instantiable on its own."""
        with pytest.raises(TypeError):
            DataSourceBase()

    def test_stub_implements_interface(self):
        src = StubAPISource()
        assert src.name == "stub_api"
        assert src.source_type == DataSourceType.API
        assert src.is_available() is True

    def test_get_locations_returns_list(self):
        src = StubAPISource()
        locs = src.get_locations("ny")
        assert isinstance(locs, list)
        assert len(locs) == 2
        assert locs[0]["id"] == "loc1"

    def test_get_menu_returns_list(self):
        src = StubAPISource()
        items = src.get_menu("loc1")
        assert isinstance(items, list)
        assert items[0]["product"] == "Item from loc1"

    def test_fetch_all_aggregates_correctly(self):
        src = StubAPISource()
        result = src.fetch_all("ca")
        assert result["source"] == "stub_api"
        assert len(result["locations"]) == 2
        assert "loc1" in result["menus"]
        assert "loc2" in result["menus"]
        assert result["total_items"] == 2  # 1 item per location

    def test_repr(self):
        src = StubScraperSource()
        assert "stub_scraper" in repr(src)
        assert "scraper" in repr(src)


# ---------------------------------------------------------------------------
# DataSourceManager tests
# ---------------------------------------------------------------------------
class TestDataSourceManager:
    def test_register_and_get(self):
        mgr = DataSourceManager()
        src = StubAPISource()
        mgr.register(src)
        assert mgr.get("stub_api") is src
        assert mgr.get("STUB_API") is src  # case-insensitive

    def test_register_rejects_non_base(self):
        mgr = DataSourceManager()
        with pytest.raises(TypeError):
            mgr.register("not a source")

    def test_register_rejects_duplicate(self):
        mgr = DataSourceManager()
        mgr.register(StubAPISource())
        with pytest.raises(ValueError, match="already registered"):
            mgr.register(StubAPISource())

    def test_unregister(self):
        mgr = DataSourceManager()
        mgr.register(StubAPISource())
        mgr.unregister("stub_api")
        assert mgr.get("stub_api") is None

    def test_contains(self):
        mgr = DataSourceManager()
        mgr.register(StubAPISource())
        assert "stub_api" in mgr
        assert "nonexistent" not in mgr

    def test_len(self):
        mgr = DataSourceManager()
        assert len(mgr) == 0
        mgr.register(StubAPISource())
        assert len(mgr) == 1

    def test_list_sources(self):
        mgr = DataSourceManager()
        mgr.register(StubAPISource())
        mgr.register(StubScraperSource())
        info = mgr.list_sources()
        names = {s["name"] for s in info}
        assert names == {"stub_api", "stub_scraper"}

    def test_fetch_dispatches_correctly(self):
        mgr = DataSourceManager()
        mgr.register(StubAPISource())
        result = mgr.fetch("stub_api", "ny")
        assert result["source"] == "stub_api"
        assert result["total_items"] == 2

    def test_fetch_raises_on_unknown_source(self):
        mgr = DataSourceManager()
        with pytest.raises(KeyError, match="not registered"):
            mgr.fetch("unknown", "ny")

    def test_fetch_locations_only(self):
        mgr = DataSourceManager()
        mgr.register(StubAPISource())
        locs = mgr.fetch_locations("stub_api", "ny")
        assert len(locs) == 2

    def test_fetch_menu_only(self):
        mgr = DataSourceManager()
        mgr.register(StubAPISource())
        items = mgr.fetch_menu("stub_api", "loc1")
        assert len(items) == 1


# ---------------------------------------------------------------------------
# Adapter wiring tests (mocked to avoid real HTTP / Apify calls)
# ---------------------------------------------------------------------------
class TestCannMenusAdapter:
    @patch("data_sources.cannmenus_adapter.CannMenusClient")
    @patch.dict("os.environ", {"CANNMENUS_API_TOKEN": "test-token"})
    def test_get_locations(self, MockClient):
        mock_instance = MockClient.return_value
        mock_instance.get_retailers.return_value = [
            {"id": "r1", "name": "Shop 1"},
        ]

        from data_sources.cannmenus_adapter import CannMenusAdapter
        adapter = CannMenusAdapter()
        locs = adapter.get_locations("ny")
        assert len(locs) == 1
        mock_instance.get_retailers.assert_called_once_with("NY")

    @patch("data_sources.cannmenus_adapter.CannMenusClient")
    @patch.dict("os.environ", {"CANNMENUS_API_TOKEN": "test-token"})
    def test_get_menu(self, MockClient):
        mock_instance = MockClient.return_value
        mock_instance.get_menu.return_value = [{"product": "Flower"}]

        from data_sources.cannmenus_adapter import CannMenusAdapter
        adapter = CannMenusAdapter()
        items = adapter.get_menu("r1")
        assert len(items) == 1
        mock_instance.get_menu.assert_called_once_with("r1")

    @patch.dict("os.environ", {"CANNMENUS_API_TOKEN": ""})
    def test_is_available_false_when_no_token(self):
        from data_sources.cannmenus_adapter import CannMenusAdapter
        adapter = CannMenusAdapter()
        assert adapter.is_available() is False

    @patch.dict("os.environ", {"CANNMENUS_API_TOKEN": "real-token"})
    def test_is_available_true_when_token_set(self):
        from data_sources.cannmenus_adapter import CannMenusAdapter
        adapter = CannMenusAdapter()
        assert adapter.is_available() is True


class TestLeaflyAdapter:
    @patch("data_sources.leafly_adapter.scrape_leafly")
    @patch.dict("os.environ", {"APIFY_TOKEN": "test-token"})
    def test_get_locations_returns_synthetic(self, mock_scrape):
        from data_sources.leafly_adapter import LeaflyAdapter
        adapter = LeaflyAdapter()
        locs = adapter.get_locations("los-angeles")
        assert len(locs) == 1
        assert locs[0]["id"] == "leafly_los-angeles"

    @patch("data_sources.leafly_adapter.scrape_leafly")
    @patch.dict("os.environ", {"APIFY_TOKEN": "test-token"})
    def test_get_menu_calls_scrape_leafly(self, mock_scrape):
        mock_scrape.return_value = [{"name": "Product A"}]

        from data_sources.leafly_adapter import LeaflyAdapter
        adapter = LeaflyAdapter()
        items = adapter.get_menu("leafly_los-angeles")
        assert len(items) == 1
        mock_scrape.assert_called_once_with("los-angeles")

    @patch.dict("os.environ", {"APIFY_TOKEN": ""})
    def test_is_available_false_when_no_token(self):
        from data_sources.leafly_adapter import LeaflyAdapter
        adapter = LeaflyAdapter()
        assert adapter.is_available() is False


# ---------------------------------------------------------------------------
# CanaData.getSourceData integration test (mocked manager)
# ---------------------------------------------------------------------------
class TestCanaDataSourceIntegration:
    @patch("CanaData.DataSourceManager")
    def test_get_source_data_populates_internal_structures(self, MockMgr):
        mock_mgr_instance = MockMgr.return_value
        mock_mgr_instance.__contains__ = MagicMock(return_value=True)
        mock_mgr_instance.fetch.return_value = {
            "source": "stub",
            "locations": [{"id": "s1", "name": "Store"}],
            "menus": {"s1": [{"product": "A"}, {"product": "B"}]},
            "total_items": 2,
        }
        mock_mgr_instance.list_sources.return_value = [{"name": "stub"}]

        from CanaData import CanaData
        cana = CanaData()
        cana.source_manager = mock_mgr_instance
        cana.searchSlug = "ny"

        cana.getSourceData("stub")

        assert "s1" in cana.allMenuItems
        assert len(cana.allMenuItems["s1"]) == 2
        assert cana.menuItemsFound == 2
        assert len(cana.totalLocations) == 1
