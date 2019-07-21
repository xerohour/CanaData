import os, sys
import csv
from datetime import datetime
from yattag import Doc
from yattag import indent
import re
import json
from operator import itemgetter

class FlowerFilter(object):
     pass

half_gram = 'prices.half_gram'
gram = 'prices.gram'
two_grams = 'prices.two_grams'
eighth = 'prices.eighth'
quarter = 'prices.quarter'
half_ounce = 'prices.half_ounce'
ounce = 'prices.ounce'

### editable ###

csv_folder = "../"+"CanaData_" + str(datetime.today().strftime('%m-%d-%Y'))
#csv_file = "vermont_results.csv"
#csv_file = "washington_results.csv"
#csv_file = "washington-dc_results.csv"
csv_file = "colorado_results.csv"
#csv_file = "arizona_results.csv"
#csv_file = "maine_results.csv"
#csv_file = "nevada_results.csv"

flower_filters = []
with open('./flower-filters.json') as json_file:
    data = json.load(json_file)
    for filter in data['filters']:
        flower_filter = FlowerFilter()
        flower_filter.table_sort_col = str(filter["table_sort_col"]) #used for view
        flower_filter.limit_results_amt = int(filter["limit_results_amt"]) #used for view
        flower_filter.limit_results_amt_email = int(filter["limit_results_amt_email"]) #used for view
        flower_filter.name = str(filter["name"]) #used for view
        flower_filter.key = str(filter["key"]) #most important var
        flower_filter.compare = str(filter["compare"]) #disregards zero amts
        flower_filter.price = float(filter["price"]) #float max price
        flower_filter.categories = filter["categories"]
        flower_filter.brands = filter["brands"]
        flower_filter.stores = filter["stores"]
        flower_filter.strains = filter["strains"]
        flower_filter.bad_words = filter["bad_words"]
        if 'good_words' in filter:
            flower_filter.good_words = filter["good_words"]
        flower_filter.priority_words = filter["priority_words"]
        flower_filter.thc_floor = int(filter["thc_floor"]) #float experimental: scans all output for any percentagex and tries to figure out if it's THC. If set to 0 it will disregard filter. It will disregard all results that do not have THC info.
        if 'cbd_floor' in filter:
            flower_filter.cbd_floor = float(filter["cbd_floor"]) #float same as above
        else:
            flower_filter.cbd_floor = 0
        flower_filter.thc_floor_strict = bool(filter["thc_floor_strict"]) #Allows items with no avail THC info
        flower_filter.cbd_floor_strict = bool(filter["cbd_floor_strict"]) #Allows items with no avail THC info

        if 'terpenes' in filter:
            flower_filter.terpenes = filter["terpenes"]
        else:
            flower_filter.terpenes = []

        flower_filters.append(flower_filter)
### non editable ###

def getComparisonVal(op,val1,val2):
    if(op == '>='):
        if(val1 >= val2):
            return 1
        else:
            return 0
    if(op == '<='):
        if(val1 > 0 and val1 <= val2):
            return 1
        else:
            return 0
    if(op == '=='):
        if(val1 == val2):
            return 1
        else:
            return 0
    if(op == '>'):
        if(val1 > val2):
            return 1
        else:
            return 0
    if(val1 > 0 and op == '<'):
        if(val1 < val2):
            return 1
        else:
            return 0
    else:
        return 0

hasWeightArr = []
with open(csv_folder+"/"+csv_file, encoding="utf8") as csvDataFile:
    csvReader = csv.reader(csvDataFile)

    for row in csvReader:
        if(row[9].replace('.','',1).isdigit() and float(row[9]) > 0  \
        or row[10].replace('.','',1).isdigit() and float(row[10]) > 0 \
        or row[11].replace('.','',1).isdigit() and float(row[11]) > 0 \
        or row[12].replace('.','',1).isdigit() and float(row[12]) > 0 \
        or row[13].replace('.','',1).isdigit() and float(row[13]) > 0 \
        or row[14].replace('.','',1).isdigit() and float(row[14]) > 0 \
        or row[15].replace('.','',1).isdigit() and float(row[15]) > 0):
            hasWeightArr.append(row)

