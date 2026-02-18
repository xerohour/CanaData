"""
Leafly adapter -- wraps the existing LeaflyScraper behind DataSourceBase.

This is a scraper-based data source.  It requires the APIFY_TOKEN
environment variable and the ``apify-client`` package.
"""

import os
import logging
from typing import Any, Dict, List

from data_sources.base import DataSourceBase, DataSourceType
from LeaflyScraper import scrape_leafly

logger = logging.getLogger(__name__)


class LeaflyAdapter(DataSourceBase):
    """Adapter that exposes Leafly scraping through the DataSourceBase interface.

    Leafly works differently from a typical API: the scraper returns a flat
    list of items for a location slug rather than distinct locations + menus.
    We model this as a single virtual location whose menu is the full result set.
    """

    name = "leafly"
    source_type = DataSourceType.SCRAPER

    def is_available(self) -> bool:
        """Available when APIFY_TOKEN is set."""
        token = os.getenv("APIFY_TOKEN", "")
        return bool(token) and token != "your_apify_token_here"

    def get_locations(self, slug: str) -> List[Dict[str, Any]]:
        """Return a single virtual location representing the Leafly search.

        Leafly does not expose a separate location listing endpoint --
        the scraper returns products directly.  We wrap the slug as a
        synthetic location so that ``fetch_all`` can call ``get_menu``
        on it uniformly.

        Args:
            slug: City or region slug (e.g. "los-angeles").

        Returns:
            A single-element list with a virtual location dict.
        """
        return [{"id": f"leafly_{slug}", "name": f"Leafly: {slug}"}]

    def get_menu(self, location_id: str) -> List[Dict[str, Any]]:
        """Scrape Leafly products for the slug embedded in *location_id*.

        Args:
            location_id: Synthetic id created by ``get_locations``
                         (format: ``leafly_<slug>``).

        Returns:
            List of product dicts from the Leafly scraper.
        """
        # Extract the original slug from the synthetic id
        slug = location_id.replace("leafly_", "", 1)
        self._logger.info("Scraping Leafly for slug=%s", slug)
        items = scrape_leafly(slug)
        self._logger.info("Scraped %d items from Leafly", len(items))
        return items
