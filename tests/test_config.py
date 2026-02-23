import os
from unittest.mock import patch
from config import CanaConfig

def test_config_defaults():
    """Test that CanaConfig loads default values correctly."""
    with patch.dict(os.environ, {}, clear=True):
        config = CanaConfig()
        assert config.weedmaps_base_url == 'https://api-g.weedmaps.com/discovery/v1/listings'
        assert config.page_size == '100'
        assert config.max_workers == 10
        assert config.rate_limit == 1.0
        assert config.cache_enabled is True
        assert config.pagination_params == '&page_size=100&size=100'

def test_config_env_vars():
    """Test that CanaConfig loads values from environment variables."""
    env_vars = {
        'WEEDMAPS_BASE_URL': 'https://custom.api.weedmaps.com',
        'PAGE_SIZE': '50',
        'MAX_WORKERS': '5',
        'RATE_LIMIT': '2.5',
        'CACHE_ENABLED': 'false',
        'CACHE_TTL': '1800',
        'MEMORY_CACHE_SIZE': '1000',
        'ENABLE_DISK_CACHE': 'false',
        'OPTIMIZE_PROCESSING': 'false',
        'USE_CONCURRENT_PROCESSING': 'true',
        'MENU_PAGE_SIZE': '50',
        'LOG_LEVEL': 'DEBUG'
    }

    with patch.dict(os.environ, env_vars, clear=True):
        config = CanaConfig()
        assert config.weedmaps_base_url == 'https://custom.api.weedmaps.com'
        assert config.page_size == '50'
        assert config.max_workers == 5
        assert config.rate_limit == 2.5
        assert config.cache_enabled is False
        assert config.cache_ttl == 1800
        assert config.memory_cache_size == 1000
        assert config.enable_disk_cache is False
        assert config.optimize_processing is False
        assert config.use_concurrent_processing is True
        assert config.menu_page_size == 50
        assert config.log_level == 'DEBUG'
        assert config.pagination_params == '&page_size=50&size=50'
