import logon as LL
import common as CM
import csv
BASE_URL = "https://www.twig.me/v7/"
email = 'admin@zestl.com'
pwd = 'Zspladmin99'
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/location_coordinates_20Mar2017.csv"
ZbotID = 0
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
hasHeader = "Y"
lat = 1
long = 2

with open(inputFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    for row in data:

        url = BASE_URL + "zvice/setcoordinates/" + row[ZbotID]
        body = {"lat" : row[lat], "lng" : row[long]}
        method = "POST"
        jsonresponse = CM.hit_url_method(body, headers1, method, url)
        print jsonresponse
