# CanaData


# Welcome to CanaData
Don's favorite tool to retrieve state/cities listing results from Weedmaps! (Yes you can try all 50 states two ways!)


## Discord to discuss:
https://discord.gg/6WAcVek


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


## Secret Functionality:
- Putting `all` for the states/cities question will loop through a txt file of all 50 states. This is nice because it will create a csv per state
- Putting `united-states` will go through all listing (10k+) in the entire US but it will put all of it into 1 CSV... _BEWARE THIS IS A MASSIVE FILE_
