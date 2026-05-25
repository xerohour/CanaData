from CanaData import CanaData
import logging
import sys

# Configure logging to show the output in the console
# The logger in CanaData.py is named 'CanaData' or '__name__'
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)


def test_connection():
    """
    Test the Weedmaps connection using the current do_request implementation.
    This helps verify if headers are needed or if the API is blocking requests.
    """
    cana = CanaData()

    # Use the Colorado discovery URL
    url = "https://api-g.weedmaps.com/discovery/v1/listings?filter[any_retailer_services][]=storefront&filter[any_retailer_services][]=delivery&filter[region_slug[deliveries]]=colorado&filter[region_slug[dispensaries]]=colorado&page_size=1&size=1"

    print("\n[Verification] Testing Weedmaps API Connection...")
    print(f"[Verification] URL: {url}")

    result = cana.do_request(url)

    if result and result != "break":
        print("\n[SUCCESS] Data retrieved successfully!")
        meta = result.get("meta", {})
        total = meta.get("total_listings", "unknown")
        print(f"[INFO] Total listings found for Colorado: {total}")

        # Print first listing name if available
        listings = result.get("data", {}).get("listings", [])
        if listings:
            print(f"[INFO] Sample location: {listings[0].get('name')}")

    elif result == "break":
        print(
            "\n[WARNING] Received 422 Validation Error. The connection worked, but the parameters might be invalid."
        )
    else:
        print(
            "\n[FAILURE] Request failed. Check your logs for 406 (Not Acceptable) or other errors."
        )
        print(
            "[TIP] If you see 406, you likely need to re-add the headers to do_request in CanaData.py."
        )


if __name__ == "__main__":
    test_connection()
