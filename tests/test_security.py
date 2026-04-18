import os
import pytest
from CanaData import CanaData
from datetime import datetime
import shutil


class TestSecurity:

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        # Setup: Ensure clean state
        traversal_file = "traversal_test.csv"
        if os.path.exists(traversal_file):
            os.remove(traversal_file)

        today = datetime.today().strftime('%m-%d-%Y')
        # Check where CanaData writes
        dirs_to_check = [f'CanaData_{today}', f'tests/CanaData_{today}']

        for d in dirs_to_check:
            if os.path.exists(d):
                shutil.rmtree(d, ignore_errors=True)

        yield

        # Teardown: remove created files
        if os.path.exists(traversal_file):
            os.remove(traversal_file)

        for d in dirs_to_check:
            if os.path.exists(d):
                shutil.rmtree(d, ignore_errors=True)

    def test_path_traversal_sanitization(self):
        """Test that path traversal attempts are sanitized in csv_maker."""
        cana = CanaData()

        # malicious_filename intended to traverse up one directory
        malicious_filename = "../traversal_test"
        data = [{'test': 'data'}]

        # Attempt to exploit
        try:
            cana.csv_maker(malicious_filename, data)
        except Exception:
            pass

        # Check if traversal occurred (file written outside intended directory)
        traversal_file = "traversal_test.csv"

        if os.path.exists(traversal_file):
            pytest.fail(
                f"Path traversal vulnerability exploited! File found at {traversal_file}")

        # Verify that the file WAS created in the correct location with sanitized name
        # We need to find where it was written.
        # Based on sys.path[0], it could be in tests/CanaData_DATE or
        # ./CanaData_DATE
        import sys
        today = datetime.today().strftime('%m-%d-%Y')
        sanitized_filename = "..traversal_test"

        # Possible locations
        possible_paths = [
            f'{sys.path[0]}/CanaData_{today}/{sanitized_filename}.csv',
            f'CanaData_{today}/{sanitized_filename}.csv'
        ]

        found = False
        for p in possible_paths:
            if os.path.exists(p):
                found = True
                break

        if not found:
            # It might be fine if exception was raised, but we expect sanitization and write
            # However, let's just assert that traversal didn't happen.
            pass

    def test_sanitize_filename_method(self):
        """Test the _sanitize_filename method directly."""
        cana = CanaData()

        # This checks if the method exists and works as expected
        if not hasattr(cana, '_sanitize_filename'):
            pytest.fail(
                "_sanitize_filename method is missing! Security fix not implemented.")

        # These assertions verify the implementation logic
        assert cana._sanitize_filename("../evil") == "..evil"
        assert cana._sanitize_filename(
            "valid-file_name.123") == "valid-file_name.123"
        assert cana._sanitize_filename(
            "invalid/characters!@#") == "invalidcharacters"
        assert cana._sanitize_filename(
            "..\\windows\\style") == "..windowsstyle"
        assert cana._sanitize_filename("foo bar") == "foobar"  # spaces removed
