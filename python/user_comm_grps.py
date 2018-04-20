
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


def getAllUserGroups(headers, zbotID):
    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + zbotID, None, headers)
    #
    # print "User Group API response : Code : " + str(jsondata['code'])
    # print "======================="
    # print jsondata['reply']
    # print "======================="
    return jsondata['reply']


headers, headers1 = LL.req_headers()

usergroups = getAllUserGroups(headers1, LL.zbotID)
# print usergroups


inputFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/CommGrp_SportsTeacher.csv"
# inputFile = "/home/ec2-user/python/inputs/CommGrp_PRO.csv"
# fname = = "/home/ec2-user/python/inputs/PrePrimaryTeacherUserGroups.csv"

# ## the response is ugly - so i'll housekeep it

grpvals = json.loads(usergroups)
print "=======================****"
grps = grpvals['output']
grpname = grps['usergroup']

print "&&&&&&&&&&&&"
print grpname
print "&&&&&&&&&&&&"

with open(inputFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    # if hasHeader == "Y":
    #     row1 = data.next()
    # method = "POST"
    for row in data:

        zviceID = row[0]

        # jsondata = getBaseStructure(zviceID, headers1)
        # print jsondata
        BASE_URL = LL.BASE_URL


        print "+++++++++++++++++++++++++++++++++++"

        url =  "https://twig.me/v1/user/communication/" + zviceID + "/groups"
        method = "GET"
        body = {}
        jsondata = hit_url_method(body, headers1, method, url)
        # with open('/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/rundir/tmpgrps', 'w') as wf:
        #     wf.write(str(jsondata))
        # print jsondata
        jsondata = json.loads(jsondata)
        jsondata = jsondata['data']['elements']
        # ['data']
        # "https://twig.me/v1/user/communication/46EPXXS54FJNG/groups/1"
        for element in jsondata:
            # print element
            if element['title'] != None and row[1] in element['title']:
                print element['cardsjsonurl']
                url = element['cardsjsonurl']


        print "+++++++++++++++++++++++++++++++++++"
        print "+++++++++++++++++++++++++++++++++++"
        print "+++++++++++++++++++++++++++++++++++"
        print "+++++++++++++++++++++++++++++++++++"


        body['UserGroupID'] = grpname[row[2]]
        method = "POST"
        jsondata = hit_url_method(body, headers1, method, url)
        # with open('/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/rundir/tmpgrps', 'w') as wf:
        #     wf.write(str(jsondata))
        print jsondata


