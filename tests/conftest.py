import sys
import os
import shutil
import tempfile

import pytest

# Add the project root to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CanaData import CanaData


@pytest.fixture
def cana(tmp_path):
    """Create a CanaData instance with a temporary cache directory."""
    instance = CanaData()
    # Override cache directory to use a temp path so tests don't pollute the repo
    instance.cacheDir = str(tmp_path / '.cache')
    os.makedirs(instance.cacheDir, exist_ok=True)
    # Speed up tests by removing rate-limit delay
    instance.rateLimitDelay = 0
    return instance


@pytest.fixture
def output_dir(tmp_path):
    """Provide a temporary output directory for CSV tests."""
    return tmp_path
