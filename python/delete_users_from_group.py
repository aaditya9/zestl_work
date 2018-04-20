import json
import logon as LL
import common as CM
import re
import requests
import csv
import password as PP

SERVER = "https://www.twig.me/"
version = "v8/"
BASE_URL = SERVER + version
zviceID = "9J5EDAR3Y2PZA"    ####  Business ID
email = "admin@zestl.com"
pwd = PP.pwd
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"

hasHeader1 = "Y"

# User Group Info :--- Users in Group1#

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
url = "https://twig.me/v8/usergroups/9J5EDAR3Y2PZA" + "?filter={\"limit\":1000,\"offset\":0}"
method = "GET"
body = {}
jsonresponse = CM.hit_url_method(body, headers1, method, url)
print jsonresponse
for a in json.loads(jsonresponse)['data']['elements']:
    with open(inputFile, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        if hasHeader1 == "Y":
            row1 = data.next()
        for row in data:
            gname = row[0].strip()
            if gname == a['title']:
                print "*************** Working on this Group : " + gname + "  ******************"
                url = a['cardsjsonurl']
                method = a['method']
                body = {}
                jsonresponse = CM.hit_url_method(body, headers1, method, url)
                print jsonresponse
                for sub in json.loads(jsonresponse)['data']['elements']:
                    if "basecard" == sub['cardtype']:
                        print "present"
                        for subac in sub['actions']:
                            if "Remove User?" == subac['title']:
                                print "ready to delete"
                                body = {}
                                method = subac['method']
                                print method
                                url = subac['actionUrl']
                                print url
                                print "------------"
                                ja = CM.hit_url_method(body, headers1, method, url)
                                print ja
                    # else: print "next level not present"