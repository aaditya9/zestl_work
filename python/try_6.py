import requests
import csv
import logon as LL
import common as CM
# zvice = "6R44NHAMKXTVH"
email = "admin@zestl.com"
pwd = "Zspladmin99"
SERVER = "http://twig.me/"
version = "v7/"
BASE_URL = SERVER + version
tagCol = 1
csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_per_1.csv"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
with open(csvfile, 'r') as infile:
    data = csv.reader(infile, delimiter=',')
    for row in data:
        zvice = row[tagCol].strip()
        # print zvice
        jsondata = CM.getBaseStructure(zvice, headers1, BASE_URL)
        print jsondata['title']

