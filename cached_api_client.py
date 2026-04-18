import requests
import time
import logging
from typing import Dict, Any, Optional
from cache_manager import CacheManager

logger = logging.getLogger(__name__)


class CachedAPIClient:
    """Enhanced API client with caching capabilities"""

    def __init__(self, cache_manager: CacheManager):
        self.cache_manager = cache_manager
        self.session = requests.Session()

    def get(
            self,
            url: str,
            params: Optional[Dict] = None,
            use_cache: bool = True,
            force_refresh: bool = False,
            **kwargs) -> Any:
        """Make GET request with caching support"""

        # Check cache first (unless force refresh)
        if use_cache and not force_refresh:
            cached_data = self.cache_manager.get(url, params)
            if cached_data is not None:
                return cached_data

        # Make API request
        logger.debug(f"Making API request to {url}")
        self.cache_manager.stats['api_requests'] += 1

        try:
            response = self.session.get(url, params=params, **kwargs)
            response.raise_for_status()
            data = response.json()

            # Cache the response
            if use_cache:
                self.cache_manager.set(url, data, params)

            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {url}: {e}")
            raise

    def get_with_retry(
            self,
            url: str,
            params: Optional[Dict] = None,
            max_retries: int = 3,
            **kwargs) -> Any:
        """Make GET request with retry logic and caching"""
        for attempt in range(max_retries):
            try:
                return self.get(url, params, **kwargs)
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise

                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(
                    f"Request failed (attempt {
                        attempt +
                        1}), retrying in {wait_time}s: {e}")
                time.sleep(wait_time)