class GetOutOfLoop( Exception ):
    pass

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

def extract_float_from_str(str):
    mgarr = []
    for idx, char in enumerate(str):
        if not str.isdigit() and idx is not 0:
            if str is ".":
                mgarr.append(str)
            else:
                break
                #we've reached the end of the amt

        elif str.isspace() and idx is 0:
            pass
        else:
            mgarr.append(str)

    return ''.join(mgarr)

filtered_tables = []
for filter in flower_filters:
    arr = hasWeightArr.copy()

    intToUse = 9
    if(filter.key == gram):
        intToUse = 9
    if(filter.key == two_grams):
        intToUse = 10
    if(filter.key == eighth):
        intToUse = 11
    if(filter.key == quarter):
        intToUse = 12
    if(filter.key == half_ounce):
        intToUse = 13
    if(filter.key == ounce):
        intToUse = 14
    if(filter.key == half_gram):
        intToUse = 15

    for row in hasWeightArr:

        if(filter.price):
            if(getComparisonVal(filter.compare,float(row[intToUse]),float(filter.price)) == 0):
                try:
                    arr.remove(row)
                    continue
                except:
                    pass
                continue

        if(len(filter.categories)):
            if(row[20].lower() not in str(filter.categories).lower()):
                try:
                    arr.remove(row)
                    continue
                except:
                    pass
                continue

        if(len(filter.brands)):
            res = [ele for ele in filter.brands if(ele.lower() in " ".join(row).lower())] 
            if (bool(res) is False):
                try:
                    arr.remove(row)
                    continue
                except:
                    pass
                continue

        if(len(filter.strains)):

            res = [ele for ele in filter.strains if(ele.lower() in " ".join(row).lower())] 
            if (bool(res) is False):
                try:
                    arr.remove(row)
                    continue
                except:
                    pass
                continue

        if(len(filter.stores)):
            res = [ele for ele in filter.stores if(ele.lower() in " ".join(row).lower())] 
            if (bool(res) is False):
                try:
                    arr.remove(row)
                    continue
                except:
                    pass
                continue

        
        if hasattr(filter, 'bad_words') and len(filter.bad_words):
            breaker = False
            for word in filter.bad_words:
                for subrow in row:
                    if(word.lower() in subrow.lower()):
                        try:
                            arr.remove(row)
                            continue
                        except:
                            pass
                        breaker = True 
                        break
                    else:

                        continue
                if breaker:
                    break


        if hasattr(filter, 'good_words') and len(filter.good_words):
            if any(ext in " ".join(row).lower() for ext in filter.good_words):
                pass
            else:
                print("removing non good_words item")
                try:
                    arr.remove(row)
                    continue
                except:
                    pass

                    

        if(filter.thc_floor > 0):
            if("THC".lower() not in " ".join(row).lower()):
                if(filter.thc_floor_strict):
                    try:
                        arr.remove(row)
                        continue
                    except:
                        pass
                else:
                    pass
            else:
                for subrow in row:
                    if('thc' in str(subrow).lower()):
                        ind = subrow.lower().find('THC'.lower())
                        result = 0

                        #If the first char is a digit, let's ussume it's THC
                        if(subrow[0].isdigit()):
                            result = subrow[0:7]
                        #THC:
                        if "THC:" in subrow:
                            result = subrow.split("THC:")[1][0:7]

                        if len(re.findall(r"[-+]?\d*\.\d+|\d+", str(result) )) > 0:
                            result = re.findall(r"[-+]?\d*\.\d+|\d+", str(result) )[0]
                        
                        if str(result).replace('.','',1).isdigit():
                            if(float(result) < float(filter.thc_floor)):
                                try:
                                    arr.remove(row)
                                    break
                                except:
                                    pass
                                
                                break
                            else:
                                strtoadd = str('thc'+"+"+str(result))
                                row.append( strtoadd )
                                break

        if(filter.cbd_floor > 0.001):
            if("CBD".lower() not in " ".join(row).lower()):
                if(filter.cbd_floor_strict):
                    try:
                        arr.remove(row)
                        continue
                    except:
                        pass
                else:
                    pass
            else:
                for subrow in row:

                    if('cbd' in str(subrow).lower()):
                        ind = subrow.lower().find('CBD'.lower())
                        result = 0
                        if(find_between(subrow, "CBD: ", "%").replace('.','',1).isdigit()):
                            result = find_between(subrow, "CBD: ", "%")
                        if(find_between(subrow, "CBD - ", "%").replace('.','',1).isdigit()):
                            result = find_between(subrow, "CBD - ", "%")
                        if(find_between(subrow, ": ", "% CBD").replace('.','',1).isdigit()):
                            result = find_between(subrow, ": ", "% CBD")
                        if( subrow.split('% CBD')[0][len(subrow.split('% CBD')[0])-4:len(subrow.split('% CBD')[0])].replace('.','',1).isdigit() ):
                            result = subrow.split('% CBD')[0][len(subrow.split('% CBD')[0])-4:len(subrow.split('% CBD')[0])]
                            
                        if( subrow.split('% CBD')[0].replace('.','',1).isdigit() ):
                            result = subrow.split('% CBD')[0]
                            
                        if(float(result) < filter.cbd_floor):
                            try:
                                arr.remove(row)
                                break
                            except:
                                pass
                            
                            break
                        else:
                            strtoadd = str("cbd"+"+"+str(result))
                            row.append(str(strtoadd))
                            break
        if(len(filter.terpenes)):
            for terp in filter.terpenes:
                if(str(terp["name"].lower()) not in " ".join(row).lower()):
                    if(terp["floor_strict"]):
                        try:
                            arr.remove(row)
                            continue
                        except:
                            pass
                    else:
                        pass
                else:
                    for subrow in row:

                        if(terp["name"].lower() in str(subrow).lower()):
                            ind = subrow.lower().find(terp["name"].lower())
                            result = 0
                            if(find_between(subrow, terp["name"].lower()+": ", "%").replace('.','',1).isdigit()):
                                result = find_between(subrow.lower(), terp["name"].lower()+": ", "%")

                            if(len(subrow.lower().split(terp["name"].lower())[1])):
                                if(subrow.lower().split(terp["name"].lower())[1][0] == ":"):
                                    result = subrow.lower().split(terp["name"].lower())[1][1]

                                    if(subrow.lower().split(terp["name"].lower())[1][1].isspace()):

                                        result = subrow.lower().split(terp["name"].lower())[1][2:7]

                                    elif( (subrow.lower().split(terp["name"].lower())[1][1]).isdigit() ):

                                        result = subrow.lower().split(terp["name"].lower())[1][1:7]
                                        pass
                                
                                    
                                elif(subrow.lower().split(terp["name"].lower())[1][0].isspace() \
                                    and len(subrow.lower().split(terp["name"].lower())[1]) > 1 ):
                                    if(subrow.lower().split(terp["name"].lower())[1][1] == "-"):
                                        result = subrow.lower().split(terp["name"].lower())[1][3:7]
                                    elif(subrow.lower().split(terp["name"].lower())[1][1].isdigit()):
                                        result = subrow.lower().split(terp["name"].lower())[1][1:7]

                                if len(re.findall(r"[-+]?\d*\.\d+|\d+", str(result) )) > 0:
                                    result = re.findall(r"[-+]?\d*\.\d+|\d+", str(result) )[0]

                            if str(result).replace('.','',1).isdigit():
                                if(float(result) < float(terp["floor"])):
                                    try:
                                        arr.remove(row)
                                        break
                                    except:
                                        pass
                                    
                                    break
                                else:
                                    strtoadd = str(terp["name"].lower()+"+"+str(result))

                                    row.append( strtoadd )

                                    break

                                
    if(filter.limit_results_amt > -1 and len(arr) > filter.limit_results_amt):
        
        #sorting by price before snipping
        arr = sorted(arr, key=lambda x: (x[1]))
        arr = arr[-filter.limit_results_amt:]
    filtered_tables.append(arr)

