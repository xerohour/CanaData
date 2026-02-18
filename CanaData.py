import requests
import json
import csv
import logging
import os
from datetime import datetime
from os import path as ospath
from os import makedirs
from sys import path, argv
from typing import Optional, List, Dict, Any, Union
from dotenv import load_dotenv
from LeaflyScraper import scrape_leafly
from CannMenusClient import CannMenusClient
from data_sources import DataSourceManager
import concurrent.futures
import threading
import time
from concurrent_processor import ConcurrentMenuProcessor
from cache_manager import CacheManager
from cached_api_client import CachedAPIClient
from optimized_data_processor import OptimizedDataProcessor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Low and behold, the almighty CanaData
class CanaData:
    """
    CanaData - A Weedmaps Data Scraper
    
    This class provides functionality to scrape cannabis dispensary and delivery service
    data from Weedmaps API, including location information and menu items.
    
    Workflow:
    1. Initialize with configuration settings
    2. Set search slug (city/state identifier)
    3. Retrieve all locations for the slug via paginated API calls
    4. For each location, fetch and flatten menu data
    5. Export results to CSV files
    
    Attributes:
        baseUrl (str): Base API endpoint for Weedmaps discovery
        pageSize (str): Pagination parameters for API requests
        searchSlug (str): Current city/state slug being processed
        storefronts (bool): Whether to include storefront dispensaries
        deliveries (bool): Whether to include delivery services
        locationsFound (int): Counter for locations retrieved
        testMode (bool): Enable verbose debugging output
        menuItemsFound (int): Counter for total menu items processed
        maxLocations (int): Total locations available for current slug
        locations (list): Collection of location dictionaries with slug and type
        emptyMenus (dict): Locations with no menu items
        allMenuItems (dict): Menu items organized by location ID
        finishedMenuItems (list): Flattened menu items ready for export
        totalLocations (list): All location metadata
        unFriendlyStates (list): Slugs with zero locations found
        NonGreenState (bool): Flag indicating current slug has no locations
        slugGrab (bool): Whether to save discovered slugs
    """
    def __init__(self, max_workers: int = 10, rate_limit: float = 1.0, cache_enabled: bool = True, optimize_processing: bool = True):
        # Where the Magic happens
        self.baseUrl: str = os.getenv('WEEDMAPS_BASE_URL', 'https://api-g.weedmaps.com/discovery/v1/listings')
        self.brandsBaseUrl: str = os.getenv('WEEDMAPS_BRANDS_URL', 'https://api-g.weedmaps.com/discovery/v1/brands')
        self.strainsBaseUrl: str = os.getenv('WEEDMAPS_STRAINS_URL', 'https://api-g.weedmaps.com/discovery/v1/strains')
        # Pagination & Page size
        self.pageSize: str = f"&page_size={os.getenv('PAGE_SIZE', '100')}&size={os.getenv('PAGE_SIZE', '100')}"
        # Populated with the City/State Slug
        self.searchSlug: Optional[str] = None
        # Set to True if we are grabbing storefronts
        self.storefronts: bool = True
        # Set to True if we are grabbing deliveries
        self.deliveries: bool = True
        # Number of Locations found for searchSlug
        self.locationsFound: int = 0
        # Set to true if troubleshooting
        self.testMode: bool = False
        # Number of Items found
        self.menuItemsFound: int = 0
        # Number returned from Weedmaps as to Max # of locations
        self.maxLocations: Optional[int] = None
        # Dataset of locations
        self.locations: List[Dict[str, Any]] = []
        # Dictionary of Empty Location Menus
        self.emptyMenus: Dict[str, Any] = {}
        # Avoids duplicating items from deliveries using their Storefront Menus
        self.allMenuItems: Dict[str, List[Dict[str, Any]]] = {}
        # List of flattened menu items
        self.finishedMenuItems: List[Dict[str, str]] = []
        # List of total flattened locations
        self.totalLocations: List[Dict[str, Any]] = []
        # List of States with No locations
        self.unFriendlyStates: List[str] = []
        # Set to True if there are no locations
        self.NonGreenState: bool = False
        # Sets whether or not we grab the slugs for the search
        self.slugGrab: bool = False
        # Brand and Strain datasets
        self.brands: List[Dict[str, Any]] = []
        self.strains: List[Dict[str, Any]] = []
        self.extractedStrains: Dict[str, Any] = {}
        self.brandsFound: int = 0
        self.strainsFound: int = 0
        
        # Concurrent processing configuration
        self.max_workers = max_workers
        self.rate_limit = rate_limit
        
        # Caching configuration
        self.cache_enabled = cache_enabled
        if cache_enabled:
            cache_ttl = int(os.getenv('CACHE_TTL', 3600))
            self.cache_manager = CacheManager(
                memory_cache_size=int(os.getenv('MEMORY_CACHE_SIZE', 2000)),
                memory_cache_ttl=cache_ttl,
                disk_cache_ttl=cache_ttl * 6,  # Disk cache lasts longer
                enable_disk_cache=os.getenv('ENABLE_DISK_CACHE', 'true').lower() == 'true'
            )
            self.api_client = CachedAPIClient(self.cache_manager)
        else:
            self.cache_manager = None
            self.api_client = None
            
        # Data processing optimization
        self.optimize_processing = optimize_processing
        if optimize_processing:
            self.data_processor = OptimizedDataProcessor(max_workers=max_workers)
        else:
            self.data_processor = None

        # Pluggable data source manager
        self.source_manager = DataSourceManager()
        self.source_manager.auto_register()

    def do_request(self, url, use_cache: bool = True):
        """
        Execute HTTP GET request and return JSON response.
        
        This is the core HTTP request handler for all API calls. It handles
        successful responses (200), validation errors (422), and other errors.
        
        Args:
            url (str): Complete URL to request
            use_cache (bool): Whether to use caching (default: True)
            
        Returns:
            dict: JSON response data if successful (status 200)
            str: 'break' if validation error (status 422)
            bool: False if other error occurred
        """
        
        # Use cached API client if enabled
        if self.cache_enabled and self.api_client and use_cache:
            try:
                return self.api_client.get(url, timeout=30)
            except Exception as e:
                logger.warning(f"Cached request failed, trying without cache: {e}")
                # Fall back to direct request
                pass
        
        # Direct request without cache
        try:
            req = requests.get(url, timeout=30)
            if req.status_code == 200:
                return req.json()
            elif req.status_code == 422:
                try:
                    error_detail = req.json().get('errors', [{}])[0].get('detail', req.text)
                    logger.error(f"Validation Error (422): {error_detail}")
                except Exception:
                    logger.error(f"Validation Error (422): {req.text}")
                return 'break'
            elif req.status_code == 406:
                logger.error(f"Not Acceptable (406): This is likely due to bot detection. Try updating headers.")
                return False
            else:
                logger.warning(f"Request failed with status {req.status_code}: {req.text}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error occurred: {str(e)}")
            return False

    def getLocations(self, lat=None, long=None):
        """
        Retrieve all dispensary/delivery locations for the current search slug.
        """
        if not self.searchSlug:
            logger.error("No search slug provided! Use -go <slug> or specify a slug.")
            return

        while True:
            # Construct the paginated API URL with current offset
            url = f'{self.baseUrl}?offset={str(self.locationsFound)}{self.pageSize}'

            # Add filters based on user selection or defaults
            if self.storefronts:
                url += f'&filter[any_retailer_services][]=storefront&filter[region_slug[dispensaries]]={self.searchSlug}'

            if self.deliveries:
                url += f'&filter[any_retailer_services][]=delivery&filter[region_slug[deliveries]]={self.searchSlug}'

            # Execute the request
            locations = self.do_request(url)

            if locations:
                if locations == 'break':
                    break
                
                # First response sets the total expected result count
                if self.maxLocations is None:
                    self.maxLocations = locations['meta']['total_listings']
                    logger.info(f"Set the max locations # to {self.maxLocations}")

                if self.maxLocations == 0:
                        logger.warning(f"Found no locations for the state: {self.searchSlug}")
                        if self.searchSlug:
                            self.unFriendlyStates.append(self.searchSlug)
                        self.NonGreenState = True
                        break

                logger.info(f'Working on locations #{self.locationsFound} through #{self.locationsFound+len(locations["data"]["listings"])}')

                for location in locations['data']['listings']:
                    self.locations.append({
                        'slug': location['slug'],
                        'type': location['type']
                    })
                    self.locationsFound += 1

                if self.maxLocations is not None and self.locationsFound >= self.maxLocations:
                    logger.info('Retrieved all locations! Moving to pull Menus')
                    break
            else:
                retry = input('Issue with Page. Retry? (n/no or hit enter)\n\n- ').lower()
                if 'n' in retry:
                    self.NonGreenState = True
                    break

    def getMenus(self):
        """
        Fetch and process menu data for all retrieved locations.
        """
        if self.NonGreenState:
            return

        # Check if we should use concurrent processing
        use_concurrent = os.getenv('USE_CONCURRENT_PROCESSING', 'false').lower() == 'true'
        
        if use_concurrent:
            self._getMenusConcurrent()
        else:
            self._getMenusSequential()

    def _getMenusSequential(self):
        """Original sequential menu fetching implementation"""
        for i, location in enumerate(self.locations):
            location_slug = location["slug"]
            location_type = location["type"]
            finished = False

            while not finished:
                try:
                    url = f'https://weedmaps.com/api/web/v1/listings/{location_slug}/menu?type={location_type}'
                    logger.info(f"Processing menu ({i+1}/{len(self.locations)}) --> {location_slug}")
                    
                    if self.testMode:
                        logger.debug(f"Menu URL: {url}")

                    resp = requests.get(url, timeout=30)
                    if resp.status_code == 503:
                        logger.warning(f"503 Service Unavailable for {location_slug}. Skipping.")
                        finished = True
                        break

                    if resp.status_code == 200:
                        self.process_menu_json(resp.json())
                        finished = True
                    else:
                        logger.error(f"Failed to fetch menu for {location_slug}: {resp.status_code}")
                        skip = input("Press enter to retry or type 'skip': ").lower()
                        if 'skip' in skip:
                            finished = True
                except Exception as e:
                    logger.error(f"Error processing {location_slug}: {str(e)}")
                    skip = input("Press enter to retry or type 'skip': ").lower()
                    if 'skip' in skip:
                        finished = True

        logger.info("Finished gathering menus. Organizing for export...")
        self.organize_into_clean_list()

    def _getMenusConcurrent(self):
        """Concurrent menu fetching implementation"""
        logger.info(f"Processing {len(self.locations)} locations concurrently...")
        
        # Create processor with configuration from environment or defaults
        max_workers = int(os.getenv('MAX_WORKERS', self.max_workers))
        rate_limit = float(os.getenv('RATE_LIMIT', self.rate_limit))
        
        processor = ConcurrentMenuProcessor(max_workers=max_workers, rate_limit=rate_limit)
        
        # Define the processing function for a single location
        def process_location_menu(location):
            return self._fetch_and_process_menu(location)
        
        # Process all locations concurrently
        results = processor.process_locations(self.locations, process_location_menu)
        
        # Update instance variables with results
        # The _fetch_and_process_menu method already updates self.allMenuItems
        logger.info("Finished gathering menus. Organizing for export...")
        self.organize_into_clean_list()
        
        # Log any errors that occurred
        if processor.errors:
            logger.warning(f"Encountered {len(processor.errors)} errors during processing")
            for error in processor.errors[:5]:  # Log first 5 errors
                logger.warning(f"Error for {error['location']['slug']}: {error['error']}")

    def _fetch_and_process_menu(self, location: Dict[str, Any]) -> bool:
        """Fetch and process menu for a single location"""
        location_slug = location["slug"]
        location_type = location["type"]
        
        try:
            url = f'https://weedmaps.com/api/web/v1/listings/{location_slug}/menu?type={location_type}'
            
            if self.testMode:
                logger.debug(f"Menu URL: {url}")
            
            resp = requests.get(url, timeout=30)
            
            if resp.status_code == 503:
                logger.warning(f"503 Service Unavailable for {location_slug}. Skipping.")
                return False
            
            if resp.status_code == 200:
                # Process the menu data using the existing method
                self.process_menu_json(resp.json())
                return True
            else:
                logger.error(f"Failed to fetch menu for {location_slug}: {resp.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error processing {location_slug}: {str(e)}")
            return False

    def getBrands(self):
        """
        Retrieve all brands from Weedmaps discovery API.
        """
        offset: int = 0
        while True:
            url = f'{self.brandsBaseUrl}?offset={str(offset)}{self.pageSize}'
            logger.info(f"Fetching brands (offset: {offset})...")
            
            data = self.do_request(url)
            if data and data != 'break':
                brands_list = data.get('data', {}).get('brands', [])
                if not brands_list:
                    break
                
                for brand in brands_list:
                    self.brands.append(brand)
                    self.brandsFound += 1
                
                total_brands = data.get('meta', {}).get('total_brands', 0)
                if self.brandsFound >= total_brands:
                    break
                offset += len(brands_list)
            else:
                break
        logger.info(f"Retrieved {self.brandsFound} brands.")

    def getStrains(self):
        """
        Retrieve all strains from Weedmaps discovery API.
        NOTE: This endpoint is currently unreliable (often 404/406).
        Consider using extracted menu strain data instead.
        """
        logger.warning("Global Strains endpoint is currently unreliable. Proceeding with attempt, but menu-based extraction is recommended.")
        offset: int = 0
        while True:
            url = f'{self.strainsBaseUrl}?offset={str(offset)}{self.pageSize}'
            logger.info(f"Fetching strains (offset: {offset})...")
            
            data = self.do_request(url)
            if data and data != 'break':
                strains_list = data.get('data', {}).get('strains', [])
                if not strains_list:
                    # Try alternate key if 'strains' not found
                    strains_list = data.get('data', {}).get('taxonomy', {}).get('strains', [])
                    if not strains_list:
                        break
                
                for strain in strains_list:
                    self.strains.append(strain)
                    self.strainsFound += 1
                
                total_strains = data.get('meta', {}).get('total_strains', 0)
                if self.strainsFound >= total_strains or total_strains == 0:
                    break
                offset += len(strains_list)
            else:
                # If 404, we might be using the wrong version/path for strains
                logger.warning(f"Could not fetch strains from {url}. Status might be 404 or restricted.")
                break
        logger.info(f"Retrieved {self.strainsFound} strains.")

    def process_menu_json(self, menu_json):
        """
        Process the JSON response for a single location's menu.
        """
        listing = menu_json.get('listing', {})
        listing_id = listing.get('id')
        listing_slug = listing.get('slug')
        listing_type = 'deliveries' if listing.get('_type') == 'delivery' else 'dispensaries'
        listing_url = f'/{listing_type}/{listing_slug}'
        
        categories = menu_json.get('categories', [])
        menu_items_count = 0

        self.allMenuItems[listing_id] = []

        if not categories:
            logger.info(f"Location {listing_slug} has no categories.")
            self.emptyMenus[listing_id] = listing
        else:
            for category in categories:
                for item in category.get('items', []):
                    item.update({
                        'locations_found_at': [listing_url],
                        'listing_id': listing_id,
                        'listing_wmid': listing.get('wmid')
                    })
                    
                    # Extract strain data if present
                    if 'strain_data' in item:
                        strain = item['strain_data']
                        slug = strain.get('slug')
                        if slug and slug not in self.extractedStrains:
                            self.extractedStrains[slug] = strain
                    elif 'strain' in item:
                        # Sometimes it's just 'strain' and might be a dict or ID
                        strain = item['strain']
                        if isinstance(strain, dict):
                            slug = strain.get('slug')
                            if slug and slug not in self.extractedStrains:
                                self.extractedStrains[slug] = strain

                    self.allMenuItems[listing_id].append(item)
                    menu_items_count += 1
                    self.menuItemsFound += 1

        listing['num_menu_items'] = str(menu_items_count)
        self.totalLocations.append(listing)
        logger.info(f"Processed {menu_items_count} items for {listing_slug}")

    def getLeaflyData(self):
        """
        Fetch data from Leafly using the Apify Scraper.
        """
        if not self.searchSlug:
            logger.error("No search slug provided for Leafly!")
            return

        logger.info(f"Starting Leafly integration for: {self.searchSlug}")
        leafly_items = scrape_leafly(self.searchSlug)
        
        if leafly_items:
            # Map Leafly items to our structure
            # Since Apify returns a list of items, we'll group them by a dummy ID or store ID if present
            self.allMenuItems['leafly_export'] = leafly_items
            self.menuItemsFound = len(leafly_items)
            logger.info(f"Successfully integrated {self.menuItemsFound} Leafly items.")
        else:
            logger.warning("No data retrieved from Leafly.")

    def getCannMenusData(self):
        """
        Fetch data from CannMenus using their official API.
        """
        slug = self.searchSlug
        if not slug or not isinstance(slug, str):
            logger.error("No valid search slug provided for CannMenus!")
            return

        logger.info(f"Starting CannMenus integration for state: {slug}")
        client = CannMenusClient()
        
        # CannMenus uses 2-letter state codes usually, let's assume slug might be one or we need to map it
        # For now, we'll try to pass the slug directly
        # Since we check self.searchSlug above, this is safe, but explicit check 
        # avoids linting issues.
        search_term = slug.upper()
        if not search_term:
            logger.error("No valid search term for CannMenus.")
            return

        retailers = client.get_retailers(search_term)
        
        if not retailers:
            logger.warning(f"No retailers found on CannMenus for: {self.searchSlug}")
            return

        for shop in retailers:
            shop_id = shop.get('id')
            shop_name = shop.get('name')
            logger.info(f"Fetching menu for {shop_name} from CannMenus...")
            menu = client.get_menu(shop_id)
            
            if menu:
                self.allMenuItems[shop_id] = menu
                self.menuItemsFound += len(menu)
                # Mock a listing entry for totalLocations
                self.totalLocations.append(shop)
        
        logger.info(f"Finished CannMenus integration. Total items: {self.menuItemsFound}")

    def getSourceData(self, source_name: str):
        """
        Fetch data from any registered pluggable data source.

        This method uses the DataSourceManager to dispatch to the correct
        adapter (API client or scraper) based on *source_name*.  It stores
        the results in the same internal structures that getMenus() and
        getCannMenusData() use, so the downstream CSV export works unchanged.

        Args:
            source_name (str): Registered adapter name (e.g. "cannmenus", "leafly").
        """
        slug = self.searchSlug
        if not slug:
            logger.error("No search slug provided for source '%s'!", source_name)
            return

        if source_name not in self.source_manager:
            available = [s["name"] for s in self.source_manager.list_sources()]
            logger.error(
                "Source '%s' is not registered. Available: %s",
                source_name, ", ".join(available) or "(none)",
            )
            return

        logger.info("Fetching data via pluggable source '%s' for slug=%s", source_name, slug)
        try:
            result = self.source_manager.fetch(source_name, slug)
        except Exception as exc:
            logger.error("Source '%s' failed: %s", source_name, exc)
            return

        # Merge results into CanaData's internal structures
        for loc_id, items in result.get("menus", {}).items():
            self.allMenuItems[loc_id] = items
            self.menuItemsFound += len(items)

        for loc in result.get("locations", []):
            self.totalLocations.append(loc)

        logger.info(
            "Source '%s' integration complete: %d locations, %d items",
            source_name, len(result.get("locations", [])), result.get("total_items", 0),
        )

    def organize_into_clean_list(self):
        """
        Flatten nested menu item dictionaries into uniform CSV-ready format.
        
        This method transforms the hierarchical menu data structure into a flat
        list of dictionaries where:
        1. All nested keys are flattened with dot notation (e.g., 'price.amount')
        2. All items have the same set of keys (missing keys filled with 'None')
        3. All values are converted to strings for CSV compatibility
        
        Process:
            1. Flatten each menu item dictionary using flatten_dictionary()
            2. Collect all unique keys across all items
            3. Create uniform dictionaries with all keys present
            4. Fill missing keys with 'None' value
            
        Side Effects:
            - Updates self.finishedMenuItems with flattened, uniform data
            
        Example:
            Input:  {'name': 'Product', 'price': {'amount': 10}}
            Output: {'name': 'Product', 'price.amount': '10'}
        """
        # Use optimized data processor if enabled
        if self.optimize_processing and self.data_processor:
            logger.info("Using optimized data processing pipeline")
            self.finishedMenuItems = self.data_processor.process_menu_data(self.allMenuItems)
        else:
            # Fall back to original method
            logger.info("Using original data processing method")
            self._original_organize_into_clean_list()
    
    def _original_organize_into_clean_list(self):
        """
        Original data organization method for backward compatibility.
        """
        # Grab the data from allMenuItems
        listings = self.allMenuItems

        # This is where our flat datasets will reside once finished
        flatDictList = []

        # Loop through the Listings
        for listing in listings:
            # Loop through the menu item Dictionaries for each listings
            for item in listings[listing]:
                # Flatten the dataset for each item
                flatData = self.flatten_dictionary(item)
                # Add the flat dataset to our flatDictList
                flatDictList.append(flatData)

        # This set will collect all possible keys
        all_keys_set = set()
        for item in flatDictList:
            all_keys_set.update(item.keys())
        
        all_keys = sorted(list(all_keys_set))

        # This list will house all data after each key has been filled out
        ready_list = []

        # Loop through the flatDictList to update any missing keys
        for item in flatDictList:
            # Create a dictionary with all keys initialized to 'None'
            flat_ordered_dict = {key: 'None' for key in all_keys}
            # Update with actual values, converting to string
            for key, value in item.items():
                flat_ordered_dict[key] = str(value)
            
            ready_list.append(flat_ordered_dict)

        # Replace our finished menu items list with our flat, ordered, dictionary list
        self.finishedMenuItems = ready_list

    def flatten_dictionary(self, d):
        """
        Recursively flatten a nested dictionary using dot notation for keys.
        
        This is a custom iterative implementation using a stack-based approach
        to handle arbitrarily nested dictionaries and lists. It converts:
        - Nested dicts: {'a': {'b': 'c'}} → {'a.b': 'c'}
        - Lists of dicts: {'a': [{'b': 'c'}]} → {'a.b': 'c'}
        - Lists of strings: {'a': ['x', 'y']} → {'a': 'x.y'}
        - Empty values: {'a': []} → {'a': 'None'}
        
        Args:
            d (dict): Nested dictionary to flatten
            
        Returns:
            dict: Flattened dictionary with dot-notation keys and string values
            
        Algorithm:
            Uses a stack to track nested levels and a keys list to build
            dot-notation paths. Handles lists, dicts, and primitive values
            with special logic for empty containers.
        """
        # Custom iterative implementation using a stack to handle recursion without recursion depth issues
        result = {}
        stack = [iter(d.items())] # Stack contains iterators of dictionary items
        keys = []                 # Tracks the current path in the dictionary (e.g., ['price', 'amount'])
        while stack:
            for k, v in stack[-1]:
                keys.append(k)
                if isinstance(v, list):
                    # Handle lists: if it's a list of dicts, go deeper; if primitives, join them
                    if len(v) > 0:
                        for item in v:
                            if item:
                                if isinstance(item, dict):
                                    if len(item.keys()) < 1:
                                        result['.'.join(keys)] = 'None'
                                    else:
                                        # Push the nested dict onto the stack
                                        stack.append(iter(item.items()))
                                elif isinstance(item, list):
                                    # Fallback for nested lists (semi-unsupported)
                                    result['.'.join(keys)] = '.'.join(item)
                                    keys.pop()
                                else:
                                    # Primitives in a list are joined by dot notation
                                    result['.'.join(keys)] = ''.join(str(v))
                                    keys.pop()
                                    break
                        break
                    else:
                        result['.'.join(keys)] = 'None'
                        keys.pop()
                elif isinstance(v, dict):
                    # Handle nested dictionaries
                    if len(v.keys()) < 1:
                        result['.'.join(keys)] = 'None'
                        keys.pop()
                    else:
                        # Push the nested dict onto the stack
                        stack.append(iter(v.items()))
                        break
                else:
                    # Leaf node: Store the value as a string
                    result['.'.join(keys)] = str(v)
                    keys.pop()
            else:
                # Finished processing an iterator: pop the path segment and the iterator itself
                if keys:
                    keys.pop()
                stack.pop()
        return result

    # Function recieves a city name and sets to searchSlug
    def setCitySlug(self, search):
        # Set searchSlug to City/State provided
        self.searchSlug = search

    def csv_maker(self, filename, data, preorganized=False):
        """
        Export a list of dictionaries to a CSV file with timestamp.
        
        Creates a dated folder (CanaData_MM-DD-YYYY) and writes the data
        to a CSV file with headers from the first dictionary's keys.
        
        Args:
            filename (str): Base name for the CSV file (without extension)
            data (list): List of dictionaries with uniform keys
            preorganized (bool): Unused parameter (legacy)
            
        Side Effects:
            - Creates CanaData_[date] folder if it doesn't exist
            - Writes CSV file to that folder
            - Prints success message with item count
            
        File Format:
            - First row: column headers (dictionary keys)
            - Subsequent rows: dictionary values in same order
            - UTF-8 encoding for special characters
        """
        today = datetime.today().strftime('%m-%d-%Y')
        # Variable on where to save the file
        home_dir = f'{path[0]}/CanaData_{today}'

        # Check if the folder exists
        if not ospath.exists(home_dir):
            # If not exist, create
            makedirs(home_dir)

        # Create CSV file as outfile
        with open(f'{home_dir}/{filename}.csv', 'w', newline='', encoding='utf-8') as outfile:
            # Setup csv writer with file
            output = csv.writer(outfile)

            # Row 1 Keys = first item in list's keys
            all_keys = list(data[0].keys())

            # Write row of keys
            output.writerow(all_keys)

            # Loop through the dataset
            for row in data:
                # Write row of item's values
                output.writerow(row.values())

            # Print visual notification of finished export & number of items seen
            print(f'Successfully exported ({str(len(data))} items) to CSV -> {filename}.csv')

    def dataToCSV(self):
        """
        Main entry point for triggering CSV generation.
        
        This method decides whether to export data based on the current state
        (NonGreenState) and attempts to export both the detailed menu items 
        and the high-level listing information.
        
        Side Effects:
            - Calls csv_maker twice (if data exists)
            - Prints summary statistics to the console
        """
        # If the state was not friendly for listings, skip making CSV
        if self.NonGreenState is True:
            return

        # Attempt detailed results export
        try:
            self.csv_maker(f'{self.searchSlug}_results', self.finishedMenuItems)
        except Exception as e:
            print(f'Error: {str(e)}')
            print('^^ Probably were no actual items (if error says \'list index out of range\')')

        # Attempt high-level listings export
        try:
            self.csv_maker(f'{self.searchSlug}_total_listings', self.totalLocations)
        except Exception as e:
            print(f'Error: {str(e)}')
            print('^^ Musta been a bad search query? (if error says \'list index out of range\')')

        # Attempt Brands export
        if self.brands:
            try:
                self.csv_maker('all_brands', self.brands)
            except Exception as e:
                print(f'Error exporting brands: {str(e)}')

        # Attempt Strains export
        if self.strains:
            try:
                self.csv_maker('all_strains', self.strains)
            except Exception as e:
                print(f'Error exporting strains: {str(e)}')

        # Attempt Extracted Strains export (Menu-based)
        if self.extractedStrains:
            try:
                # Convert dict values to list for CSV
                extracted_list = list(self.extractedStrains.values())
                # Use current search slug in filename if available
                filename = f'{self.searchSlug}_extracted_strains' if self.searchSlug else 'extracted_strains'
                self.csv_maker(filename, extracted_list)
                print(f'- Exported {len(extracted_list)} unique strains found in menus.')
            except Exception as e:
                print(f'Error exporting extracted strains: {str(e)}')

        print(f'\n\nResults for -> {self.searchSlug}:\n- {str(self.locationsFound)} Locations\n- {str(len(self.allMenuItems.keys()))} Menus\n- {str(len(self.emptyMenus.keys()))} Empty Menus\n- {str(self.menuItemsFound)} Menu Items')

    def resetDataSets(self):
        """
        Reset stateful attributes before processing the next search slug.
        
        Crucial for the "all" or "mylist" modes to ensure data from one 
        state doesn't bleed into the next one.
        """
        # Reset identifiers and counters
        self.searchSlug = None
        self.locationsFound = 0
        self.maxLocations = None
        
        # Clear data collections
        self.locations = []
        self.allMenuItems = {}
        self.finishedMenuItems = []
        self.totalLocations = []
        
        # We don't reset brands and strains here as they are global metadata
        # potentially fetched once per run.
        
        # Reset status flags
        self.NonGreenState = False
        self.extractedStrains = {}


    def identifyNaughtyStates(self):
        """
        Print a summary of slugs that returned no results.
        """
        if len(self.unFriendlyStates) > 0:
            # Ensure all items are strings
            slugs = [str(s) for s in self.unFriendlyStates]
            print(f'\nThese States were found to have 0 listings!\n{", ".join(slugs)}')

    def identifyDataTypes(self):
        """
        Interactive prompt to toggle storefront vs delivery scraping.
        """
        # Default is True for both; user can opt-out here
        dispensaryChoice = input('\n\nAre we pulling Dispensary Info? (No/n or hit enter for yes)\n\n--').lower()
        if 'n' in dispensaryChoice or 'no' in dispensaryChoice:
            self.storefronts = False

        deliveriesChoice = input('\n\nAre we pulling Deliveries Info? (No/N or hit enter for yes)\n\n--').lower()
        if 'n' in deliveriesChoice or 'no' in deliveriesChoice:
            self.deliveries = False

    def slugs(self):
        """
        Enable slug recording mode (unused in current main loop).
        """
        print('Set slugGrab to true!')
        self.slugGrab = True

    def TestMode(self):
        """
        Enable troubleshooting mode for more verbose output.
        """
        print('Set Troubleshooting Mode to True')
        self.testMode = True


