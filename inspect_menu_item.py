import requests

def get_valid_slug():
    # Remove region filter to ensure we get *any* listing
    url = "https://api-g.weedmaps.com/discovery/v1/listings?filter[any_retailer_services][]=storefront&page_size=1"
    
    try:
        print("Finding a valid dispensary slug...")
        req = requests.get(url, timeout=10)
        if req.status_code == 200:
            data = req.json()
            listings = data.get('data', {}).get('listings', [])
            if listings:
                slug = listings[0].get('slug')
                print(f"Found slug: {slug}")
                return slug
    except Exception as e:
        print(f"Error finding slug: {e}")
    return None

def inspect_menu(slug):
    if not slug:
        return

    url = f"https://weedmaps.com/api/web/v1/listings/{slug}/menu?type=dispensary"
    print(f"Fetching menu for {slug}...")
    try:
        req = requests.get(url, timeout=10)
        if req.status_code == 200:
            data = req.json()
            categories = data.get('categories', [])
            if categories:
                # Find a category with items
                for cat in categories:
                    items = cat.get('items', [])
                    if items:
                        print(f"Found {len(items)} items in category '{cat.get('title')}'.")
                        item = items[0]
                        print("\n--- Item Keys ---")
                        print(list(item.keys()))
                        
                        # Check for strain specific fields
                        print("\n--- Strain Related Data ---")
                        found_strain_data = False
                        for key in ['strain_id', 'strain_slug', 'strain_name', 'strain', 'genetics', 'classification']:
                            if key in item:
                                print(f"{key}: {item[key]}")
                                found_strain_data = True
                        
                        if not found_strain_data:
                            print("No direct strain fields found.")

                        # Recurse a bit if 'strain' is a dict
                        if 'strain' in item and isinstance(item['strain'], dict):
                            print("\n--- Strain Object Keys ---")
                            print(list(item['strain'].keys()))
                        
                        return # Inspect only one item
            else:
                print("No categories found.")
        else:
            print(f"Failed: {req.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    slug = "metropolitan-wellness-center"
    inspect_menu(slug)
