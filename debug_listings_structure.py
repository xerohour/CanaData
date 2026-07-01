import requests

url = "https://api-g.weedmaps.com/discovery/v1/listings?page_size=1"

print(f"Fetching: {url}")
try:
    req = requests.get(url, timeout=10)
    print(f"Status: {req.status_code}")
    if req.status_code == 200:
        data = req.json()
        print(f"Top keys: {list(data.keys())}")
        if 'data' in data:
            d = data['data']
            print(f"Data keys: {list(d.keys())}")
            if 'listings' in d:
                listings = d['listings']
                print(f"Listings count: {len(listings)}")
                if len(listings) > 0:
                    print(f"First listing keys: {list(listings[0].keys())}")
                    print(f"First listing slug: {listings[0].get('slug')}")
            else:
                print("'listings' key not found in data.")
        else:
            print("'data' key not found.")
    else:
        print(f"Response: {req.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
