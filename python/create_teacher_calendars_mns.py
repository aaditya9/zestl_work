import base64
import time
import urllib2
from urllib2 import URLError
from urllib2 import HTTPError
import requests
import urllib
import json
import time
import os
import re
import sys
import csv
import StringIO
import itertools

import lib.login_generic as LL






def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata






BASE_URL="http://twig.me/v1/"
email = 'radhika@zestl.com'
pwd = 'zestl123'
ZbotID = '9J5EDAR3Y2PZA'

filename = "/Users/sujoychakravarty/Dropbox/Zestl-share/Deployment/Millennium/Teaches_Admin_TagIDs_24072016.csv"

# headers, headers1 = LL.req_headers(passkey)
headers, headers1 = LL.req_headers(email, pwd, ZbotID, BASE_URL)



with open(filename, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    for row in data:
        ZviceID = row[0]

    # ZviceID = "28PGE3C95ZMZ8"

    # POST /v1/5TFLX6L78PMD4/calendars/

        method = "POST"
        url = BASE_URL + ZviceID + "/calendars/"
        r = requests.get("http://twig.me/v1/push/dectest/" + ZviceID)
        tagnum = r.json()['decTagID']

        body = {"LinkType":"CALENDAR","categorytype":"Calendar","ZviceID":tagnum,"Description":"Teacher's appointment calendar","Title":"Appointments","interactionID":"CommonInteraction_INTERACTION_TYPE_ADD_CALENDAR"}

        jsonreply = hit_url_method(body, headers1, method, url)
        # print jsonreply
        # jsonreply = json.loads(jsonreply)
        # jsonreply = hit_url_method(body, headers1, method, url)
        print "======calendar response ======="
        print jsonreply

