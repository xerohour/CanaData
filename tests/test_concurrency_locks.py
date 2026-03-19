import pytest
import threading
from CanaData import CanaData
import time
from unittest.mock import patch

def test_fine_grained_locks():
    cana = CanaData()
    assert hasattr(cana, '_items_lock')
    assert hasattr(cana, '_empty_lock')
    assert hasattr(cana, '_strains_lock')
    assert hasattr(cana, '_count_lock')
    assert hasattr(cana, '_locations_lock')
