
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
    with open('/Users/sujoychakravarty/Dropbox/Zestl-scripts/rundir/tmp', 'w') as f:
        f.write(str(response))
    return json.loads(response)

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


headers, headers1 = LL.req_headers()

zviceID = "9YFEFHP9MVYDX"
# zviceID = LL.zbotID
#
# jsondata = getBaseStructure(zviceID, headers1)
# # print jsondata


hasHeader = "Y"
tagIDCol = 0

inputFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/Pilot_Users_part1_list.csv"


with open(inputFile, 'r') as f:
    data = csv.reader(f, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    for row in data:
        zviceID = row[0].strip()
        # tcardname = row[1].strip()
        # allowedusers = row[2].strip()




        url = "https://twig.me/v1/zvice/interaction/" + zviceID
        body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_GENERIC_NOTES","notetype":"P","useclubbing":False}
        method = "POST"
        # url = "https://twig.me/v1/permissions/communication/CYE5WLGBESTAT"
        # url = "https://twig.me/v1/zvice/interaction/CYE5WLGBESTAT"
        #
        # body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_GET_CARDS_PERMISSIONS_USR_GRPS","cardType":"GenericCard","cardID":"180","actionType":"MAIL"}
        #


        jsonresponse = hit_url_method(body, headers1, method, url)
        print "++++++++ ------------- +++++++++++"

        print jsonresponse

        print "++++++++ ------------- +++++++++++"
        print "++++++++ ------------- +++++++++++"
        print "++++++++ ------------- +++++++++++"
        print "++++++++ ------------- +++++++++++"

        jsondata = json.loads(jsonresponse)
        body = {}
        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_DELETE_GENERIC_NOTE"
        # url = "https://twig.me/v1/zvice/interaction/ACTY37DGEBN6C"
        for element in jsondata['data']['elements']:
            for action in element['actions']:
                if 'Delete' in action['title']:
                    noteID =  action['inputs'][1]['properties'][1]['value']
                    body['noteid'] = noteID
                    jsonresponse = hit_url_method(body, headers1, method, url)
                    print "+++++++++ Deleting Note ++++++"
                    print jsonresponse

        # BASE_URL = LL.BASE_URL

        #
        # print "+++++++++++++++++++++++++++++++++++"
        #
        # url =  "https://twig.me/v1/usergroups/3/9J5EDAR3Y2PZA"
        # method = "GET"
        # body = {}
        # jsondata = hit_url_method(body, headers1, method, url)
        # with open('/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/rundir/tmpgrps', 'w') as wf:
        #     wf.write(str(jsondata))
        # jsondata = json.loads(jsondata)
        # jsondata = jsondata['data']['elements']
        # for element in jsondata:
        #     if "basecard" in element['cardtype']:
        #         zviceID = element['tagId']
        #         url = "https://twig.me/v1/usergroups/3/user/" + zviceID + "/delete/9J5EDAR3Y2PZA"
        #         method = "POST"
        #         print "===deleting user " + element['title']
        #         jsondata = hit_url_method(body, headers1, method, url)
        #         print jsondata
        # print jsondata

        # url = "https://twig.me/v1/usergroups/3/user/9FBFN2U24YE4M/delete/9J5EDAR3Y2PZA"
        # method = "POST"
        # jsondata = hit_url_method(body, headers1, method, url)
        # print jsondata

