import os
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

"""
Leafly Data Scraper Module

This module leverages the Apify platform to scrape dispensary and product data from Leafly.
It acts as a wrapper around the `paradox-analytics/leafly-scraper` actor.
"""


def scrape_leafly(location_slug):
    """
    Scrape Leafly dispensary and product data using the Apify API.

    This function triggers a remote Apify actor run to collect data for a specific
    location. It waits for the run to complete and then downloads the results.

    Prerequisites:
        - APIFY_TOKEN must be set in the .env file.

    Args:
        location_slug (str): The city or region slug as used on Leafly (e.g., 'los-angeles', 'portland-or').

    Returns:
        list: A list of dictionaries, where each dictionary represents a scraped product or dispensary item.
              Returns an empty list if the scraping run fails or credentials are missing.

    Configuration:
        The scraper is currently configured to:
        - Fetch max 50 stores per run
        - Include product details (`scrapeProducts: True`)
        - Use Apify proxies to avoid IP bans
    """
    token = os.getenv("APIFY_TOKEN")
    if not token:
        print("Error: APIFY_TOKEN not found in environment variables.")
        return []

    client = ApifyClient(token)

    # Prepare the Actor input for paradox-analytics/leafly-scraper
    run_input = {
        "location": location_slug,
        "maxStores": 50,
        "scrapeProducts": True,
        "proxyConfiguration": {"useApifyProxy": True},
    }

    print(f"🚀 Starting Leafly scrape for: {location_slug}...")

    try:
        # Run the Actor and wait for it to finish
        run = client.actor("paradox-analytics/leafly-scraper").call(run_input=run_input)

        # Fetch results from the run's dataset
        print("✅ Scraping complete. Downloading results...")
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append(item)

        return results
    except Exception as e:
        print(f"❌ Leafly scrape failed: {str(e)}")
        return []


if __name__ == "__main__":
    # Test script
    test_slug = "los-angeles"
    data = scrape_leafly(test_slug)
    print(f"Retrieved {len(data)} items total.")
