import os
import shutil
import pytest
from datetime import datetime
from CanaData import CanaData
import sys

class TestSecurity:

    @pytest.fixture
    def cana(self):
        return CanaData()

    def test_sanitize_filename(self, cana):
        """Test that filenames are correctly sanitized."""
        # Test basic alphanumeric
        assert cana._sanitize_filename("valid_filename") == "valid_filename"

        # Test path traversal characters
        # Replaces slash with underscore
        assert cana._sanitize_filename("dir/filename") == "dir_filename"
        assert cana._sanitize_filename("dir\\filename") == "dir_filename"

        # Replaces path traversal sequence (../ -> .._)
        assert cana._sanitize_filename("../invalid_filename") == ".._invalid_filename"

        # Test other special characters
        assert cana._sanitize_filename("file$name") == "file_name"
        assert cana._sanitize_filename("file name") == "file_name"

        # Test allowed special characters
        assert cana._sanitize_filename("file-name.csv") == "file-name.csv"
        assert cana._sanitize_filename("file_name") == "file_name"
        assert cana._sanitize_filename("file.name") == "file.name"

    def test_csv_maker_traversal_prevention(self, cana):
        """Test that csv_maker prevents path traversal."""
        malicious_filename = "../security_test"
        data = [{'test': 'data'}]

        # Run csv_maker
        cana.csv_maker(malicious_filename, data)

        today = datetime.today().strftime('%m-%d-%Y')
        # Based on sys.path[0] being the test directory when running pytest
        base_dir = sys.path[0]
        cana_dir = os.path.join(base_dir, f'CanaData_{today}')

        # If traversal succeeded (vulnerability present), file would be here:
        exploited_path = os.path.join(base_dir, "security_test.csv")

        # If sanitized correctly, file should be here:
        sanitized_name = cana._sanitize_filename(malicious_filename) + ".csv"
        sanitized_path = os.path.join(cana_dir, sanitized_name)

        # Verify vulnerability is NOT exploited
        assert not os.path.exists(exploited_path), f"Vulnerability exploited! File found at {exploited_path}"

        # Verify sanitized file IS created
        assert os.path.exists(sanitized_path), f"Sanitized file not found at {sanitized_path}"

        # Cleanup
        if os.path.exists(sanitized_path):
            os.remove(sanitized_path)
        if os.path.exists(cana_dir) and not os.listdir(cana_dir):
            os.rmdir(cana_dir)
        if os.path.exists(exploited_path):
            os.remove(exploited_path)
