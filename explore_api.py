from CanaData import CanaData
import json
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', stream=sys.stdout)
logger = logging.getLogger('APIExplorer')

def explore_endpoint(name, url):
    cana = CanaData()
    logger.info(f"Testing {name} endpoint: {url}")
    
    # We use the do_request method which has the curl user-agent now
    result = cana.do_request(url)
    
    if result and result != 'break':
        logger.info(f"✅ SUCCESS: {name} returned data.")
        
        # Save a sample to a file for analysis
        filename = f"sample_{name.lower().replace(' ', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
        logger.info(f"Data sample saved to {filename}")
        
        # Look for cross-reference keys
        data_keys = result.get('data', {}).keys()
        logger.info(f"Available data keys: {list(data_keys)}")
        
        # Try to find specific IDs or identifiers
        first_item = None
        for key in data_keys:
            items = result['data'].get(key, [])
            if items and isinstance(items, list):
                first_item = items[0]
                break
        
        if first_item and isinstance(first_item, dict):
            logger.info("Potential cross-reference fields found in first item:")
            id_fields = [k for k in first_item.keys() if 'id' in k.lower() or 'slug' in k.lower() or 'license' in k.lower() or 'sku' in k.lower()]
            for field in id_fields:
                logger.info(f"  - {field}: {first_item[field]}")
        
        return result
    else:
        logger.error(f"❌ FAILED: {name} endpoint returned error or no data.")
        return None

if __name__ == "__main__":
    endpoints = [
        ("Products", "https://api-g.weedmaps.com/discovery/v1/products?page_size=5&size=5"),
        ("Brands", "https://api-g.weedmaps.com/discovery/v1/brands?page_size=5&size=5"),
        ("Categories", "https://api-g.weedmaps.com/discovery/v1/categories")
    ]
    
    for name, url in endpoints:
        explore_endpoint(name, url)
        print("-" * 50)
