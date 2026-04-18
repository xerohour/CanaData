import requests


def check_simple(url):
    print(f"Testing URL: {url}")
    try:
        resp = requests.get(url, timeout=30)
        print(f"Status Code: {resp.status_code}")
        if resp.status_code == 200:
            print("Success!")
        else:
            print(f"Failed: {resp.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")


def check_inspect(url):
    print(f"Inspecting URL: {url}")
    try:
        resp = requests.get(url, timeout=30)
        print(f"Status Code: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print("Successfully fetched data.")
            # Print keys
            print(f"Top level keys: {data.keys()}")
            if 'data' in data:
                print(f"Data type: {type(data['data'])}")
                if isinstance(data['data'], list) and len(data['data']) > 0:
                    print(f"Sample item keys: {data['data'][0].keys()}")
                elif isinstance(data['data'], dict):
                    print(f"Data keys: {data['data'].keys()}")
                    # Check for nested list
                    for k, v in data['data'].items():
                        if isinstance(v, list) and len(v) > 0:
                            keys_str = v[0].keys() if hasattr(v[0], 'keys') else 'No keys'
                            print(f"Found list in '{k}', sample item keys: {keys_str}")
                            break
        else:
            print(f"Failed: {resp.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    check_inspect("https://api-g.weedmaps.com/discovery/v1/brands?page_size=1")
    check_inspect(
        "https://api-g.weedmaps.com/discovery/v1/listings?page_size=1")
