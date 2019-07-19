#!/usr/bin/python3
from datetime import datetime
from os import path as ospath
from os import makedirs
from sys import path
from sys import argv
import requests
import json
import csv


# Low and behold, the almighty CanaData
class CanaData:
    def __init__(self):
        # Where the Magic happens
        self.baseUrl = 'https://api-g.weedmaps.com/discovery/v1/listings'
        # Pagination & Page size
        self.pageSize = '&page_size=100&size=100'
        # Populated with the City/State Slug
        self.searchSlug = None
        # Set to True if we are grabbing storefronts
        self.storefronts = True
        # Set to True if we are grabbing deliveries
        self.deliveries = True
        # Number of Locations found for searchSlug
        self.locationsFound = 0
        # Number of Items found
        self.menuItemsFound = 0
        # Number returned from Weedmaps as to Max # of locations
        self.maxLocations = None
        # Dataset of locations
        self.locations = []
        # Dictionary of Empty Location Menus
        self.emptyMenus = {}
        # Avoids duplicating items from deliveries using their Storefront Menus
        self.allMenuItems = {}
        # List of flattened menu items
        self.finishedMenuItems = []
        # List of total flattened locations
        self.totalLocations = []
        # List of States with No locations
        self.unFriendlyStates = []
        # Set to True if there are no locations
        self.NonGreenState = False
        # Sets whether or not we grab the slugs for the search
        self.slugGrab = False

    # This function recieves a URL (string) and makes an HTTP request to it
    # If successul, converts the response to JSON and returns the dataset
    def do_request(self, url):
        # Make the request to the URL (no authentication)
        req = requests.get(url)
        # If status was success
        if req.status_code == 200:
            # Convert dataset to JSON
            reqJson = req.json()
            # Return JSON dataset
            return reqJson
        elif req.status_code == 422:
            print(req.text)
            exit()
            return 'break'
        else:
            # Print the error into the terminal
            print(req.text)
            exit()
            # Return False to signal issues
            return False

    # This function takes no input but uses the self variables to make its requests
    # Looping through to get all Locations for a given City/State slug
    def getLocations(self, lat=None, long=None):
        # While true lets us loop until we have all data
        while True:
            # Create the url with Offset so to paginate to next set of data
            url = f'{self.baseUrl}?offset={str(self.locationsFound)}{self.pageSize}'

            # If we are returning storefronts our URL needs extra parameters
            if self.storefronts is True:
                url += f'&filter[any_retailer_services][]=storefront&filter[region_slug[dispensaries]]={self.searchSlug}'

            # If we are returning deliveries our URL needs extra parameters
            if self.deliveries is True:
                url += f'&filter[any_retailer_services][]=delivery&filter[region_slug[deliveries]]={self.searchSlug}'

            # Make the http request and get back either data or False
            locations = self.do_request(url)

            # Check if the request was successul or not
            if locations is not False:
                if locations == 'break':
                    break
                # If we haven't set our max # of locations, do so
                if self.maxLocations is None:
                    # Set self variable to the responses' total listing attribute
                    self.maxLocations = locations['meta']['total_listings']
                    # Print what we set the max at for visual checking
                    print(f'\nSet the max locations # to {self.maxLocations}')

                    # If the Max locations is 0, then we know we should stop going forward
                    if locations['meta']['total_listings'] == 0:
                        # Print that we found nothing
                        print('Found no locations for the state (sad times)!')
                        # Add the state to our list of un-green states
                        self.unFriendlyStates.append(self.searchSlug)
                        # Set our non green state attribute to True so it knows to stop processing this slug
                        self.NonGreenState = True
                        # Break out of the While true loop
                        break

                # Visual queue to how far along the script is
                print(f'Working on locations #{self.locationsFound} through #{self.locationsFound+len(locations["data"]["listings"])}')

                # Loop through the listings and pull out the slug and type
                for location in locations['data']['listings']:
                    location_dct = {}
                    location_dct['slug'] = location['slug']
                    location_dct['type'] = location['type']
                    self.locations.append(location_dct)

                    # Count the number of listings
                    self.locationsFound += 1

                # IF we've reached the max number of locations, we are finished so break
                if self.locationsFound == self.maxLocations:
                    print('\nRetrieved all locations! Moving to pull Menus\n')
                    break

            # If there is an issue pulling the data from the page, (potentially due to rate limiting), ask user to continue or not
            else:
                # User is prompted to enter no/n or hit enter to continue
                retry = input('Issue with Page. Retry? (n/no or hit enter)\n\n- ').lower()

                # If the user put "n" or "no" then we stop trying and put this slug into the list of bad states
                if 'n' in retry or 'no' in retry:
                    # Set NonGreenState to True to skip other functions when we get to them
                    self.NonGreenState = True
                    break
                # Otherwise we try again!
                else:
                    self.do_request(url)

    # This function goes through the list of locations and gets the menu + flattens the items
    def getMenus(self):
        # If the city/state slug is not friendly to Cannabis, skip them!
        if self.NonGreenState is True:
            return

        location_count = 0

        seen_locations = []

        # If the city/state slug is friendly, then loop through the listings one by one
        for location in self.locations:
            finished = False

            while finished is False:
                try:
                    # Craft a URL variable which pulls all menu items for a location
                    url = f'https://weedmaps.com/api/web/v1/listings/{location["slug"]}/menu?type={location["type"]}'

                    # Get the menu data from the URL
                    menuData = requests.get(url)

                    # If that was successful
                    if menuData.status_code == 200:
                        # Convert the menu data to JSON to work with
                        menuJsonData = menuData.json()

                        # Add to our count of Listing Progress
                        location_count += 1

                        # Clean dictionary to house the finished encoded items + reorganizes them all into right order
                        clean_listing = {}

                        # Integer to count # of menu items for listing
                        menu_items = 0

                        # Print visual queue the location is being worked on
                        print(f'\nWorking on menu ({str(location_count)}/{str(len(self.locations))}) --> {menuJsonData["listing"]["name"]}')

                        # Loop through values of the Listing Data (not menu items) to clean them with encoding!
                        for listingKey in menuJsonData['listing'].keys():
                            clean_listing[listingKey] = str(menuJsonData['listing'][listingKey]).encode('utf-8')

                        if len(menuJsonData["categories"]) == 0:
                            print('No Categories means no items, moving on!\nGrabbed the listing info though')
                            # Add the listing to our totalLocations list
                            self.totalLocations.append(menuJsonData['listing'])
                            # Dictionary of Empty Location Menus added to the EmptyMenus Dictionary
                            self.emptyMenus[menuJsonData["listing"]["id"]] = menuJsonData["listing"]
                            print(f'Added to Total Locations (empty menu)! {str(len(self.totalLocations))}')
                            finished = True
                            break
                        else:
                            # Print visual of how many Categories exist in this menu
                            print(f'There are {str(len(menuJsonData["categories"]))} Categories in the Menu!')

                        # Create a string representation of the Listing (this should be what each item refers to in listing_url)
                        if menuJsonData["listing"]["_type"] == 'delivery':
                            listing_type = 'deliveries'
                        elif menuJsonData["listing"]["_type"] == 'dispensary':
                            listing_type = 'dispensaries'
                        else:
                            print(menuJsonData['listing']['_type'])

                        listing_url = f'/{listing_type}/{menuJsonData["listing"]["slug"]}'
                        # print(f'-- The listing URL is: {listing_url}')

                        self.allMenuItems[menuJsonData["listing"]["id"]] = []

                        # Loop through each menu category
                        for menuItemCategory in menuJsonData['categories']:
                            for menuItem in menuItemCategory['items']:
                                menuItem['locations_found_at'] = [listing_url]
                                menuItem['listing_id'] = menuJsonData["listing"]["id"]
                                menuItem['listing_wmid'] = menuJsonData["listing"]["wmid"]
                                # Add the menu item to our allMenuItems dictionary
                                self.allMenuItems[menuJsonData["listing"]["id"]].append(menuItem)
                                menu_items += 1
                                self.menuItemsFound += 1

                        # Visual progress of Listing's items amount
                        finished_statement = f'#{str(menu_items)} Items in the Menu!'
                        if menu_items == 0:
                            finished_statement += '  <--- Will be on Listings CSV but no items on Menu Results!'
                        # print(finished_statement)

                        # Add # of menu items to listing Info!
                        menuJsonData['listing']['num_menu_items'] = str(menu_items)

                        # print(f'#{str(self.menuItemsFound)} Total Items Processed!!')

                        # Add the listing to our totalLocations list
                        self.totalLocations.append(menuJsonData['listing'])
                        print(f'Added to Total Locations (normal)! {str(len(self.totalLocations))}')

                        # print(f'#{str(len(self.allMenuItems.keys()))} Total Menus Processed!!')

                        finished = True

                except Exception as e:
                    print(e)
                    print(menuData.text)
                    input('Issue with menu retrival, see issue and hit Enter to retry or enter "Skip" to continue\n\n- ').lower()
                    continue
        print('\n\nFinished grabbing all the Menus & Items! \n\nOrganizing now into clean lists for export!\n(up to a couple minutes on those big exports (5k+) looking at you California)\n')
        # Special function to flatten all our Menu items!
        self.organize_into_clean_list()

    # This function loops through our identifed menu items and flattens them into exportable datasets
    def organize_into_clean_list(self):
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

        # This list will be all possible keys
        all_keys = []
        # This list will house all data after each key has been filled out if it wasn't present before
        ready_list = []

        # Loop through the flatDictList and grab all the keys
        for item in flatDictList:
            # for each key in each menu item dictionary
            for key in item.keys():
                # If we haven't grabbed the key already
                if key not in all_keys:
                    # Add the key to our all_keys list
                    all_keys.append(key)

        # Loop through the flatDictList to update any missing keys
        for item in flatDictList:
            # New dicitonary the dataset will be put into
            flat_ordered_dict = {}
            # List of current keys in the dictionary
            current_keys = list(item.keys())
            # Loop through the list of all_keys
            for all_key in all_keys:
                # if one of the all_keys is not present in this dicitonary's key list, add it with value
                if all_key in current_keys:
                    flat_ordered_dict[all_key] = str(item[all_key])
                # IF the key is not present in the dictionary's key list, add it with value as "None"
                else:
                    flat_ordered_dict[all_key] = 'None'
            # Add our ordered dict to the Ready List
            ready_list.append(flat_ordered_dict)

        # Replace our finished menu items list with our flat, ordered, dictionary list
        self.finishedMenuItems = ready_list

    # My special dictionary flattening function.
    # Magic is magic
    def flatten_dictionary(self, d):
        result = {}
        stack = [iter(d.items())]
        keys = []
        while stack:
            for k, v in stack[-1]:
                keys.append(k)
                if isinstance(v, list):
                    if len(v) > 0:
                        for item in v:
                            if item:
                                if isinstance(item, dict):
                                    if len(item.keys()) < 1:
                                        result['.'.join(keys)] = 'None'
                                    else:
                                        stack.append(iter(item.items()))
                                elif isinstance(item, list):
                                    result['.'.join(keys)] = '.'.join(item)
                                    keys.pop()
                                else:
                                    result['.'.join(keys)] = ''.join(str(v))
                                    keys.pop()
                                    break
                        break
                    else:
                        result['.'.join(keys)] = 'None'
                        keys.pop()
                elif isinstance(v, dict):
                    if len(v.keys()) < 1:
                        result['.'.join(keys)] = 'None'
                        keys.pop()
                    else:
                        stack.append(iter(v.items()))
                        break
                else:
                    result['.'.join(keys)] = str(v)
                    keys.pop()
            else:
                if keys:
                    keys.pop()
                stack.pop()
        return result

    # Function recieves a city name and sets to searchSlug
    def setCitySlug(self, search):
        # Set searchSlug to City/State provided
        self.searchSlug = search

    # Function recieves a filename & dataset (list of dictionaries)
    def csv_maker(self, filename, data, preorganized=False):
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

    # Function determines whether or not a CSV should be made
    def dataToCSV(self):
        # If the state was not friendly for listings, skip making CSV
        if self.NonGreenState is True:
            return

        # Try to make a CSV of the dataset, try because sometimes will fail if Locations exist with 0 menu items
        try:
            self.csv_maker(f'{self.searchSlug}_results', self.finishedMenuItems)
        except Exception as e:
            print(f'Error: {str(e)}')
            print('^^ Probably were no actual items (if error says \'list index out of range\')')

        # Listing dataset typically has values regardless of empty menus, turn that dataset into a CSV
        try:
            self.csv_maker(f'{self.searchSlug}_total_listings', self.totalLocations)
        except Exception as e:
            print(f'Error: {str(e)}')
            print('^^ Musta been a bad search query? (if error says \'list index out of range\')')

        print(f'\n\nResults for -> {self.searchSlug}:\n- {str(self.locationsFound)} Locations\n- {str(len(self.allMenuItems.keys()))} Menus\n- {str(len(self.emptyMenus.keys()))} Empty Menus\n- {str(self.menuItemsFound)} Menu Items')

    # Since we loop through states in the "All" option, we have to reset some values
    def resetDataSets(self):
        # Reset the search slug
        self.searchSlug = None
        # Reset the number of locations found
        self.locationsFound = 0
        # Reset the max number of locations
        self.maxLocations = None
        # Reset the locations dataset
        self.locations = []
        # Reset the list of Menu Items
        self.allMenuItems = {}
        # Reset the list of Finished Menu Items
        self.finishedMenuItems = []
        # Reset the list of Total Locations
        self.totalLocations = []
        # Reset the NonGreenState Status to False
        self.NonGreenState = False

    # Function to announce the # of non Cannabis friendly states (0 listings in state)
    def identifyNaughtyStates(self):
        if len(self.unFriendlyStates) > 0:
            print(f'\nThese States were found to have 0 listings!\n{", ".join(self.unFriendlyStates)}')

    # Function to determine if we are searching for Dispensary data or Delivery Data (can be both)
    def identifyDataTypes(self):
        # Ask the user to put y/yes or we wont search dispensaries
        dispensaryChoice = input('\n\nAre we pulling Dispensary Info? (No/n or hit enter for yes)\n\n--').lower()
        if 'n' in dispensaryChoice or 'no' in dispensaryChoice:
            # Set self value to False so dispensaries are included in datasets
            self.storefronts = False

        # Ask the user to put y/yes or we wont search deliveries
        deliveriesChoice = input('\n\nAre we pulling Deliveries Info? (No/N or hit enter for yes)\n\n--').lower()
        if 'n' in deliveriesChoice or 'no' in dispensaryChoice:
            # Set self value to False so deliveries are included in datasets
            self.deliveries = False

    # Sets the self attribute for grabbing slugs within a search
    def slugs(self):
        print('Set slugGrab to true!')
        self.slugGrab = True


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
        answer = input(f'\n\n   !!~~-- Welcome to CanaData  (>-_-)>  --~~!!\n\nWhat city slug or state slug would you like to search? Can put all for all states or mylist for your custom list or slugs for the list of custom slugs from slugs.txt!\n\nKnown State Options:\n{", ".join(allStatesSlugs)}\n\nKnown Slug Options:\n{", ".join(knownSlugs)}\n\nKnown Mylist Options:\n{", ".join(mySlugList)}\n\n-- ').lower()

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
    for slug in searchSlugs:
        if len(slug) > 0:
            # Visual queue of starting a state
            print(f'\n\nStarting on {slug}')
            # Set our searchSlug to the State we are working on
            cana.setCitySlug(slug)
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
