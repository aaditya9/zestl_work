
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
import hashlib\

import lib.login1 as LL


def getBaseStructure(zbotID, headers1):
    url = LL.BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    response = hit_url(RequestBody, headers1, zbotID, url)
    with open('/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/rundir/tmp', 'w') as f:
        f.write(str(response))
    return json.loads(response)

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def getAllUserGroups(headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('GET', BASE_URL + 'usergroups/' + zbotID, None, headers)
    #
    # print "User Group API response : Code : " + str(jsondata['code'])
    # print "======================="
    # print jsondata['reply']
    # print "======================="
    return jsondata['reply']


headers, headers1 = LL.req_headers()

jsondata = getBaseStructure(LL.zbotID, headers1)
print "found base structure"

BASE_URL = LL.BASE_URL

usergroups = getAllUserGroups(headers1, LL.zbotID, BASE_URL)
with open("/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/python/tmpfile", 'w') as wf:
    wf.write(usergroups)
grplist =  json.loads(usergroups)['output']['usergroup']

print grplist

print "+++++++++++++++++++++++++++++++++++"

for k, v in grplist.items():
    if "Admin PrePrimary" in k:
        grpID = str(v)
        print k, v

        url =  "https://twig.me/v1/usergroups/" + grpID + "/9J5EDAR3Y2PZA"
        method = "GET"
        body = {}
        jsondata = hit_url_method(body, headers1, method, url)
        with open('/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/rundir/tmpgrps', 'w') as wf:
            wf.write(str(jsondata))
        jsondata = json.loads(jsondata)
        jsondata = jsondata['data']['elements']
        for element in jsondata:
            if "basecard" in element['cardtype']:
                zviceID = element['tagId']
                url = "https://twig.me/v1/usergroups/" + grpID + "/user/" + zviceID + "/delete/9J5EDAR3Y2PZA"
                method = "POST"
                print "===deleting user " + element['title'] + " from the group " + str(k)
                jsondata = hit_url_method(body, headers1, method, url)
                print jsondata
        print jsondata

# url = "https://twig.me/v1/usergroups/3/user/9FBFN2U24YE4M/delete/9J5EDAR3Y2PZA"
# method = "POST"
# jsondata = hit_url_method(body, headers1, method, url)
# print jsondata

