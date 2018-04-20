
import base64
import time
import urllib2
from urllib2 import URLError
from urllib2 import HTTPError
import requests
import urllib
import json
# import time
import os
import re
import sys
import csv
import StringIO
import itertools
import copy
import logon as LL
import common as CM
import hashlib




# inputLoginFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/login.csv"

# hasHeader = 'N'

# "https://twig.me/v4/usergroups/2HRKLHBPPYXSN"

# SERVER = "http://52.8.240.85/"
SERVER = "https://twig.me/"
version = "v4/"
BASE_URL = SERVER + version

zviceID = "23KBNM7BUFTYR"
# urlAdd = "zvice/interaction/" + zviceID
# "https://twig.me/v4/2HRKLHBPPYXSN"
# "https://twig.me/v4/membership/user/23KBNM7BUFTYR"
email = "admin@zestl.com"
# pwd = "TwigMeNow"
pwd = "Zspladmin99"
hasHeaderzvice = 'Y'
zvicefile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/memberships_uts.csv"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

with open(zvicefile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeaderzvice == "Y":
        row1 = data.next()
    for row in data:
        zviceID = row[0]


        r = requests.get("http://twig.me/v1/push/enctest/" + zviceID)
        tagnum = r.json()['encTagID']
        urlAdd = "membership/user/" + tagnum


        body = {}

        body['Title'] = row[2]
        body['Fees'] = ""
        body['StartDate'] = "2014-10-14"
        body['Expiry'] = row[3]
        body['Status'] = row[4]
        body['Notes'] = ""
        method = "POST"

        url = BASE_URL + urlAdd

        jsondata = CM.hit_url_method(body, headers1, method, url)

        print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
        print jsondata