"""
Base interface for all CanaData data source modules.

Every new data source -- whether a direct API client or a web scraper --
should subclass `DataSourceBase` and implement the required methods.
CanaData will interact with each source exclusively through this interface.
"""

import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class DataSourceType(Enum):
    """Categorises how a data source fetches its data."""
    API = "api"          # Direct API access (like CannMenus)
    SCRAPER = "scraper"  # Web scraping / third-party actor (like Leafly)


class DataSourceBase(ABC):
    """
    Abstract base class that every data source adapter must implement.

    Subclasses provide two things:
      1. A way to list locations / retailers for a given search term.
      2. A way to fetch menu items for a specific location.

    The return format is always a list of plain dictionaries so that
    CanaData's existing flatten / CSV pipeline can consume them directly.

    Attributes:
        name (str):  Human-readable source name (e.g. "CannMenus").
        source_type (DataSourceType):  API or SCRAPER.
    """

    # -- class-level metadata (override in subclasses) --------------------
    name: str = "base"
    source_type: DataSourceType = DataSourceType.API

    # -- lifecycle --------------------------------------------------------
    def __init__(self) -> None:
        self._logger = logging.getLogger(f"data_sources.{self.name}")

    def is_available(self) -> bool:
        """Return True if this source has the credentials / deps it needs.

        The default implementation always returns True.  Override to check
        for env vars, API tokens, installed packages, etc.
        """
        return True

    # -- abstract contract ------------------------------------------------
    @abstractmethod
    def get_locations(self, slug: str) -> List[Dict[str, Any]]:
        """Retrieve a list of dispensary / retailer locations.

        Args:
            slug: A search identifier -- could be a state code ("NY"),
                  a city slug ("los-angeles"), or any source-specific key.

        Returns:
            A list of dicts.  Each dict must contain at least:
                - ``id``   (str): unique identifier for the location
                - ``name`` (str): human-readable name
            Additional keys are source-specific and will be preserved.
        """
        ...

    @abstractmethod
    def get_menu(self, location_id: str) -> List[Dict[str, Any]]:
        """Retrieve menu / product items for a single location.

        Args:
            location_id: The identifier returned by ``get_locations()``.

        Returns:
            A list of dicts, each representing one menu item.
            The dicts should be as flat as possible; nested structures
            are acceptable (CanaData will flatten them).
        """
        ...

    # -- convenience helpers ---------------------------------------------
    def fetch_all(self, slug: str) -> Dict[str, Any]:
        """High-level helper: fetch locations then menus for each one.

        Returns a dict structured like::

            {
                "source": "<source name>",
                "locations": [ ... ],
                "menus": { "<location_id>": [ ...items... ], ... },
                "total_items": <int>
            }
        """
        self._logger.info("fetch_all starting for slug=%s", slug)
        locations = self.get_locations(slug)
        self._logger.info("Found %d locations", len(locations))

        menus: Dict[str, List[Dict[str, Any]]] = {}
        total_items = 0

        for loc in locations:
            loc_id = str(loc.get("id", ""))
            loc_name = loc.get("name", loc_id)
            if not loc_id:
                self._logger.warning("Skipping location with no id: %s", loc)
                continue

            self._logger.info("Fetching menu for %s (%s)", loc_name, loc_id)
            items = self.get_menu(loc_id)
            menus[loc_id] = items
            total_items += len(items)

        result = {
            "source": self.name,
            "locations": locations,
            "menus": menus,
            "total_items": total_items,
        }
        self._logger.info(
            "fetch_all complete: %d locations, %d items", len(locations), total_items
        )
        return result

    def __repr__(self) -> str:
        return f"<DataSource:{self.name} type={self.source_type.value}>"
