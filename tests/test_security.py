import os
import shutil
import pytest
from unittest.mock import patch, MagicMock
from CanaData import CanaData
from datetime import datetime

class TestSecurity:
    @pytest.fixture
    def cana(self):
        return CanaData(cache_enabled=False)

    def test_path_traversal_prevention(self, cana, tmp_path):
        """
        Verify that filenames with traversal characters are sanitized
        and files are written within the intended directory.
        """
        # Mock sys.path[0] to be tmp_path
        with patch('CanaData.path', [str(tmp_path)]):
            # Setup malicious slug
            cana.searchSlug = "../../../evil_traversal"
            cana.finishedMenuItems = [{"test": "data"}]

            # Execute csv_maker
            # The filename passed will be "../../../evil_traversal_results"
            filename = f"{cana.searchSlug}_results"
            cana.csv_maker(filename, cana.finishedMenuItems)

            # Calculate expected directory
            today = datetime.today().strftime('%m-%d-%Y')
            expected_dir = tmp_path / f"CanaData_{today}"

            # Verify directory exists
            assert expected_dir.exists()

            # Verify file exists inside the directory with sanitized name
            # The sanitizer replaces .. with nothing (basename) or _
            # _sanitize_filename uses os.path.basename, then regex.
            # os.path.basename("../../../evil_traversal_results") -> "evil_traversal_results"
            # Regex [^a-zA-Z0-9_.-] -> keeps it as is.
            expected_file = expected_dir / "evil_traversal_results.csv"
            assert expected_file.exists()

            # Verify file does NOT exist outside
            traversal_file = tmp_path / "evil_traversal_results.csv"
            assert not traversal_file.exists()

    def test_sanitize_filename_method(self, cana):
        """Test the sanitization logic directly."""
        # Standard traversal (Unix)
        assert cana._sanitize_filename("../evil") == "evil"
        assert cana._sanitize_filename("valid_file") == "valid_file"
        assert cana._sanitize_filename("file/with/slash") == "slash"

        # Backslash handling (platform dependent or just sanitized char)
        # On Linux, \ is a char, so it gets replaced by _
        # On Windows, it would be a separator.
        # We just verify it doesn't return the full path with separators intact.
        sanitized_backslash = cana._sanitize_filename("file\\with\\backslash")
        assert "\\" not in sanitized_backslash
        assert "/" not in sanitized_backslash

        # Hidden files are prefixed
        assert cana._sanitize_filename(".hidden") == "_.hidden"
        assert cana._sanitize_filename("file with spaces") == "file_with_spaces"

        # Command injection chars are replaced
        sanitized_cmd = cana._sanitize_filename("file;rm -rf /")
        assert ";" not in sanitized_cmd
        assert " " not in sanitized_cmd
        assert "/" not in sanitized_cmd
