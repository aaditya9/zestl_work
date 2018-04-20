import requests
import csv
import logon as LL
import common as CM

email = "admin@zestl.com"
pwd = "Zspladmin99"
SERVER = "http://twig.me/"
version = "v7/"
BASE_URL = SERVER + version

# csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_per_1.csv"
csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_details.csv"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

with open(csvfile, 'r') as infile:
    data = csv.reader(infile, delimiter=',')
    for row in data:
        # num = int(row[0])+1
        # r = requests.get("http://twig.me/v1/push/enctest/" + str(num))
        r = requests.get("http://twig.me/v1/push/enctest/" + row[0])
        # r = requests.get("http://twig.me/v1/tagid/3142?enc=1" + row[0])
        tagnum =  r.json()['encTagID']
        print tagnum
        jsondata = CM.getBaseStructure(tagnum, headers1, BASE_URL)
        print  "===="
        print jsondata['title']

        # print tagnum + "-" + jsondata['title']