if __name__ == '__main__':
    # Initiate the Library
    cana = CanaData()

    # This is where we end pu putting our list of items. Replaced with a list of search slugs -> []
    searchSlugs = None

    try:
        # Grab list of States from local file
        allStatesSlugs = [line.rstrip('\n').lower().replace(' ', '-') for line in open('states.txt')]  # Updated by Manually through magic
    except Exception as e:
        print('Looks like no states.txt file! No biggy, just cant use the all option!')

    try:
        # Grab list of known Cities from local file
        knownSlugs = [line.rstrip('\n').lower().replace(' ', '-') for line in open('slugs.txt')]
    except Exception as e:
        print('Looks like no slugs.txt file! No biggy, just cant use the slugs option!')

    try:
        # Grab list of known Cities from local file
        mySlugList = [line.rstrip('\n').lower().replace(' ', '-') for line in open('mylist.txt')]  # Updated by Manually through magic
    except Exception as e:
        print('Looks like no mylist.txt file! No biggy, just cant use the mylist option!')

    # Argument list
    argList = list(argv)

    if '-tshoot' in argList:
        cana.TestMode()

    # Check if arguments were passed
    if len(argList) > 1:
        # There were arguments! Now to check for specifics

        # This looks to see if we need to save the City list that we identify!
        if '-slugs' in argList:
            cana.slugs()

    # This specifically looks for the quick run argument and sets the State list
    if '-go' in argList:
        # Search slug location in args is after the -go
        searchSlug = argList.index('-go') + 1
        # Determine if its one of our preset 3 or a regular search
        if argv[searchSlug].lower() == 'mylist':
            searchSlugs = mySlugList
        elif argv[searchSlug].lower() == 'slugs':
            # Slug list is set to the list from the cities.txt file
            searchSlugs = knownSlugs
        elif argv[searchSlug].lower() == 'all':
            # Slug list is set to the list from the cities.txt file
            searchSlugs = allStatesSlugs
        else:
            searchSlugs = [argv[searchSlug].lower()]
        # Visual queue of start (in place of question for search slug)
        print(f'\n\n   !!~~-- Welcome to CanaData  (>-_-)>  --~~!!\n\n\n\nStarting Quickrun on {str(len(searchSlugs))} Slugs: \n{str(", ".join(searchSlugs))}\n\n\n')

    # If user is not doing Quickrun
    # Ask them for a slug then determine if its one of our preset 3 or a regular search
    else:
        # Ask the user for what City they'd like to run
        answer = input(f'\n\n   !!~~-- Welcome to CanaData  (>-_-)>  --~~!!\n\nWhat city slug or state slug would you like to search? Can put all for all states or mylist for your custom list or slugs for the list of custom slugs from slugs.txt!\n\nOptions:\n- Use -go <slug> for quick run\n- Use -leafly with a slug for Leafly data\n- Use -cannmenus with a state code for CannMenus data\n\nKnown State Options:\n{", ".join(allStatesSlugs)}\n\nKnown Slug Options:\n{", ".join(knownSlugs)}\n\nKnown Mylist Options:\n{", ".join(mySlugList)}\n\n-- ').lower()

        # Check if user asked for all
        if answer == 'all':
            # States list is set to our 50 state list # Fingers crossed it runs through all!
            searchSlugs = allStatesSlugs
        elif answer == 'mylist':
            # States list is set to the list from the myList.txt file
            searchSlugs = mySlugList
        elif answer == 'slugs':
            # Slug list is set to the list from the cities.txt file
            searchSlugs = knownSlugs
        else:
            # State list is set to a single item list of what the user input
            searchSlugs = [answer]

    # This Loop fires no matter what to process all search slugs provided either manually or through a .txt file!
    # Fun functions against them all!
    
    # Global data fetch (if requested)
    if '-brands' in argList:
        cana.getBrands()
    if '-strains' in argList:
        cana.getStrains()

    for slug in searchSlugs:
        if len(slug) > 0:
            # Visual queue of starting a state
            print(f'\n\nStarting on {slug}')
            # Set our searchSlug to the State we are working on
            cana.setCitySlug(slug)
            
            # Skip location/menu scraping if only fetching global metadata
            if '-brands' in argList or '-strains' in argList:
                if not any(arg in argList for arg in ['-go', 'all', 'mylist', 'slugs']) and len(searchSlugs) == 1 and str(searchSlugs[0]) == str(answer if 'answer' in locals() else None):
                     # If user just typed something but also wants brands/strains, maybe they want both
                     pass

            if '-source' in argList:
                # Generic pluggable source: -source <name>
                source_idx = argList.index('-source') + 1
                if source_idx < len(argList):
                    cana.getSourceData(argList[source_idx])
                else:
                    print('Error: -source requires a source name argument')
                    print(f'Available: {[s["name"] for s in cana.source_manager.list_sources()]}')
            elif '-leafly' in argList:
                cana.getLeaflyData()
            elif '-cannmenus' in argList:
                cana.getCannMenusData()
            else:
                # Default to Weedmaps
                # Get the locations for the given slug
                cana.getLocations()
                # Get the Menus for the locations found
                cana.getMenus()
            
            # Convert our Datasets to CSV's (1 for Menu Items & 1 for Listing Info)
            cana.dataToCSV()
            # Reset the self variables to avoid using old data from other states/slugs
            cana.resetDataSets()
    # Print out the list of Non-Cannabis friendly states
    cana.identifyNaughtyStates()
