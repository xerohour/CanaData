import requests

def check_endpoint(name, url):
    print(f"\n--- Testing: {name} ---")
    print(f"URL: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://weedmaps.com/',
        'Origin': 'https://weedmaps.com'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            # Print keys or a snippet for structure analysis
            if isinstance(data, dict):
                print(f"Top-level keys: {list(data.keys())}")
                if 'data' in data:
                    print(f"Data type: {type(data['data'])}")
                    if isinstance(data['data'], list) and len(data['data']) > 0:
                        print("First item keys:", data['data'][0].keys() if isinstance(data['data'][0], dict) else "Not a dict")
            return data
        else:
            print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    return None

if __name__ == "__main__":
    # 1. Test EXACT URL from README
    readme_url = "https://api-g.weedmaps.com/discovery/v1/listings?filter[any_retailer_services][]=storefront&filter[any_retailer_services][]=delivery&filter[region_slug[deliveries]]=washington-dc&filter[region_slug[dispensaries]]=washington-dc&page_size=100&size=100"
    check_endpoint("README CURL Example", readme_url)
    
    # 2. Test Region Discovery again without custom User-Agent (let requests use default)
    # Actually, let's try with a more 'browser-like' set of headers if the above fails.
    
    # 3. Test the Menu endpoint which uses weedmaps.com (not api-g)
    check_endpoint("Web Menu API", "https://weedmaps.com/api/web/v1/listings/metropolitan-wellness-center/menu?type=dispensary")
