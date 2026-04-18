import requests
import os
from dotenv import load_dotenv

load_dotenv()

"""
CannMenus API Client Module

This module provides a client for interacting with the CannMenus API, allowing users to
fetch dispensary and menu data from legalized states. It handles authentication via
environment variables and provides normalized data structures.
"""


class CannMenusClient:
    """
    Official API Client for CannMenus.

    This client authenticates with the CannMenus API to retrieve retailer lists
    and detailed menus. It is designed to work with the `CanaData` scraper
    to provide an alternative data source to Weedmaps.

    Attributes:
        api_token (str): API key from environment variable CANNMENUS_API_TOKEN
        base_url (str): Base endpoint for the API (v1)
        headers (dict): Standard headers including authentication token

    Usage:
        >>> client = CannMenusClient()
        >>> retailers = client.get_retailers("NY")
        >>> menu = client.get_menu(retailers[0]['id'])
    """

    def __init__(self):
        self.api_token = os.getenv('CANNMENUS_API_TOKEN')
        self.base_url = "https://api.cannmenus.com/v1"
        self.headers = {
            "X-Token": f"{self.api_token}",
            "Accept": "application/json"
        }

    def get_retailers(self, state):
        """
        Fetch a list of active retailers in a specific state.

        Args:
            state (str): Two-letter state code (e.g., 'CA', 'NY', 'CO').

        Returns:
            list: A list of dictionaries, where each dictionary represents a retailer.
                  Returns an empty list if the request fails or API token is missing.

        Example Data:
            [
                {'id': '123', 'name': 'Green Hope', 'city': 'New York', ...},
                ...
            ]
        """
        if not self.api_token:
            print("Error: CANNMENUS_API_TOKEN not found.")
            return []

        url = f"{self.base_url}/retailers?state={state}"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            print(f"Error fetching retailers: {str(e)}")
            return []

    def get_menu(self, retailer_id):
        """
        Fetch the full normalized menu for a specific retailer.

        Args:
            retailer_id (str): The unique CannMenus ID for the retailer.

        Returns:
            list: A list of standardized menu items. Returns empty list on failure.
                  The API returns items that are already flattened/normalized,
                  making them compatible with CanaData's export format.
        """
        url = f"{self.base_url}/retailers/{retailer_id}/menu"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            # Returns already flattened/normalized menu items
            return response.json().get('data', [])
        except Exception as e:
            print(f"Error fetching menu: {str(e)}")
            return []


if __name__ == "__main__":
    # Test script usage
    client = CannMenusClient()
    # Replace with real values to test
    # retailers = client.get_retailers("NY")
    # print(f"Found {len(retailers)} retailers in NY.")
