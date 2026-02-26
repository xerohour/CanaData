import os
import sys
import shutil
import pytest
from datetime import datetime
from CanaData import CanaData

class TestSecurity:

    @pytest.fixture
    def cana(self):
        return CanaData(interactive_mode=False)

    def test_path_traversal_sanitization(self, cana):
        # Setup
        malicious_slug = "../traversal_test"
        cana.searchSlug = malicious_slug
        data = [{'key': 'value'}]

        # Action
        cana.csv_maker(f'{cana.searchSlug}_results', data)

        today = datetime.today().strftime('%m-%d-%Y')

        # Calculate where csv_maker thinks home_dir is
        # it uses sys.path[0]
        base_dir = sys.path[0]
        home_dir = os.path.join(base_dir, f"CanaData_{today}")

        # Vulnerable path logic:
        # f'{home_dir}/{filename}.csv' -> f'{base_dir}/CanaData_{today}/../traversal_test_results.csv'
        # -> f'{base_dir}/traversal_test_results.csv'

        vulnerable_path = os.path.join(base_dir, "traversal_test_results.csv")

        is_vulnerable = os.path.exists(vulnerable_path)

        # Safe path logic (if we sanitize):
        # Sanitizer does basename('../traversal_test_results') -> 'traversal_test_results'
        # Then keeps safe chars. So it becomes 'traversal_test_results'

        safe_filename = "traversal_test_results.csv"
        safe_path = os.path.join(home_dir, safe_filename)

        is_safe = os.path.exists(safe_path)

        # Cleanup
        if is_vulnerable:
            os.remove(vulnerable_path)
        if is_safe:
            os.remove(safe_path)
        if os.path.exists(home_dir):
            try:
                os.rmdir(home_dir)
            except OSError:
                pass

        # Assertions
        assert not is_vulnerable, f"Security Vulnerability: File written to vulnerable path! {vulnerable_path}"
        assert is_safe, f"File not found at expected safe path: {safe_path}"
