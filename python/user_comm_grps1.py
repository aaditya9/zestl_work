
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
    with open('/Users/Minal Thorat/Dropbox/Zestl-share/scripts/rundir/tmp', 'w') as f:
        f.write(str(response))
    return json.loads(response)

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']

def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']

def getAllUserGroups(headers, zbotID):
    # jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + zbotID, None, headers)
    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + zbotID + "?filter={\"limit\":1000,\"offset\":0}",None, headers)

    # print "User Group API response : Code : " + str(jsondata['code'])
    # print "======================="
    # print jsondata['reply']
    # print "======================="
    return jsondata['reply']

# def getAllUserGroups(headers, zbotID,val):
#     val1 = '"' + val + '"'
#     # jsondata = invoke_rest('GET', BASE_URL + 'usergroups/' + zviceID + "?filter={\"limit\":10000,\"offset\":0,\"groupname\":\"COEHOD\"}" , None, headers)
#     jsondata = LL.invoke_rest('GET',LL.BASE_URL + 'usergroups/' + zbotID + "?filter={\"limit\":10000,\"offset\":0,\"groupname\":" + val1 + "}",None, headers)
#     # jsondata = invoke_rest('GET', BASE_URL + 'usergroups/' + zviceID ,None, headers)
#     return jsondata['reply']



headers, headers1 = LL.req_headers()

usergroups = getAllUserGroups(headers1, LL.zbotID)
print usergroups

inputFile = "/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
errorFile = "indus_UCG.txt"
# ## the response is ugly - so i'll housekeep it

grpvals = json.loads(usergroups)
print "=======================****"
grps = grpvals['output']
grpname = grps['usergroup']

with open(inputFile, 'r') as rf:
    with open(errorFile, "a") as ef:
        data = csv.reader(rf, delimiter=',')
        counter = 0
        for row in data:
            zviceID = row[0].strip()
            print "Working for this zviceID : " + zviceID
            # val = row[2]
            # usergroups = getAllUserGroups(headers1, LL.zbotID,val)
            # print usergroups
            # grpvals = json.loads(usergroups)
            # # print "=======================****"
            # grps = grpvals['output']
            # grpname = grps['usergroup']

            counter += 1
            print counter
            # jsondata = getBaseStructure(zviceID, headers1)
            # print jsondata
            BASE_URL = LL.BASE_URL
            # print "+++++++++++++++++++++++++++++++++++"
            url =  "https://twig.me/v13/user/communication/" + zviceID + "/groups"
            method = "GET"
            body = {}
            jsondata = hit_url_method(body, headers1, method, url)
            jsondata = json.loads(jsondata)
            jsondata = jsondata['data']['elements']
            for element in jsondata:
                if element['title'] != None and row[1] in element['title']:
                    print element['cardsjsonurl']
                    url = element['cardsjsonurl']

            print "+++++++++++++++++++++++++++++++++++"
            body['UserGroupID'] = grpname[row[2]]
            method = "POST"
            jsondata = hit_url_method(body, headers1, method, url)
            print jsondata
            ef.write(zviceID+ "  ::  " + jsondata + "\n")