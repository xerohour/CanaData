import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CanaConfig:
    """
    Configuration class for CanaData.
    """
    def __init__(self):
        self.weedmaps_base_url = os.getenv('WEEDMAPS_BASE_URL', 'https://api-g.weedmaps.com/discovery/v1/listings')
        self.brands_base_url = os.getenv('WEEDMAPS_BRANDS_URL', 'https://api-g.weedmaps.com/discovery/v1/brands')
        self.strains_base_url = os.getenv('WEEDMAPS_STRAINS_URL', 'https://api-g.weedmaps.com/discovery/v1/strains')

        self.page_size = os.getenv('PAGE_SIZE', '100')
        self.max_workers = int(os.getenv('MAX_WORKERS', '10'))
        self.rate_limit = float(os.getenv('RATE_LIMIT', '1.0'))

        self.cache_enabled = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
        self.cache_ttl = int(os.getenv('CACHE_TTL', '3600'))
        self.memory_cache_size = int(os.getenv('MEMORY_CACHE_SIZE', '2000'))
        self.enable_disk_cache = os.getenv('ENABLE_DISK_CACHE', 'true').lower() == 'true'

        self.optimize_processing = os.getenv('OPTIMIZE_PROCESSING', 'true').lower() == 'true'
        self.use_concurrent_processing = os.getenv('USE_CONCURRENT_PROCESSING', 'false').lower() == 'true'
        self.menu_page_size = int(os.getenv('MENU_PAGE_SIZE', '100'))

        self.log_level = os.getenv('LOG_LEVEL', 'INFO')

    @property
    def pagination_params(self) -> str:
        return f"&page_size={self.page_size}&size={self.page_size}"
