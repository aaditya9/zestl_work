
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
    print jsondata
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


def change_view_permissions_fullurl(body, headers, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL , json.dumps(body), headers)
    return jsondata['reply']

headers, headers1 = LL.req_headers()

zviceID = "D7Y9768TMU5TH"
# zviceID = LL.zbotID
inputFile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\uservrushali_OR.csv"


usergroups = getAllUserGroups(headers1, LL.zbotID, LL.BASE_URL)
# with open("C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\tmp_usergrp", 'w') as wf:
#     wf.write(usergroups)
grplist =  json.loads(usergroups)['output']['usergroup']
#

with open(inputFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    for row in data:
        zviceID = row[0]
        jsondata = getBaseStructure(zviceID, headers1)

        cards = []

        for element in jsondata['data']['elements']:
            # print element['title']
            cards.append(element['title'])

        print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        print cards
        for item in cards:
            if cards.count(item) > 1:
                print zviceID + "  :  "  + item + "  :  " + str(cards.count(item))
                jsondata = getBaseStructure(zviceID, headers1)
                for element in jsondata['data']['elements']:
                    if item in element['title']:
                        # print element['actions'][3]['actions'][2]['title']
                        url = element['actions'][3]['actions'][2]['actionUrl']
                        method = element['actions'][3]['actions'][2]['method']
                        body = {}
                        galleryId = re.sub(r'.*gallery/(\d+)', r'\1', url)
                        url = element['actions'][3]['actions'][2]['actionUrl']
                        print " -------------- delete ---------------"
                        print "Deleting " + galleryId + " in user " + zviceID
                        print " -------------- delete ---------------"
                        body['GalleryID'] = int(galleryId)
                        jsonreply = hit_url_method(body, headers1, method, url)
                        print json.loads(jsonreply)

                body = {}

                url = "https://twig.me/v1/" + zviceID + "/gallery"

                method = "POST"
                body = {"Title": "My Photos", "Description": "Photo Gallery"}

                jsonreply = hit_url_method(body, headers1, method, url)
                print json.loads(jsonreply)
                jsonreply = json.loads(jsonreply)
                cardID = jsonreply['cardid']
                grpID = grplist['Linked Users']
                print grpID
                actionType = 'VIEW'
                RequestBody = {"interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN",
                               "opType": "1",
                               "actionType": actionType,
                               "groupID": grpID,
                               "cardID": cardID,
                               "cardType": "GenericCard"
                               }
                zbotID = zviceID
                url = LL.BASE_URL + 'zvice/interaction/' + zviceID
                response = change_view_permissions_fullurl(RequestBody, headers1, url)
                print response
                actionType = "ADMIN"
                RequestBody = {"interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN",
                               "opType": "1",
                               "actionType": actionType,
                               "groupID": grpID,
                               "cardID": cardID,
                               "cardType": "GenericCard"
                               }
                url = LL.BASE_URL + 'zvice/interaction/' + zviceID
                response = change_view_permissions_fullurl(RequestBody, headers1, url)
                print response

        if cards.count("My Photos") < 1:
            print zviceID + "  :  Does not contain My Photos"
            body = {}

            url = "https://twig.me/v1/" + zviceID + "/gallery"

            method = "POST"
            body = {"Title": "My Photos", "Description": "Photo Gallery"}

            jsonreply = hit_url_method(body, headers1, method, url)
            print json.loads(jsonreply)
            jsonreply = json.loads(jsonreply)
            cardID = jsonreply['cardid']
            grpID = grplist['Linked Users']
            print grpID
            actionType = 'VIEW'
            RequestBody = {"interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN",
                           "opType": "1",
                           "actionType": actionType,
                           "groupID": grpID,
                           "cardID": cardID,
                           "cardType": "GenericCard"
                           }
            zbotID = zviceID
            url = LL.BASE_URL + 'zvice/interaction/' + zviceID
            response = change_view_permissions_fullurl(RequestBody, headers1, url)
            print response
            actionType = "ADMIN"
            RequestBody = {"interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN",
                           "opType": "1",
                           "actionType": actionType,
                           "groupID": grpID,
                           "cardID": cardID,
                           "cardType": "GenericCard"
                           }
            url = LL.BASE_URL + 'zvice/interaction/' + zviceID
            response = change_view_permissions_fullurl(RequestBody, headers1, url)
            print response


# print jsondata

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
