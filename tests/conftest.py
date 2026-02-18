"""
Shared fixtures and test utilities for the CanaData test suite.

Provides reusable fixtures for CanaData instances, cache managers,
concurrent processors, data processors, and sample test data.
"""

import sys
import os
import pytest
import tempfile
import shutil
from unittest.mock import patch

# Add the project root to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cache_manager import CacheManager
from concurrent_processor import ConcurrentMenuProcessor
from optimized_data_processor import OptimizedDataProcessor


@pytest.fixture
def canadata_instance():
    """Create a CanaData instance with caching disabled to avoid side effects."""
    from CanaData import CanaData
    return CanaData(cache_enabled=False, optimize_processing=False)


@pytest.fixture
def canadata_optimized():
    """Create a CanaData instance with optimized processing enabled."""
    from CanaData import CanaData
    return CanaData(cache_enabled=False, optimize_processing=True)


@pytest.fixture
def cache_manager(tmp_path):
    """Create a CacheManager instance backed by a temporary directory."""
    return CacheManager(cache_dir=str(tmp_path / "cache"))


@pytest.fixture
def temp_cache_dir(tmp_path):
    """Provide a temporary cache directory path."""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return str(cache_dir)


@pytest.fixture
def concurrent_processor():
    """Create a ConcurrentMenuProcessor with fast settings for tests."""
    return ConcurrentMenuProcessor(max_workers=3, rate_limit=0.01)


@pytest.fixture
def optimized_processor():
    """Create an OptimizedDataProcessor instance."""
    return OptimizedDataProcessor(max_workers=2)


# ---------------------------------------------------------------------------
# Sample data fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_menu_json():
    """Sample menu JSON as returned by the Weedmaps menu endpoint."""
    return {
        "listing": {
            "id": 12345,
            "slug": "test-dispensary",
            "wmid": 67890,
            "name": "Test Dispensary"
        },
        "categories": [
            {
                "title": "Flower",
                "items": [
                    {
                        "name": "Blue Dream",
                        "price": {"amount": 50, "currency": "USD"},
                        "thc": 18,
                        "category": "flower",
                        "strain_data": {
                            "slug": "blue-dream",
                            "name": "Blue Dream",
                            "genetics": "hybrid"
                        }
                    },
                    {
                        "name": "OG Kush",
                        "price": {"amount": 55, "currency": "USD"},
                        "thc": 22,
                        "category": "flower",
                        "strain_data": {
                            "slug": "og-kush",
                            "name": "OG Kush",
                            "genetics": "indica"
                        }
                    }
                ]
            },
            {
                "title": "Concentrates",
                "items": [
                    {
                        "name": "Shatter",
                        "price": {"amount": 40, "currency": "USD"},
                        "thc": 80,
                        "category": "concentrates"
                    }
                ]
            }
        ]
    }


@pytest.fixture
def sample_locations():
    """Sample location list matching the internal CanaData format."""
    return [
        {"slug": "dispensary-1", "type": "dispensary"},
        {"slug": "dispensary-2", "type": "dispensary"},
        {"slug": "delivery-1", "type": "delivery"},
    ]


@pytest.fixture
def sample_locations_response():
    """Sample API response from the Weedmaps listings endpoint."""
    return {
        "meta": {"total_listings": 2},
        "data": {
            "listings": [
                {"slug": "dispensary-1", "type": "dispensary"},
                {"slug": "dispensary-2", "type": "dispensary"},
            ]
        }
    }


@pytest.fixture
def sample_menu_items_dict():
    """Sample allMenuItems dictionary for data processing tests."""
    return {
        "location-1": [
            {
                "name": "Product A",
                "price": {"amount": 25, "currency": "USD"},
                "tags": ["indica", "relaxing"],
            },
            {
                "name": "Product B",
                "price": {"amount": 30, "currency": "USD"},
                "tags": ["sativa", "energizing"],
            },
        ],
        "location-2": [
            {
                "name": "Product C",
                "price": {"amount": 45, "currency": "USD"},
                "tags": ["hybrid"],
            }
        ],
    }