csvfile = "./output/filtered.csv"

#with open(csvfile, "w") as output:
#    writer = csv.writer(output, lineterminator='\n')
#    writer.writerows(filteredItemsArr)  

def translate_amnt_to_col(amnt):
    if(amnt == gram):
        return 9
    if(amnt == two_grams):
        return 10
    if(amnt == eighth):
        return 11
    if(amnt == quarter):
        return 12
    if(amnt == half_ounce):
        return 13
    if(amnt == ounce):
        return 14
    if(amnt == half_gram):
        return 15

def as_currency(amount):
    if amount >= 0:
        return '${:,.2f}'.format(amount)
    else:
        return amount

def as_percentage(amount):
    if amount >= 0 and amount < 101:
        return '{:,.2f}%'.format(amount)
    else:
        return ""

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def generate_html( ):
    priorityClass = ""
    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html', lang="en"):
        with tag('head'):
            doc.asis('<meta charset="utf-8">')
            doc.asis('<meta name="viewport" content="width=device-width, initial-scale=1">')
            doc.asis('<link rel="shortcut icon" href="./favicon.ico" />')
            doc.asis('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">')
            doc.asis('<link href="https://cdn.jsdelivr.net/gh/fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.css" type="text/css" rel="stylesheet" />')
            doc.asis('<link href="./css/theme.bootstrap.min.css" type="text/css" rel="stylesheet" />')
            doc.asis('<link href="./css/styles.css" type="text/css" rel="stylesheet" />')
            with tag('script', src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"):
                pass
            with tag('script', src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"):
                pass
            with tag('script', src="https://cdn.jsdelivr.net/gh/fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.js"):
                pass
            with tag('script', src="./js/jquery.tablesorter.min.js"):
                pass
            with tag('script', src="./js/jquery.tablesorter.widgets.min.js"):
                pass
            with tag('script', src="./js/scripts.js"):
                pass
            with tag('body'):
                with tag('div', klass="container-fluid main"):
                    with tag('nav', klass="navbar navbar-expand-lg navbar-light bg-light"):
                        with tag('a', klass="navbar-brand"):
                            doc.stag('img', src="./img/logo.jpg", klass="img logo")
                            text("FLOWER FILTER")
                        with tag('div', klass="collapse navbar-collapse", id="navbarSupportedContent"):
                            with tag('ul', klass="navbar-nav mr-auto"):
                                for navitem in flower_filters:
                                    with tag('li', klass="nav-item"):
                                        with tag('a', href='#'+navitem.name.replace(" ", "_").lower()):
                                            text(navitem.name)
                            with tag('small',klass="text-secondary"):
                                text(csv_folder+"/"+csv_file)
                        with tag('small',klass="text-danger"):
                                now = datetime.now().strftime("%b %d %Y %I:%M %p").lstrip("0").replace(" 0", " ")
                                text("Updated: ")
                                doc.asis('<br>')
                                text(now)
                    for i in range(len(flower_filters)):

                        with tag('h3', id=flower_filters[i].name.replace(" ", "_").lower()):
                            text(flower_filters[i].name)
                            with tag('span', klass="results-amt text-danger"):
                                text(" (" + str(len(filtered_tables[i])) +" Results)" )

                        with tag('small'):
                            with tag("strong"):
                                text("Applied filters: ")

                            for key, value in dict((name, getattr(flower_filters[i], name)) for name in dir(flower_filters[i]) if not name.startswith('__')).items():
                                with tag("span", klass="text-danger"):
                                    text(key)
                                if(isinstance(value, list)):
                                    with tag("span", klass="text-secondary"):
                                        text(json.dumps(value))
                                else:
                                    with tag("span", klass="text-secondary"):
                                        text(value)
                        with tag('table', klass='col-12 table table-hover'):
                            with tag('thead', klass='table-info'):
                                with tag('tr'):
                                    with tag('th', ('data-sort', 'int')): #id
                                        text('Id')
                                    with tag('th', ('data-sort', 'float')): #price
                                        text('Price')
                                    with tag('th'):
                                        text('Image')
                                    with tag('th', ('data-sort', 'string')):
                                        text('Strain')
                                    with tag('th', ('data-sort', 'string')):
                                        text('Category')
                                    with tag('th', ('data-sort', 'float'), klass="canabinoid"):
                                            text('THC')
                                    if(flower_filters[i].cbd_floor > 0):
                                        with tag('th', ('data-sort', 'float'), klass="canabinoid"):
                                                text('CBD')
                                    if(len(flower_filters[i].terpenes)):
                                        for terp in flower_filters[i].terpenes:

                                            with tag('th', ('data-sort', 'float'), klass="canabinoid"):
                                                    text(terp['name'])

                                    with tag('th', ('data-sort', 'string')):
                                        text('Dispensary')
                                    with tag('th', width="30%"):
                                        text('Info')
                            with tag('tbody',klass=""):
                                for row in filtered_tables[i]:
                                    
                                    if(len(flower_filters[i].priority_words)):

                                        res = [ele for ele in flower_filters[i].priority_words if(ele.lower() in "".join(row).lower())]
                                        if (bool(res) is True):
                                            priorityClass = "priority"
                                        else:
                                            priorityClass = ""
                                    with tag('tr', klass=priorityClass):
                                        with tag('th', scope='row'):
                                            with tag("small"):
                                                text(row[0])
                                        with tag('td'):
                                            with tag('strong'):
                                                text(as_currency(float(row[translate_amnt_to_col(flower_filters[i].key)])))
                                        with tag('td', klass="thumb"):
                                            with tag('a', ('data-fancybox', 'gallery'), href=row[17]):
                                                doc.stag('img', src=row[17], klass="img img-thumbnail", width="140", onerror="this.src='./img/logo.jpg';")
                                        with tag('td'):
                                            line = re.sub('[#]', '', row[28])
                                            url = 'https://weedmaps.com'+line
                                            with tag('a', href=url, target="_blank"):
                                                text(row[2])
                                        with tag('td'):
                                            text(row[20])
                                        with tag('td'):
                                            if(len(" ".join(row).split("thc"+"+")) > 1):
                                                colorClass = ""
                                                amt = " ".join(row).split("thc"+"+")[1].split(' ')[0]
                                                if float(amt) >= 28:
                                                    colorClass = "text-danger font-weight-bold"
                                                with tag('span', klass=colorClass):
                                                    text( as_percentage( float(amt) ) )
                                                
                                        if(flower_filters[i].cbd_floor > 0):
                                            with tag('td'):
                                                if(len(" ".join(row).split("cbd"+"+")) > 1):
                                                    amt = " ".join(row).split("cbd"+"+")[1].split(' ')[0]
                                                    text( as_percentage( float(amt) ) )
                                        if(flower_filters[i].terpenes):
                                            for terp in flower_filters[i].terpenes:
                                                
                                                with tag('td'):
                                                    if(len(" ".join(row).lower().split(terp["name"].lower()+"+")) > 1):
                                                        amt = " ".join(row).lower().split(terp["name"].lower()+"+")[1].split(' ')[0]
                                                        text( as_percentage( float(amt) ) )
                                        with tag('td'):
                                            text(row[29])
                                        with tag('td'):
                
                                            text(cleanhtml(row[1]))
                    doc.asis('''<!-- Footer -->
                    <footer class="page-footer font-small blue pt-4">

                      <!-- Footer Links -->
                      <div class="container-fluid text-center text-md-left">

                        <!-- Grid row -->
                        <div class="row">

                          <!-- Grid column -->
                          <div class="col-md-6 mt-md-0 mt-3">

                            <!-- Content -->
                            <h5 class="text-uppercase">About The Project</h5>
                            <p>This project is made to handle the data that is available from weedmaps, etc, etc.</p>

                          </div>
                          <!-- Grid column -->

                          <hr class="clearfix w-100 d-md-none pb-3">

                          <!-- Grid column -->
                          <div class="col-md-3 mb-md-0 mb-3">

                            <!-- Links -->
                            <h5 class="text-uppercase">Links</h5>

                            <ul class="list-unstyled">
                              <li>
                                <a href="https://weedmaps.com/" target="_blank">weedmaps.com</a>
                              </li>
                              <li>
                                <a href="https://www.cannabinoidclinical.com/science-cannabinoids" target="_blank">Cannabis Science</a>
                              </li>
                              <li>
                                <a href="https://www.leafly.com/news/cannabis-101/list-major-cannabinoids-cannabis-effects" target="_blank">Cannabinoids Info</a>
                              </li>
                              <li>
                                <a href="https://www.sclabs.com/terpenes/" target="_blank">Terpenes</a>
                              </li>
                            </ul>

                          </div>
                          <!-- Grid column -->

                          <!-- Grid column -->
                          <div class="col-md-3 mb-md-0 mb-3">

                            <!-- Links -->
                            <h5 class="text-uppercase">Links</h5>

                            <ul class="list-unstyled">
                              <li>
                                <a href="https://www.reddit.com/r/trees" target="_blank">/r/trees</a>
                              </li>
                            </ul>

                          </div>
                          <!-- Grid column -->

                        </div>
                        <!-- Grid row -->

                      </div>
                      <!-- Footer Links -->

                      <!-- Copyright -->
                      <div class="footer-copyright text-center py-3">©420 <a href="#">CanaData + CanaParse</a>
                      </div>
                      <!-- Copyright -->

                    </footer>
                    <!-- Footer -->''')

    return indent(doc.getvalue()) 

def generate_html_email( ):

    priorityClass = ""
    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html', lang="en"):
        with tag('head'):
            doc.asis('<meta charset="utf-8">')
            doc.asis('<meta name="viewport" content="width=device-width, initial-scale=1">')
            doc.asis('<link rel="shortcut icon" href="./favicon.ico" />')
            doc.asis('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">')
            doc.asis('<link href="https://cdn.jsdelivr.net/gh/fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.css" type="text/css" rel="stylesheet" />')
            doc.asis('<link href="./css/theme.bootstrap.min.css" type="text/css" rel="stylesheet" />')
            doc.asis('<link href="./css/styles.css" type="text/css" rel="stylesheet" />')
            with tag('script', src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"):
                pass
            with tag('script', src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"):
                pass
            with tag('script', src="https://cdn.jsdelivr.net/gh/fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.js"):
                pass
            with tag('script', src="./js/jquery.tablesorter.min.js"):
                pass
            with tag('script', src="./js/jquery.tablesorter.widgets.min.js"):
                pass
            with tag('script', src="./js/scripts.js"):
                pass
            with tag('body',style="font-size:10px;"):
                with tag('div', klass="container main", style="margin:0 auto;max-width:600px;"):
                    with tag('nav', klass="navbar navbar-expand-lg navbar-light bg-light"):
                        with tag('a', klass="navbar-brand"):
                            doc.stag('img', src="https://github.com/justinemter/CanaData/blob/master/parse-script/output/img/logo.jpg?raw=true", klass="img logo")

                    for i in range(len(flower_filters)):

                        with tag('h1', id=flower_filters[i].name.replace(" ", "_").lower()):
                            text(flower_filters[i].name)

                        with tag('table', klass='col-12 table table-hover', align="center", width="100%", border="0", cellspacing="0", cellpadding="0"):
                            with tag('thead', klass='table-info'):
                                with tag('tr'):
                                    with tag('th', ('data-sort', 'float')): #price
                                        text('Price')
                                    with tag('th'):
                                        text('Image')
                                    with tag('th', ('data-sort', 'string')):
                                        text('Strain')
                                    with tag('th', ('data-sort', 'string')):
                                        text('Category')
                                    with tag('th', ('data-sort', 'float'), klass="canabinoid"):
                                            text('THC')
                                    with tag('th', ('data-sort', 'string')):
                                        text('Dispensary')

                            with tag('tbody',klass=""):
                                idx = 0
                                for row in filtered_tables[i]:
                                    if flower_filters[i].limit_results_amt_email > -1 and idx > flower_filters[i].limit_results_amt_email:
                                        print(flower_filters[i].limit_results_amt_email)
                                        break
                                    idx += 1
                                    if(len(flower_filters[i].priority_words)):

                                        res = [ele for ele in flower_filters[i].priority_words if(ele.lower() in "".join(row).lower())]
                                        if (bool(res) is True):
                                            priorityClass = "priority"
                                        else:
                                            priorityClass = ""
                                    with tag('tr', klass=priorityClass):
                                        with tag('th'):
                                            with tag('strong'):
                                                text(as_currency(float(row[translate_amnt_to_col(flower_filters[i].key)])))
                                        with tag('td', klass="thumb"):
                                            with tag('a', ('data-fancybox', 'gallery'), href=row[17]):
                                                doc.stag('img', src=row[17], klass="img img-thumbnail", width="140", onerror="this.src='https://github.com/justinemter/CanaData/blob/master/parse-script/output/img/logo.jpg?raw=true';")
                                        with tag('td'):
                                            line = re.sub('[#]', '', row[28])
                                            url = 'https://weedmaps.com'+line
                                            with tag('a', href=url, target="_blank"):
                                                text(row[2])
                                        with tag('td'):
                                            text(row[20])
                                        with tag('td'):
                                            if(len(" ".join(row).split("thc"+"+")) > 1):
                                                colorClass = ""
                                                amt = " ".join(row).split("thc"+"+")[1].split(' ')[0]
                                                if float(amt) >= 28:
                                                    colorClass = "text-danger font-weight-bold"
                                                with tag('span', klass=colorClass):
                                                    text( as_percentage( float(amt) ) )
                                        with tag('td'):
                                            text(row[29])

    return indent(doc.getvalue())


def generate_shell_html( ):
    priorityClass = ""
    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html', lang="en"):
        with tag('head'):
            doc.asis('<meta charset="utf-8">')
            doc.asis('<meta name="viewport" content="width=device-width, initial-scale=1">')
            doc.asis('<link rel="shortcut icon" href="./favicon.ico" />')
            doc.asis('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">')
            doc.asis('<link href="https://cdn.jsdelivr.net/gh/fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.css" type="text/css" rel="stylesheet" />')
            doc.asis('<link href="./css/theme.bootstrap.min.css" type="text/css" rel="stylesheet" />')
            doc.asis('<link href="./css/styles.css" type="text/css" rel="stylesheet" />')
            with tag('script', src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"):
                pass
            with tag('script', src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"):
                pass
            with tag('script', src="https://cdn.jsdelivr.net/gh/fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.js"):
                pass
            with tag('script', src="./js/jquery.tablesorter.min.js"):
                pass
            with tag('script', src="./js/jquery.tablesorter.widgets.min.js"):
                pass
            with tag('script', src="./js/scripts.js"):
                pass
            with tag('body',klass="shell"):
                doc.asis('''<div class="modal" tabindex="-1" role="dialog">
                          <div class="modal-dialog" role="document">
                            <div class="modal-content">
                              <div class="modal-header">
                                <h5 class="modal-title">Modal title</h5>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                  <span aria-hidden="true">&times;</span>
                                </button>
                              </div>
                              <div class="modal-body">
                                <p>Modal body text goes here.</p>
                              </div>
                              <div class="modal-footer">
                                <button type="button" class="btn btn-primary">Save changes</button>
                                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                              </div>
                            </div>
                          </div>
                        </div>''')
                with tag('div', klass="container-fluid main"):
                    with tag('nav', klass="navbar navbar-expand-lg navbar-light bg-light"):
                        with tag('a', klass="navbar-brand"):
                            doc.stag('img', src="./img/logo.jpg", klass="img logo")
                            text("FLOWER FILTER SHELL")
                        with tag('div', klass="collapse navbar-collapse", id="navbarSupportedContent"):
                            
                            with tag('div', klass="dropdown show"):
                                with tag('a', ("data-toggle","dropdown"), klass="btn btn-secondary dropdown-toggle", href="#", role="button", id="dropdownMenuLink"):
                                        text(csv_folder+"/"+csv_file)
                                with tag('div', klass="dropdown-menu"):
                                    with tag('a', klass="dropdown-item"):
                                        text(csv_folder+"/"+csv_file)
                                    with tag('a', klass="dropdown-item"):
                                        text(csv_folder+"/"+csv_file)
                    for i in range(len(flower_filters)):

                        with tag('h3', id=flower_filters[i].key):
                            text(flower_filters[i].name)

                        with tag('small'):
                            with tag("strong"):
                                text("Applied filters: ")
                            with tag("span"):
                                text("key: ")
                            text(flower_filters[i].key)
                            with tag("span"):
                                text("compare: ")
                            text(flower_filters[i].compare)
                            with tag("span"):
                                text("price: ")
                            text(as_currency(float(flower_filters[i].price)))
                            if(len(flower_filters[i].categories)):
                                with tag("span"):
                                    text("categories: ")
                                text("/".join(flower_filters[i].categories))
                            if(len(flower_filters[i].strains)):
                                with tag("span"):
                                    text("strains: ")
                                text("/".join(flower_filters[i].strains))
                            if(len(flower_filters[i].brands)):
                                with tag("span"):
                                    text("brands: ")
                                text("/".join(flower_filters[i].brands))
                            if(len(flower_filters[i].stores)):
                                with tag("span"):
                                    text("stores: ")
                                text("/".join(flower_filters[i].stores))
                            if(len(flower_filters[i].bad_words)):
                                with tag("span"):
                                    text("bad_words: ")
                                text("/".join(flower_filters[i].bad_words))
                            if(flower_filters[i].thc_floor):
                                with tag("span"):
                                    text("thc_floor: ")
                                text(as_percentage(float(flower_filters[i].thc_floor)))
                            if(flower_filters[i].thc_floor_strict):
                                with tag("span"):
                                    text("thc_floor_strict: ")
                                text(flower_filters[i].thc_floor_strict)
                        with tag('table', klass='col-12 table table-hover'):
                            with tag('thead', klass='table-info'):
                                with tag('tr'):
                                    with tag('th', ('data-sort', 'int')):
                                        text('Id')
                                    with tag('th', ('data-sort', 'float')):
                                        text('Price')
                                    with tag('th'):
                                        text('Image')
                                    with tag('th', ('data-sort', 'string')):
                                        text('Strain')
                                    with tag('th', ('data-sort', 'string')):
                                        text('Category')
                                    with tag('th', ('data-sort', 'float')):
                                            text('THC')
                                    with tag('th', ('data-sort', 'string')):
                                        text('Dispensary')
                                    with tag('th', width="30%"):
                                        text('Info')
                            with tag('tbody'):
                                for row in filtered_tables[i]:
                                    
                                    if(len(flower_filters[i].priority_words)):

                                        res = [ele for ele in flower_filters[i].priority_words if(ele.lower() in "".join(row).lower())]
                                        if (bool(res) is True):
                                            priorityClass = "priority"
                                        else:
                                            priorityClass = ""
                                    with tag('tr', klass=priorityClass):
                                        with tag('th', scope='row'):
                                            with tag("small"):
                                                text(row[0])
                                        with tag('td'):
                                            with tag('strong'):
                                                text(as_currency(float(row[translate_amnt_to_col(flower_filters[i].key)])))
                                        with tag('td', klass="thumb"):
                                            with tag('a', ('data-fancybox', 'gallery'), href=row[17]):
                                                doc.stag('img', src=row[17], klass="img img-thumbnail", width="140")
                                        with tag('td'):
                                            line = re.sub('[#]', '', row[28])
                                            url = 'https://weedmaps.com'+line
                                            with tag('a', href=url, target="_blank"):
                                                text(row[2])
                                        with tag('td'):
                                            text(row[20])
                                        with tag('td'):
                                            try:
                                                text(as_percentage(float(row[36]))) #THC
                                            except:
                                                text("n/a") #THC
                                        with tag('td'):
                                            text(row[29])
                                        with tag('td'):
                                            text(row[1])
    return indent(doc.getvalue()) 

def write_html_to_file(data, filename="index.html"):

    now = datetime.now()
    fileName = "./output/"+filename
    writepath = './'
    mode = 'w'
    with open(writepath+fileName, mode, encoding='utf-8') as f:
        f.write(data)

write_html_to_file(generate_html())
write_html_to_file(generate_shell_html(), "flower-filter-shell.html")
write_html_to_file(generate_html_email(), "flower-filter-email.html")
print("Done.")
                
            