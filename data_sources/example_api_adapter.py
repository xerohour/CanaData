"""
Example API Adapter Template
=============================

Copy this file and rename it to create a new direct-API data source.
Replace all TODO markers with your implementation.

Steps to integrate a new API source:

  1. Copy this file:  ``cp example_api_adapter.py myapi_adapter.py``
  2. Implement ``is_available``, ``get_locations``, and ``get_menu``.
  3. Register it in ``manager.py`` inside ``auto_register()``::

        try:
            from data_sources.myapi_adapter import MyAPIAdapter
            adapters.append(MyAPIAdapter)
        except ImportError as exc:
            logger.warning("Could not import MyAPIAdapter: %s", exc)

  4. (Optional) Add a CLI flag in CanaData.py's ``__main__`` block.
  5. Add relevant env vars to ``.env.example``.
"""

import os
import logging
import requests
from typing import Any, Dict, List

from data_sources.base import DataSourceBase, DataSourceType

logger = logging.getLogger(__name__)


class ExampleAPIAdapter(DataSourceBase):
    """Template for a new direct-API data source adapter.

    TODO: rename this class and update ``name`` / ``source_type``.
    """

    name = "example_api"                   # TODO: unique lowercase name
    source_type = DataSourceType.API

    def __init__(self) -> None:
        super().__init__()
        # TODO: read credentials from env
        self._api_token = os.getenv("EXAMPLE_API_TOKEN", "")
        self._base_url = "https://api.example.com/v1"  # TODO: real base URL
        self._headers = {
            "Authorization": f"Bearer {self._api_token}",
            "Accept": "application/json",
        }

    def is_available(self) -> bool:
        """Check whether the required API token is configured."""
        return bool(self._api_token) and self._api_token != "your_token_here"

    def get_locations(self, slug: str) -> List[Dict[str, Any]]:
        """Fetch dispensary / retailer locations from the API.

        Args:
            slug: Search identifier (state code, city slug, etc.).

        Returns:
            List of location dicts, each with at least ``id`` and ``name``.
        """
        # TODO: implement real API call
        url = f"{self._base_url}/locations?region={slug}"
        try:
            resp = requests.get(url, headers=self._headers, timeout=30)
            resp.raise_for_status()
            data = resp.json().get("data", [])
            self._logger.info("Found %d locations for %s", len(data), slug)
            return data
        except Exception as exc:
            self._logger.error("Failed to fetch locations: %s", exc)
            return []

    def get_menu(self, location_id: str) -> List[Dict[str, Any]]:
        """Fetch menu items for a single location.

        Args:
            location_id: The location identifier from ``get_locations()``.

        Returns:
            List of menu item dicts.
        """
        # TODO: implement real API call
        url = f"{self._base_url}/locations/{location_id}/menu"
        try:
            resp = requests.get(url, headers=self._headers, timeout=30)
            resp.raise_for_status()
            items = resp.json().get("data", [])
            self._logger.info("Got %d items for location %s", len(items), location_id)
            return items
        except Exception as exc:
            self._logger.error("Failed to fetch menu: %s", exc)
            return []
