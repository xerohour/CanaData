import requests
import os
from dotenv import load_dotenv

load_dotenv()


def check_endpoint(name, url, headers=None):
    print(f"Testing {name}...")
    try:
        if headers:
            resp = requests.get(url, headers=headers, timeout=15)
        else:
            resp = requests.get(url, timeout=15)

        status = resp.status_code
        if status == 200:
            print(f"  [OK] 200 - {name}")
            return True
        elif status == 406:
            print(f"  [FAIL] 406 Not Acceptable (Bot Detection) - {name}")
        elif status == 404:
            print(
                f"  [INFO] 404 Not Found (Endpoint may have changed) - {name}")
        else:
            print(f"  [WARN] {status} - {name}")
    except Exception as e:
        print(f"  [ERROR] {str(e)} - {name}")
    return False


if __name__ == "__main__":
    print("--- LIVE ENDPOINT VERIFICATION ---\n")

    # Weedmaps Discovery
    check_endpoint("Weedmaps Listings",
                   "https://api-g.weedmaps.com/discovery/v1/listings?page_size=1")
    check_endpoint("Weedmaps Brands",
                   "https://api-g.weedmaps.com/discovery/v1/brands?page_size=1")
    check_endpoint("Weedmaps Strains",
                   "https://api-g.weedmaps.com/discovery/v1/strains?page_size=1")
    check_endpoint("Weedmaps Taxonomy",
                   "https://api-g.weedmaps.com/discovery/v1/taxonomy/strains?page_size=1")

    # CannMenus (Requires Key)
    cm_key = os.getenv('CANNMENUS_API_TOKEN')
    if cm_key:
        check_endpoint("CannMenus Retailers",
                       "https://api.cannmenus.com/v1/retailers?state=NY", headers={"X-Token": cm_key})
    else:
        print("Skipping CannMenus (No API Key)")

    # Leafly (Requires Key)
    af_key = os.getenv('APIFY_TOKEN')
    if not af_key:
        print("Skipping Leafly (No Apify Token)")

    print("\n--- TEST COMPLETE ---")
