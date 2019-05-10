#!/usr/bin/python3
from os import path as ospath
from os import makedirs
from sys import path
import requests
import json
import csv


class WeedMapper:
    def __init__(self):
        self.test = True
        self.baseUrl = 'https://api-g.weedmaps.com/wm/v2/listings'
        self.pageSize = '&page_size=100&size=100'
        self.citySlug = None
        self.storefronts = False
        self.deliveries = False
        self.locationsFound = 0
        self.maxLocations = None
        self.locations = {}
        self.allMenuItems = []
        self.finishedMenuItems = []
        self.finishedLocations = []
        self.unFriendlyStates = []
        self.NonGreenState = False

    def do_request(self, url):
        req = requests.get(url)
        if req.status_code == 200:
            reqJson = req.json()
            return reqJson
        else:
            print(req.text)
            return False

    def getLocations(self, lat=None, long=None):
        while True:
            url = f'{self.baseUrl}?offset={str(self.locationsFound)}&{self.pageSize}'

            if self.storefronts is True:
                url += f'&filter[plural_types][]=dispensaries&filter[region_slug[dispensaries]]={self.citySlug}'

            if self.deliveries is True:
                url += f'&filter[plural_types][]=deliveries&filter[region_slug[deliveries]]={self.citySlug}'

            locations = self.do_request(url)

            if locations is not False:

                if self.maxLocations is None:
                    self.maxLocations = locations['meta']['total_listings']
                    print(f'\nSet the max locations # to {self.maxLocations}')

                    if self.maxLocations == 0:
                        print('Found no locations for the state (sad times)!')
                        self.unFriendlyStates.append(self.citySlug)
                        self.NonGreenState = True
                        break

                print(f'Working on locations #{self.locationsFound} through #{self.locationsFound+len(locations["data"]["listings"])}')

                for location in locations['data']['listings']:
                    self.locations[location['slug']] = location['type']
                    self.locationsFound += 1

                if self.locationsFound == self.maxLocations:
                    print('Retrieved all locations! Moving to pull Menus\n')
                    break

            else:
                retry = input('Issue with Page. Retry? (n/no or hit enter)\n\n- ').lower()

                if 'n' in retry or 'no' in retry:
                    self.NonGreenState = True
                    break
                else:
                    self.do_request(url)

    def getMenus(self):
        if self.NonGreenState is True:
            return
        for location in self.locations:
            url = f'https://weedmaps.com/api/web/v1/listings/{location}/menu?type={self.locations[location]}'

            menuData = requests.get(url)

            if menuData.status_code == 200:
                menuJsonData = menuData.json()

                self.finishedLocations.append(menuJsonData['listing'])
                print(f'Working on the menu for {menuJsonData["listing"]["name"]}')

                for menuItemCategory in menuJsonData['categories']:
                    for menuItem in menuItemCategory['items']:
                        self.allMenuItems.append(menuItem)
        self.organize_into_clean_list()

    def organize_into_clean_list(self):
        data = self.allMenuItems

        flatDictList = []

        for item in data:
            flatData = self.flatten_dictionary(item)
            flatDictList.append(flatData)

        all_keys = []
        ready_list = []

        for item in flatDictList:
            for key in item.keys():
                if key not in all_keys:
                    all_keys.append(key)

        for item in flatDictList:
            flat_ordered_dict = {}
            current_keys = list(item.keys())
            for all_key in all_keys:
                if all_key in current_keys:
                    flat_ordered_dict[all_key] = item[all_key]
                else:
                    flat_ordered_dict[all_key] = 'None'

            ready_list.append(flat_ordered_dict)

        self.finishedMenuItems = ready_list

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

    def csv_maker(self, filename, data, preorganized=False):
        file_name = filename
        home_dir = f'{path[0]}/MapperResults'
        if not ospath.exists(home_dir):
            makedirs(home_dir)

        ready_info = data

        with open(f'{home_dir}/{file_name}.csv', 'w') as outfile:
            output = csv.writer(outfile)

            all_keys = list(ready_info[0].keys())

            output.writerow(all_keys)
            for row in ready_info:
                output.writerow(row.values())
            print(f'\033[92mSuccessfully exported ({str(len(data))} items) to CSV -> {file_name}.csv \033[0m')

    def setCitySlug(self, city):
        self.citySlug = city

    def dataToCSV(self):
        if self.NonGreenState is True:
            return
        try:
            self.csv_maker(f'{self.citySlug}_results', self.finishedMenuItems)
        except Exception as e:
            print(e)
            print('Probably were no actual items.. Heres a visual conformation though!:\n', json.dumps(self.finishedMenuItems, indent=3))
        self.csv_maker(f'{self.citySlug}_total_listings', self.finishedLocations)

    def resetDataSets(self):
        self.citySlug = None
        self.locationsFound = 0
        self.maxLocations = None
        self.locations = {}
        self.allMenuItems = []
        self.finishedMenuItems = []
        self.finishedLocations = []
        self.NonGreenState = False

    def identifyNaughtyStates(self):
        print(f'\nThese States were found to have 0 listings!\n{", ".join(self.unFriendlyStates)}')

    def identifyDataTypes(self):
        dispensaryChoice = input('\n\nAre we pulling Dispensary Info? (Yes/y or hit enter)\n\n--').lower()
        if 'y' in dispensaryChoice or 'yes' in dispensaryChoice:
            self.storefronts = True

        deliveriesChoice = input('\n\nAre we pulling Deliveries Info? (Yes/y or hit enter)\n\n--').lower()
        if 'y' in deliveriesChoice or 'yes' in dispensaryChoice:
            self.deliveries = True


if __name__ == '__main__':
    mapper = WeedMapper()

    allStates = [line.rstrip('\n').lower().replace(' ', '-') for line in open('states.txt')]

    city = input('\n\n   !!~~-- Welcome to CanaData  (>-_-)>  --~~!!\n\nWhat cityslug or state slug would you like to search? (Put all for all states)\n\nOptions:\n\n' + ', '.join(allStates) + '\n\n-- ')

    mapper.identifyDataTypes()

    if city == 'all':
        states = allStates
    else:
        states = [city]

    for state in states:
        print(f'\n\nStarting on \033[92m{state}\033[0m')
        mapper.resetDataSets()
        mapper.setCitySlug(state)
        mapper.getLocations()
        mapper.getMenus()
        mapper.dataToCSV()
        print('Finished with state!')
    mapper.identifyNaughtyStates()
