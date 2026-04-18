import requests
import time


def check_url(url, description, headers=None):
    print(f"Testing {description}...")
    print(f"  URL: {url}")
    print(f"  Headers: {headers}")
    try:
        if headers:
            resp = requests.get(url, headers=headers, timeout=10)
        else:
            resp = requests.get(url, timeout=10)

        print(f"  Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            if 'data' in data:
                print(
                    f"  [SUCCESS] Found data keys: {
                        list(
                            data.get(
                                'data',
                                {}).keys())}")
                if 'meta' in data:
                    print(f"  [SUCCESS] Meta: {data.get('meta')}")
                return True
            else:
                print("  [WARN] 200 OK but no 'data' key.")
        elif resp.status_code == 403 or resp.status_code == 401:
            print("  [FAIL] Auth required.")
        elif resp.status_code == 404:
            print("  [FAIL] Not Found.")
        else:
            print(f"  [FAIL] {resp.status_code}")
    except Exception as e:
        print(f"  [ERROR] {str(e)}")
    print("-" * 40)
    return False


if __name__ == "__main__":
    versions = ['v1', 'v2', '2024-01', '2025-01', '2026-01']
    bases = [
        'https://api-g.weedmaps.com/discovery/{ver}/strains',
        'https://api-g.weedmaps.com/wm/{ver}/partners/strains',
    ]

    # Try different header configurations
    header_configs = [
        {"name": "No Headers", "headers": None},
        {"name": "Minimal User-Agent", "headers": {'User-Agent': 'Mozilla/5.0'}},
        {"name": "Full Chrome Headers", "headers": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://weedmaps.com',
            'Referer': 'https://weedmaps.com/'
        }}
    ]

    print("Starting version discovery...\n")

    found_any = False
    for ver in versions:
        for base in bases:
            url = base.format(ver=ver) + "?page_size=1"
            for config in header_configs:
                if check_url(url,
                             f"Version {ver} Path ({config['name']})",
                             config['headers']):
                    found_any = True
                    break  # Stop trying headers if one works for this URL
                time.sleep(1)  # Be nice

    if not found_any:
        print("\nNo working public endpoints found with standard patterns.")
