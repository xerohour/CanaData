import requests
import json

def test_endpoint(url):
    print(f"Testing URL: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://weedmaps.com',
        'Referer': 'https://weedmaps.com/'
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print("Successfully fetched data.")
            # Print keys and a sample
            if 'data' in data:
                print(f"Data keys: {data['data'].keys() if isinstance(data['data'], dict) else 'List data'}")
                if isinstance(data['data'], list) and len(data['data']) > 0:
                    print(f"Sample data: {json.dumps(data['data'][0], indent=2)[:500]}...")
                elif isinstance(data['data'], dict):
                    # Check for nested list
                    for k, v in data['data'].items():
                        if isinstance(v, list) and len(v) > 0:
                            print(f"Sample data from '{k}': {json.dumps(v[0], indent=2)[:500]}...")
                            break
            elif 'strains' in data:
                 print(f"Sample strains: {json.dumps(data['strains'][0], indent=2)[:500]}...")
            elif 'brands' in data:
                 print(f"Sample brands: {json.dumps(data['brands'][0], indent=2)[:500]}...")
            else:
                print(f"Top level keys: {data.keys()}")
        else:
            print(f"Failed with text: {resp.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)

if __name__ == "__main__":
    # Test strains
    test_endpoint("https://api-g.weedmaps.com/discovery/v1/strains?page_size=10")
    # Test brands
    test_endpoint("https://api-g.weedmaps.com/discovery/v1/brands?page_size=10")
    # Test listings
    test_endpoint("https://api-g.weedmaps.com/discovery/v1/listings?page_size=10")
