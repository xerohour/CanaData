import unittest
from unittest.mock import MagicMock, patch
import os
import urllib.parse

# Import after setting env vars if needed, but here we patch os.getenv
with patch.dict(os.environ, {'CANNMENUS_API_TOKEN': 'test-token'}):
    from CanaData import CanaData
    from CannMenusClient import CannMenusClient

class TestSecurityFix(unittest.TestCase):
    def test_search_slug_sanitization(self):
        cana = CanaData()
        # Malicious slug that attempts parameter injection
        malicious_slug = "california&injected=true"
        cana.setCitySlug(malicious_slug)

        # Mock do_request to capture the URL
        cana.do_request = MagicMock(return_value={'data': {'listings': []}, 'meta': {'total_listings': 0}})

        cana.getLocations()

        # Check the URL passed to do_request
        call_args = cana.do_request.call_args
        if call_args:
            url = call_args[0][0]

            # Check for parameter injection prevention
            self.assertFalse("&injected=true" in url and "%26injected%3Dtrue" not in url,
                             "Parameter injection successful in CanaData!")

            # Check for correct encoding
            self.assertIn("california%26injected%3Dtrue", url, "Slug is NOT encoded in CanaData.")
        else:
            self.fail("do_request was not called.")

    @patch('requests.get')
    def test_cannmenus_sanitization(self, mock_get):
        # Ensure token is set for this test
        with patch.dict(os.environ, {'CANNMENUS_API_TOKEN': 'test-token'}):
            client = CannMenusClient()
            # Malicious state
            malicious_state = "CA&injected=true"

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'data': []}
            mock_get.return_value = mock_response

            client.get_retailers(malicious_state)

            call_args = mock_get.call_args
            if call_args:
                url = call_args[0][0]

                self.assertFalse("&injected=true" in url and "%26injected%3Dtrue" not in url,
                                 "Parameter injection successful in CannMenus!")

                self.assertIn("CA%26injected%3Dtrue", url, "State is NOT encoded in CannMenus.")
            else:
                 self.fail("requests.get was not called.")

if __name__ == "__main__":
    unittest.main()
