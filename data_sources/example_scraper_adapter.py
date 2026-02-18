"""
Example Scraper Adapter Template
=================================

Copy this file and rename it to create a new web-scraping data source.
Replace all TODO markers with your implementation.

Steps to integrate a new scraper source:

  1. Copy this file:  ``cp example_scraper_adapter.py myscraper_adapter.py``
  2. Implement ``is_available``, ``get_locations``, and ``get_menu``.
  3. Register it in ``manager.py`` inside ``auto_register()``::

        try:
            from data_sources.myscraper_adapter import MyScraperAdapter
            adapters.append(MyScraperAdapter)
        except ImportError as exc:
            logger.warning("Could not import MyScraperAdapter: %s", exc)

  4. (Optional) Add a CLI flag in CanaData.py's ``__main__`` block.
  5. Add relevant env vars to ``.env.example``.

Note:
  Scrapers often don't have a clean "locations then menus" split.
  If your scraper returns everything in one shot, model it as a
  single synthetic location (see LeaflyAdapter for the pattern).
"""

import os
import logging
from typing import Any, Dict, List

from data_sources.base import DataSourceBase, DataSourceType

logger = logging.getLogger(__name__)


class ExampleScraperAdapter(DataSourceBase):
    """Template for a new web-scraper data source adapter.

    TODO: rename this class and update ``name`` / ``source_type``.
    """

    name = "example_scraper"               # TODO: unique lowercase name
    source_type = DataSourceType.SCRAPER

    def __init__(self) -> None:
        super().__init__()
        # TODO: read any credentials or config from env
        self._scraper_token = os.getenv("EXAMPLE_SCRAPER_TOKEN", "")

    def is_available(self) -> bool:
        """Check whether the required credentials / packages are present."""
        # TODO: also check for any required pip packages
        return bool(self._scraper_token) and self._scraper_token != "your_token_here"

    def get_locations(self, slug: str) -> List[Dict[str, Any]]:
        """Return a synthetic location wrapping the scrape target.

        Many scrapers don't separate "list locations" from "get menu".
        If that's the case, return a single virtual location and do all
        the heavy lifting in ``get_menu``.

        Args:
            slug: Search identifier (city slug, URL path, etc.).

        Returns:
            List with one synthetic location dict.
        """
        # TODO: if the scraper supports listing stores, do it here.
        # Otherwise return a single virtual location:
        return [{"id": f"example_{slug}", "name": f"ExampleScraper: {slug}"}]

    def get_menu(self, location_id: str) -> List[Dict[str, Any]]:
        """Run the scraper and return product / menu data.

        Args:
            location_id: Synthetic or real location id.

        Returns:
            List of product dicts.
        """
        slug = location_id.replace("example_", "", 1)
        self._logger.info("Scraping example source for slug=%s", slug)

        # TODO: implement real scraping logic here
        # Example pattern using an Apify actor:
        #
        #   from apify_client import ApifyClient
        #   client = ApifyClient(self._scraper_token)
        #   run_input = {"location": slug, "maxStores": 50}
        #   run = client.actor("your/actor-name").call(run_input=run_input)
        #   results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        #   return results
        #
        # Or using requests + BeautifulSoup:
        #
        #   import requests
        #   from bs4 import BeautifulSoup
        #   resp = requests.get(f"https://example.com/{slug}")
        #   soup = BeautifulSoup(resp.text, "html.parser")
        #   ...parse and return items...

        self._logger.warning("ExampleScraperAdapter.get_menu is a stub -- returning empty list")
        return []
