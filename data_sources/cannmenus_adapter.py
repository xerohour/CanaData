"""
CannMenus adapter -- wraps the existing CannMenusClient behind DataSourceBase.

This is a direct-API data source.  It requires the CANNMENUS_API_TOKEN
environment variable to be set.
"""

import os
import logging
from typing import Any, Dict, List

from data_sources.base import DataSourceBase, DataSourceType
from CannMenusClient import CannMenusClient

logger = logging.getLogger(__name__)


class CannMenusAdapter(DataSourceBase):
    """Adapter that exposes CannMenusClient through the DataSourceBase interface."""

    name = "cannmenus"
    source_type = DataSourceType.API

    def __init__(self) -> None:
        super().__init__()
        self._client = CannMenusClient()

    def is_available(self) -> bool:
        """Available when CANNMENUS_API_TOKEN is set."""
        token = os.getenv("CANNMENUS_API_TOKEN", "")
        return bool(token) and token != "your_cannmenus_token_here"

    def get_locations(self, slug: str) -> List[Dict[str, Any]]:
        """Fetch retailers for a two-letter state code.

        Args:
            slug: Two-letter state code (e.g. "NY", "CA").

        Returns:
            List of retailer dicts from CannMenus.
        """
        state_code = slug.upper().strip()
        self._logger.info("Fetching CannMenus retailers for state=%s", state_code)
        retailers = self._client.get_retailers(state_code)
        self._logger.info("Found %d retailers", len(retailers))
        return retailers

    def get_menu(self, location_id: str) -> List[Dict[str, Any]]:
        """Fetch normalized menu items for a single retailer.

        Args:
            location_id: CannMenus retailer ID.

        Returns:
            List of menu item dicts.
        """
        self._logger.info("Fetching CannMenus menu for retailer=%s", location_id)
        items = self._client.get_menu(location_id)
        self._logger.info("Got %d menu items", len(items))
        return items
