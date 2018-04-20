import logon as LL
import common as CM
import csv

# SERVER = "http://35.154.64.11/"  # test
SERVER = "https://twig.me/" #Production
version = "v7/"
BASE_URL = SERVER + version
zviceID = "WYE685C4N8BCV"

email = "admin@zestl.com"
# pwd = "TwigMeNow"
pwd = "Zspladmin99"
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/shoeXpress_product_17feb.csv"
hasHeader = "Y"

Ptitle = 2
Pdesc = 1
Pbrand = 0
pmrp = 3
pmsp = 4

f = []
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
with open(inputFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    method = "POST"
    counter = 0
    for row in data:
        counter += 1
        print counter
        body = {}
        body['title'] = row[Ptitle]
        body['desc'] = row[Pdesc]
        body['brand'] = row[Pbrand]
        body['mrp'] = int(row[pmrp])
        body['msp'] = int(row[pmsp])
        body['category'] = "122/341"
        body['filter'] = f
        # url = "http://35.154.64.11/v7/products/8SFKZCV5PFAXV/add"
        url = "https://twig.me/v7/products/WYE685C4N8BCV/add"
        jasub = CM.hit_url_method(body, headers1, method, url)
        print jasub