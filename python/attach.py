
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
from os import walk

import hashlib\

import lib.login1 as LL


def getBaseStructure(zbotID, headers1):
    url = LL.BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    response = hit_url(RequestBody, headers1, zbotID, url)
    with open('/Users/sujoychakravarty/Dropbox/Zestl-scripts/rundir/tmp', 'w') as f:
        f.write(str(response))
    return json.loads(response)

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']



mypath = "/Users/sujoychakravarty/Dropbox/Zestl-Deployment/IISP/From IISP/bus routes"

f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break


headers, headers1 = LL.req_headers()

zviceID = "4ENP84MSUMNRN"

parentCardID = 137
#### a text card
url =  LL.BASE_URL + "genericcards/" + zviceID
body = {"parentCardID":120}
method = "POST"

parentCardID = 58
media_ext = "xls"
print "++++++++ ------------- +++++++++++"

url = LL.BASE_URL + "cards/" + str(parentCardID) + "/attachment/" + zviceID

for item in f:

    filename = mypath + "/" + item
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string = encoded_string.encode('utf8')
    # print encoded_string
    body = {}
    body['media'] = encoded_string
    body['media_type'] = ""
    body['media_ext'] = media_ext
    body['media_size'] = 120000
    body['media_name'] = item
    body['Caption'] = item

    jsonresponse = hit_url_method(body, headers1, method, url)


    print jsonresponse

