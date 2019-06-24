# CanaParse.py

![CanaParse.py](https://i.imgur.com/Qsb5Go0.png)

Open up `flower-filters.json` to view/edit the filter options.

Edit two variables in `CanaParse.py`:`csv_file` and `csv_folder` to point to your CSV.

Then:

`pip3 install -r requirements.txt`

`python3 ./CanaParse.py`

## Filter Examples (the default)
Create/edit filters by opening the `flower-filters.json` file and following my lead: 
```json
{
  "filters": [
    {
      "table_sort_col":"price",
      "limit_results_amt":20,
      "limit_results_amt_email":10,
      "name": "Vape Pens - Half Gram & Under",
      "key": "prices.half_gram",
      "compare": "<=",
      "price": 35,
      "categories": ["Concentrate"],
      "brands": [],
      "stores": [],
      "strains": [],
      "bad_words": ["rso","app","syringe","crumble","krumble","shatter","resin","badder","budder","sugar","wax","shake","baker","baking","reno","sparks","carson","Silver State Relief","topical","balm","lotion","Sun Valley"],
      "priority_words": ["special","deal","hurry","2 for 1","popcorn","fresh","fat","sticky"],
      "good_words":["vape","pen","cart","distillate"],
      "thc_floor": 85,
      "cbd_floor": 0.00, 
      "thc_floor_strict": true,
      "cbd_floor_strict": false,
      "terpenes" : [
        {
          "name":"Pinene",
          "floor":0.01,
          "floor_strict":false
        }
      ]
    },
    {
      "table_sort_col":"price",
      "limit_results_amt":20,
      "limit_results_amt_email":10,
      "name": "Cheap High THC Concentrates (non vape)",
      "key": "prices.gram",
      "compare": "<=",
      "price": 60,
      "categories": ["Concentrate", "wax"],
      "brands": [],
      "stores": [],
      "strains": [],
      "bad_words": ["vape","cart","distillate","baking","reno","sparks","carson","Silver State Relief","topical","balm","lotion","Sun Valley"],
      "priority_words": ["special","deal","hurry","2 for 1","popcorn","fresh","fat","sticky"],
      "good_words":[],
      "thc_floor": 85,
      "cbd_floor": 0.00, 
      "thc_floor_strict": true,
      "cbd_floor_strict": false,
      "terpenes" : [
        {
          "name":"Pinene",
          "floor":0.01,
          "floor_strict":false
        }
      ]
    },
    {
      "table_sort_col":"price",
      "limit_results_amt":20,
      "limit_results_amt_email":10,
      "name": "Full Ounce",
      "key": "prices.ounce",
      "compare": "<=",
      "price": 150,
      "categories": ["hybrid", "sativa", "indica"],
      "brands": [],
      "stores": [],
      "strains": [],
      "bad_words": ["shake","baker","baking","reno","sparks","carson","Silver State Relief","topical","balm","lotion","Sun Valley"],
      "priority_words": ["special","deal","hurry","2 for 1","popcorn","fresh","fat","sticky"],
      "thc_floor": 17,
      "cbd_floor": 0.00, 
      "thc_floor_strict": false,
      "cbd_floor_strict": false,
      "terpenes" : [
        {
          "name":"Pinene",
          "floor":0.01,
          "floor_strict":false
        }
      ]
    },
    {
      "table_sort_col":"price",
      "limit_results_amt":20,
      "limit_results_amt_email":10,
      "name": "Half Ounce",
      "key": "prices.half_ounce",
      "compare": "<=",
      "price": 100,
      "categories": ["hybrid", "sativa", "indica"],
      "brands": [],
      "stores": [],
      "strains": [],
      "bad_words": ["shake","baker","baking","reno","sparks","carson","Silver State Relief","topical","balm","lotion","Sun Valley"],
      "priority_words": ["special","deal","hurry","2 for 1","popcorn","fresh","fat","sticky"],
      "thc_floor": 17,
      "cbd_floor": 0.00, 
      "thc_floor_strict": false,
      "cbd_floor_strict": false,
      "terpenes" : [
        {
          "name":"Pinene",
          "floor":0.01,
          "floor_strict":false
        }
      ]
    },
    {
      "table_sort_col":"price",
      "limit_results_amt":20,
      "limit_results_amt_email":-1,
      "name": "Quarters",
      "key": "prices.quarter",
      "compare": "<=",
      "price": 50,
      "categories": ["hybrid", "sativa", "indica"],
      "brands": [],
      "stores": [],
      "strains": [],
      "bad_words": ["shake","baker","baking","reno","sparks","carson","Silver State Relief","topical","balm","lotion","pr","pre","sun valley"],
      "priority_words": ["special","deal","hurry","2 for 1","popcorn","fresh","fat","sticky"],
      "thc_floor": 17,
      "cbd_floor": 0.00, 
      "thc_floor_strict": false,
      "cbd_floor_strict": false,
      "terpenes" : [
        {
          "name":"Pinene",
          "floor":0.01,
          "floor_strict":false
        }
      ]
    },
    {
      "table_sort_col":"price",
      "limit_results_amt":20,
      "name": "Half Ounce - Shake/Baker's stuff",
      "limit_results_amt_email":10,
      "key": "prices.half_ounce",
      "compare": "<=",
      "price": 80,
      "categories": ["hybrid", "sativa", "indica"],
      "brands": [],
      "stores": [],
      "strains": [],
      "bad_words": ["shake","baker","baking","reno","sparks","carson","Silver State Relief","topical","balm","lotion","pr","pre","sun valley"],
      "good_words": ["popcorn","shake","baker","baking"],
      "priority_words": ["special","deal","hurry","2 for 1","popcorn","fresh","fat","sticky"],
      "thc_floor": 17,
      "cbd_floor": 0.00, 
      "thc_floor_strict": true,
      "cbd_floor_strict": false,
      "terpenes" : [
        {
          "name":"Myrcene",
          "floor":0.0,
          "floor_strict":false
        },
        {
          "name":"Limonene",
          "floor":0.01,
          "floor_strict":false
        },
        {
          "name":"B-Caryophyllene",
          "floor":0.01,
          "floor_strict":false
        }
      ]
    },
    {
      "table_sort_col":"price",
      "limit_results_amt":20,
      "limit_results_amt_email":10,
      "name": "Gram - Select Strains",
      "key": "prices.gram",
      "compare": "<=",
      "price": 20,
      "categories": ["hybrid", "sativa", "indica"],
      "brands": [],
      "stores": [],
      "strains": ["head cheese","agent orange", "fruit salad"],
      "bad_words": ["shake","baker","baking","reno","sparks","carson","Silver State Relief","topical","balm","lotion","pr","pre","sun valley"],
      "priority_words": ["head cheese","special","deal","hurry","2 for 1","popcorn","fresh","fat","sticky"],
      "thc_floor": 14,
      "thc_floor_strict": false,
      "cbd_floor_strict": false
    },
    {
      "table_sort_col":"price",
      "limit_results_amt":20,
      "limit_results_amt_email":10,
      "name": "High THC - Grams",
      "key": "prices.gram",
      "compare": "<=",
      "price": 100,
      "categories": ["hybrid", "sativa", "indica"],
      "brands": [],
      "stores": [],
      "strains": [],
      "bad_words": ["shake","baker","baking","reno","sparks","carson","Silver State Relief","topical","balm","lotion","pr","pre","sun valley"],
      "priority_words": ["special","deal","hurry","2 for 1","popcorn","fresh","fat","sticky"],
      "thc_floor": 28,
      "cbd_floor": 0.01,
      "thc_floor_strict": true,
      "cbd_floor_strict": false,
      "terpenes" : [ 
        {
          "name":"Myrcene",
          "floor":0.05,
          "floor_strict":true
        }
      ]
    },
    {
      "table_sort_col":"price",
      "limit_results_amt":20,
      "limit_results_amt_email":10,
      "name": "High Terps - Grams",
      "key": "prices.gram",
      "compare": "<=",
      "price": 100,
      "categories": ["hybrid", "sativa", "indica"],
      "brands": [],
      "stores": [],
      "strains": [],
      "bad_words": ["shake","baker","baking","reno","sparks","carson","Silver State Relief","topical","balm","lotion","pr","pre","sun valley"],
      "priority_words": ["special","deal","hurry","2 for 1","popcorn","fresh","fat","sticky"],
      "thc_floor": 17,
      "cbd_floor": 0.01,
      "thc_floor_strict": false,
      "cbd_floor_strict": false,
      "terpenes" : [
        {
          "name":"Myrcene",
          "floor":5.0,
          "floor_strict":false
        },
        {
          "name":"Limonene",
          "floor":0.01,
          "floor_strict":false
        },
        {
          "name":"B-Caryophyllene",
          "floor":0.01,
          "floor_strict":false
        },
        {
          "name":"Pinene",
          "floor":1,
          "floor_strict":true
        }
      ]
    }
  ]
}
```

### Filter options

- `table_sort_col` *Not integrated yet - default sort html table by specified column key
- `limit_results_amt` int value to limit results by splicing the list for each filter result (currently trying to sort the arr by price before splicing - but am not sure how well this is working. For best results, set this to -1 to disable. It's useful for easing into a new CSV/filter to not overwhelm your browser with too many results until you get your filters tuned-in)
- `limit_results_amt_email` Like above but for emails. 
- `name` The name that will appear in the webpage in the nav/block heading.
- `key` The filtering is currently setup to parse/format results based on flower weight. The `key` value corresponds to the weight data columns. Available options:
    - `prices.half_gram` 
    - `prices.gram` 
    - `prices.two_grams` 
    - `prices.eighth` 
    - `prices.quarter` 
    - `prices.half_ounce` 
    - `prices.ounce` 
- `compare` This tells the script how to handle the `price` option in regard to an items price. 
- `price` In conjunction with the above option, this can be used to filter either max/min values. 
- `categories` An array of category names. 
    - `indica` Flower only
    - `sativa` Flower only
    - `hybrid` Flower only
    - `concentrate` Must be used with `good_words` and `bad_words` options to narrow in on desired items like vape pens. More info further below.
    - `wax`
    - `preroll`
- `brands` `stores` `strains` Filter by these items.
- `bad_words` Filter out any items that contain any of these bad words. 
- `good_words` Filter out all items that do not contain any of the good_words list.
- `priority_words` Highlight items a light yellow color in the html that match any of these words. 
- `thc_floor` Float value
- `cbd_floor` Dispensaries around where I live do not seem to specify CBD amounts often in their menu data unless it's a special highlight. If you want to view their CBD amounts in a nice column if any are found, keep this enabled.
- `cbd_floor_strict` Do not use this or you will heavily filter good results. Or use it.
- `terpenes` Accepts an array of objects with these values set:
  - `name`
  - `floor`
  - `floor_strict`


Create as many filters as you'd like. Just find a sweet-spot for filtering so you can limit results. 

## How To Target Specific Items Like Vape Pens: 
If you are searching for flower then filtering is a bit easier. Searching for a concentrate is trickier. You have to narrow down results based first on `weight` as usual, then `categories` and finally tweak other options like `good_words`, `bad_words` and `thc_floor`. This will help you filter out unwanted types of concentrates and also CBD focused vapes. Here is an example of some filter options to help narrow in on cheap, high THC, vape pens in my area:

```json
"key": "prices.half_gram",
"price": 35,
"categories": ["Concentrate"],
"bad_words": ["app","syringe","crumble","krumble","shatter","resin","badder","budder","sugar","wax","reno","sparks","carson","Silver State Relief","topical","balm","lotion","Sun Valley"],
"good_words":["vape","pen","cart","distillate"],
"thc_floor": 85

```

The above filter options will narrow in on local vape pens that are 85% THC or higher that are less than or equal to $35.

## HTML Output

![main html](https://i.imgur.com/M5oVdPc.png)

Located in the `./output/` dir

Each filter becomes an html table in the generated html file in the `./output/` dir (like in the image above).

## "Daily Flowers" - Automated Filtered Email Results

![daily-flowers](https://i.imgur.com/OwQdE2T.png)

The script generates a `./output/flower-filter-email.html` file that is condensed and reformatted to work better with email clients. To setup an automated task that runs CanaData.py + CanaParse.py + emails you local flower results based on your filters, first setup an smtp relay server (here's a tut for linux: https://www.linode.com/docs/email/postfix/configure-postfix-to-send-mail-using-gmail-and-google-apps-on-debian-or-ubuntu/). 

Then open up `./email.sh` and follow the instructions. 

After editing the file and following the instructions, be sure to make it executable so it can run: 

`% chmod +x ./email.sh`

Go ahead and manually test the bash script to make sure it works before handing it off to conrab: 

`% sudo ./email.sh`

## Ways To Use This Tool: 
- You only run `CanaData.py` as many times as needed to grab all the updated menus for your state. Then adjust filters and run `CanaParse.py` as many times as needed to fitler the menus you grabbed previously. Parsing/filtering can take anywhere between a few second (for states like Nevada) to a few minutes (for Washington) or even upward to an hour (Cali). Once you know what you want and get how this all works, you won't need to finick with filter options/running the script over and over again...the idea is to get it to a point where you can adjust a few options (like strain, price, terps, etc.) and let it automate email notifications. 

- **Email Results**: Setup the email functionality to make the most of this. More info in `email.sh`.
- **Strain Filtering**: Even if common data like THC info is not available, you can keep your eye out for exotic strains (you have to create a new filter for each weight: gram, eighth, etc.). 

```json
"strains": ["agent orange", "fruit salad"]
```

- **Price Hunting Quantity**: Since the script was written based on weight value - price hunting by quantity works great. Set a filter `key` as `prices.half_ounce` and filter results by setting a max `price` of `70` dollars on the filter. The result will be a filtered html table of all local (statewide) half ounce menu items that are $70 and under.

```json
"key": "prices.half_ounce",
"price": 70,
"compare": "<="
```

- **Filter Out Results From Far Away Places**: If you're in a state like California, the results you get back will be too overwhelming and locations will span across the entire state. That's not useful outside of data collection. To make that useful for making a purchase, you have to filter the data that is given. As of now you can limit location results by adding allowed dispensary names to the `stores` list in your filter. Furthermore, you can add unwanted dispensary names and city/location names to the `bad_words` lists to filter out matching items. This will all help to narrow in on results from dispensary menus nearby. 

```json
"stores": ["The Dispensary","The Source","Nevada Made Marijuana"],
"bad_words": ["shake","baker","baking","reno","sparks","carson","Silver State Relief","topical","balm","lotion"]
```

- **Cannabinoid Filtering**: Works only if this data is available on your local weedmaps menus. If it is, then filter by individual terps, THC, CBD, etc. 

```json
"thc_floor": 17,
"cbd_floor": 0.01,
"thc_floor_strict": false,
"cbd_floor_strict": false,
"terpenes" : [
  {
    "name":"Myrcene",
    "floor":5.0,
    "floor_strict":true
  },
  {
    "name":"Limonene",
    "floor":0.01,
    "floor_strict":false
  },
  {
    "name":"B-Caryophyllene",
    "floor":0.01,
    "floor_strict":false
  },
  {
    "name":"Pinene",
    "floor":0.01,
    "floor_strict":false
  }
]
```

- **Aggressive Deal Hunting at the 1st of the Month (with emails)**: If you mainly restock your jars once a month - edit your crontab to automate `./email.sh` to be triggered a few times a day toward and after the 1st of the month. That way you can stay current throughout the day of any pop-up deals from dispensaries with your automated emails. So for instance, you could setup your crontab to look like this: 
```bash
# Everyday at 10 am
0 10 * * * bash /var/www/projects/CanaData/parse-scripts/email.sh

# The following will shoot out emails at: 8, 10, 12, 2, 4, 6 o'clock for 6 days at around the 1st of the month. 
00 8 29 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 12 29 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 14 29 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 16 29 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 18 29 * * bash /var/www/projects/CanaData/parse-scripts/email.sh

00 8 30 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 12 30 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 14 30 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 16 30 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 18 30 * * bash /var/www/projects/CanaData/parse-scripts/email.sh

00 8 31 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 12 31 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 14 31 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 16 31 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 18 31 * * bash /var/www/projects/CanaData/parse-scripts/email.sh

00 8 1 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 12 1 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 14 1 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 16 1 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 18 1 * * bash /var/www/projects/CanaData/parse-scripts/email.sh

00 8 2 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 12 2 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 14 2 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 16 2 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 18 2 * * bash /var/www/projects/CanaData/parse-scripts/email.sh

00 8 3 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 12 3 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 14 3 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 16 3 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
00 18 3 * * bash /var/www/projects/CanaData/parse-scripts/email.sh
```
That will continue to automate an email everyday at 10am but will "aggressively" email you updates every 2 hours between 8am and 8pm starting a few days before the end of the month and lasting a few days after. This will give you a good scoop on large quantity deals that pop-up right when you're ready to start looking for deals. 

- **Raspberry Pi LED Notifcation**: This hasn't been implemented, but it's very possible to setup a function that triggers something like a green LED to flash if any menu matches hit your filters. The Pi can do most of the heavy lifting and run every hour. So say your looking for a high THC phenotype of the strain `Agent Orange`, you could create a single filter with those options specified and if any local menus post flower that meets your filter criteria, a horn honks, LED's flash, alexa says something, etc. If there are too many menu's in your state, these scripts might not work well on a Pi. 

## Known Issues / Things to Note
All the data that is used comes from weedmaps menus. If dispensaries do not include terpene profiles and other cannabinoid info in their listing descriptions, then there isn't a way to filter that data. This is important to note because using something like the `terpene` filter for your area might not yield any results. For example, for some reason it seems Nevada is fairly consistant with adding this data to their menu listings which makes filtering cannabinoids for that state useful. 

Get creative with the filter options - especially for `good_words` and `bad_words`. 


---
This script is made to handle the data that is available from weedmaps, so the filters reflect that. If you'd like to understand what kind of data you are getting using CanaData.py, look at the output CSV using a CSV viewer. This will help you better understand how to use the filters / add to the functionality to suite your needs. Or go to weedmaps and view their menus. That's the data we're using. 

Primary intention: to be used for flower. Put on a crontask directly after CanaData has been run and send out emails with results based on filter criteria.
