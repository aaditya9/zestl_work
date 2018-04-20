
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

import logon as LL


def getBaseStructure(zbotID, headers1):
    url = LL.BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    response = hit_url(RequestBody, headers1, zbotID, url)
    with open('/Users/User/Dropbox/Zestl-scripts/rundir/tmp', 'w') as f:
        f.write(str(response))
    return json.loads(response)

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']



mypath = "/Users/User/Dropbox/Zestl-Deployment/VKArch/FromVKA/Tinsel Town/Stage-03/Stage-03/Dwgs"
mypath = "/Users/User/Downloads/homagimages"

f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break

email = "admin@zestl.com"
password = "Zspladmin99"
BASE_URL = "https://twig.me/"
version = "v3/"

versionUrl = BASE_URL + version


headers, headers1 = LL.req_headers(email, password, versionUrl)

#
# zviceID = "EF9PHJBFDZ2GA"
#
# parentCardID = 137
# #### a text card
# url =  LL.BASE_URL + "genericcards/" + zviceID
# body = {"parentCardID":120}
# method = "POST"
#
# parentCardID = 137

# actionUrl : "https://twig.me/v1/6JB5NJW4V5NCK/gallery/27/image"

print "++++++++ ------------- +++++++++++"

# url = LL.BASE_URL + "cards/" + str(parentCardID) + "/attachment/" + zviceID

url = "https://twig.me/v3/5M4D9YP84AEQ8/gallery/33/image"
url = "https://twig.me/v3/5M4D9YP84AEQ8/gallery/33/image"
for item in f:

    filename = mypath + "/" + item
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string = encoded_string.encode('utf8')
    # print encoded_string
    body = {}
    body['media'] = encoded_string
    body['media_type'] = ""
    body['media_ext'] = "pdf"
    body['media_size'] = 120000
    body['media_name'] = item
    body['Caption'] = item

    method = "POST"

    jsonresponse = hit_url_method(body, headers1, method, url)


    print jsonresponse

