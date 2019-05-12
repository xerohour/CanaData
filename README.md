# CanaData


# Welcome to CanaData
Don's favorite tool to retrieve state/cities listing results from Weedmaps! (Yes you can try all 50 states two ways!)


## Discord to discuss:
https://discord.gg/6WAcVek

## Got an Example CURL request to show what endpoints are involved?
YUP! This example is for the lovely state of Washington DC as they don't have too many Locations so it's a smaller dataset. Feel free to changeout `washington-dc` to a lowercase version of your state (replace spaces with a dash if there is one `-`)
```
curl -g "https://api-g.weedmaps.com/discovery/v1/listings?filter[any_retailer_services][]=storefront&filter[any_retailer_services][]=delivery&filter[region_slug[deliveries]]=washington-dc&filter[region_slug[dispensaries]]=washington-dc&page_size=100&size=100"
```

## Why would I use this?
When I found that a single item by the same company can be sold at multiple locations at different prices, I was determined to find a way to put these dispensary and delivery services more in competition with each other. Stop leaving us consumers left out to dry when it comes to understanding where we should shop thats best for us.


## How do I use this?
- Go here, hover your mouse on Download and download python 3.X for your operating system -> https://www.python.org/


- Download this Repository into a folder (typically works best putting on your Desktop so it's easy to find!)


- After that is installed, open either Terminal (MacOSX) or Command Prompt (Windows 10) and navigate using CD to the script folder. If it was put on your desktop that should look something like:

`cd /Desktop/CanaData`


- Before running the script, you must install the required module (requests). Enter

`pip3 install requests`


- Now you're all setup to run the script using:

`python3 CanaData.py`


- Follow the on screen steps!


## I want more cities! State has too much info or takes to long (2hr+ for California lol!)
Please join our discord, mention @OP and let me know what cities you'd like added!


## Secret Functionality:
- Putting `all` for the states/cities question will loop through a txt file of all 50 states. This is nice because it will create a csv per state
- Putting `mylist` will attempt to read a 'mylist.txt' file locally. Please separate the states by new lines like so (capitals doesn't matter):

`California
Colorado
Oregon`
