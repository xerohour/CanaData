from sys import argv
from CanaData import CanaData

if __name__ == '__main__':
    # Initiate the Library
    cana = CanaData()

    # This is where we end pu putting our list of items. Replaced with a list
    # of search slugs -> []
    searchSlugs = None

    try:
        # Grab list of States from local file
        allStatesSlugs = [line.rstrip('\n').lower().replace(
            ' ', '-') for line in open('states.txt')]  # Updated by Manually through magic
    except Exception:
        print('Looks like no states.txt file! No biggy, just cant use the all option!')

    try:
        # Grab list of known Cities from local file
        knownSlugs = [line.rstrip('\n').lower().replace(' ', '-')
                      for line in open('slugs.txt')]
    except Exception:
        print('Looks like no slugs.txt file! No biggy, just cant use the slugs option!')

    try:
        # Grab list of known Cities from local file
        mySlugList = [line.rstrip('\n').lower().replace(
            ' ', '-') for line in open('mylist.txt')]  # Updated by Manually through magic
    except Exception:
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

    # This specifically looks for the quick run argument and sets the State
    # list
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
        print(f'\n\n   !!~~-- Welcome to CanaData  (>-_-)>  --~~!!\n\n\n\nStarting Quickrun on {len(searchSlugs)} Slugs: \n{", ".join(searchSlugs)}\n\n\n')

    # If user is not doing Quickrun
    # Ask them for a slug then determine if its one of our preset 3 or a
    # regular search
    else:
        # Ask the user for what City they'd like to run
        answer = input(
            f'\n\n   !!~~-- Welcome to CanaData  (>-_-)>  --~~!!\n\nWhat city slug or state slug would you like to search? Can put all for all states or mylist for your custom list or slugs for the list of custom slugs from slugs.txt!\n\nOptions:\n- Use -go <slug> for quick run\n- Use -leafly with a slug for Leafly data\n- Use -cannmenus with a state code for CannMenus data\n\nKnown State Options:\n{
                ", ".join(allStatesSlugs)}\n\nKnown Slug Options:\n{
                ", ".join(knownSlugs)}\n\nKnown Mylist Options:\n{
                ", ".join(mySlugList)}\n\n-- ').lower()

        # Check if user asked for all
        if answer == 'all':
            # States list is set to our 50 state list # Fingers crossed it runs
            # through all!
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

    metadata_only = (
        ('-brands' in argList or '-strains' in argList)
        and '-leafly' not in argList
        and '-cannmenus' not in argList
    )

    if metadata_only:
        cana.setCitySlug('global')
        cana.dataToCSV()
        raise SystemExit(0)

    for slug in searchSlugs:
        if len(slug) > 0:
            # Visual queue of starting a state
            print(f'\n\nStarting on {slug}')
            # Set our searchSlug to the State we are working on
            cana.setCitySlug(slug)

            if '-leafly' in argList:
                cana.getLeaflyData()
            elif '-cannmenus' in argList:
                cana.getCannMenusData()
            else:
                # Default to Weedmaps
                # Get the locations for the given slug
                cana.getLocations()
                # Get the Menus for the locations found
                cana.getMenus()

            # Convert our Datasets to CSV's (1 for Menu Items & 1 for Listing
            # Info)
            cana.dataToCSV()
            # Reset the self variables to avoid using old data from other
            # states/slugs
            cana.resetDataSets()
    # Print out the list of Non-Cannabis friendly states
    cana.identifyNaughtyStates()
