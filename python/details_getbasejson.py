
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
    with open('C:/Users/user/Dropbox/Zestl-scripts/rundir/tmp', 'w') as f:
        f.write(str(response))
    return json.loads(response)

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


headers, headers1 = LL.req_headers()

# zviceID = "2HRKLHBPPYXSN"
# zviceID = LL.zbotID
inputFile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\Indus_22Nov.csv"
newFile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\Indus_detail.csv"
with open(newFile, 'w') as a:
    with open(inputFile, 'r') as vlist:
        data = csv.reader(vlist, delimiter=',')
        i = 0
        for row in data:
            zviceID = row[0]
            jsondata = getBaseStructure(zviceID, headers1)
            for element in jsondata['data']['elements']:
                if 'basecard' in element['cardtype']:
                    name = element['title']
                if 'Link to TwigMe User' in element['title']:
                    dataTagID =  json.loads(element['actions'][1]['data'])['tagIds'][0]
                    # print "--------------------------"

            url = "https://twig.me/v1/zvice/basecard/"
            method = "POST"
            data = {"tagIds": [dataTagID]}

            jsondata = hit_url_method(data, headers1, method, url)

            print "********************************"
            jsondata = json.loads(jsondata)
            print name + "," + jsondata['data']['elements'][0]['title'] + "\n"



            a.write( name + "," + jsondata['data']['elements'][0]['title'] + "\n")

            print "********************************"



#
# url = "https://twig.me/v1/zvice/interaction/ACTY37DGEBN6C"
# body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_GENERIC_NOTES","notetype":"P","useclubbing":False}
# method = "POST"
# # url = "https://twig.me/v1/permissions/communication/CYE5WLGBESTAT"
# # url = "https://twig.me/v1/zvice/interaction/CYE5WLGBESTAT"
# #
# # body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_GET_CARDS_PERMISSIONS_USR_GRPS","cardType":"GenericCard","cardID":"180","actionType":"MAIL"}
# #
#
#
# jsonresponse = hit_url_method(body, headers1, method, url)
# print "++++++++ ------------- +++++++++++"
#
# print jsonresponse
#
# print "++++++++ ------------- +++++++++++"
# print "++++++++ ------------- +++++++++++"
# print "++++++++ ------------- +++++++++++"
# print "++++++++ ------------- +++++++++++"
#
# jsondata = json.loads(jsonresponse)
# for element in jsondata['data']['elements']:
#     for action in element['actions']:
#         if 'Delete' in action['title']:
#             print action['inputs'][1]['properties'][1]['value']
#
# BASE_URL = LL.BASE_URL
#
# #
# # print "+++++++++++++++++++++++++++++++++++"
# #
# # url =  "https://twig.me/v1/usergroups/3/9J5EDAR3Y2PZA"
# # method = "GET"
# # body = {}
# # jsondata = hit_url_method(body, headers1, method, url)
# # with open('/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/rundir/tmpgrps', 'w') as wf:
# #     wf.write(str(jsondata))
# # jsondata = json.loads(jsondata)
# # jsondata = jsondata['data']['elements']
# # for element in jsondata:
# #     if "basecard" in element['cardtype']:
# #         zviceID = element['tagId']
# #         url = "https://twig.me/v1/usergroups/3/user/" + zviceID + "/delete/9J5EDAR3Y2PZA"
# #         method = "POST"
# #         print "===deleting user " + element['title']
# #         jsondata = hit_url_method(body, headers1, method, url)
# #         print jsondata
# # print jsondata
#
# # url = "https://twig.me/v1/usergroups/3/user/9FBFN2U24YE4M/delete/9J5EDAR3Y2PZA"
# # method = "POST"
# # jsondata = hit_url_method(body, headers1, method, url)
# # print jsondata
#
