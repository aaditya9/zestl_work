#!/usr/local/bin/python

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
import sys
import hashlib
import csv

import lib.login_generic as LL





def updateDetails(headers, body, zviceID):
    return LL.invoke_rest('POST', BASE_URL + 'zvice/interaction/' + zviceID, body, headers)

def getMembershipDetails(BASE_URL, ZviceID, headers1):
    url = BASE_URL + "zvice/interaction/" + ZviceID
    body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_STATIC_DETAILS"}
    method = "POST"
    jsonreply = hit_url_method(json.dumps(body), headers1, method, url)
    return jsonreply


def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, body, headers)
    return jsondata['reply']


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']
# def feed_data(headers, headers1):
#
#     zbotID = LL.zbotID
#
#     # i like input files specified on command line
#     file_fd = open(sys.argv[1],'r')
#     token=list(file_fd)
#     b=list()
#                 # REF. NO.(0)    ACADYEAR(1)    STUDNAME(2)    CLASS(3)    DIVISIONNAME(4)    ROLL NO(5) BUS(6)    DOB(7)
#                 #BLOOD GRP(8)    HOUSE(9)    ADDRESS(10)    PHONE1(11)    PHONE2(12)    EMAIL(13)    PHOTOPATH(14)    TWIGMETAG(15)
#     for i in range(len(token)):
#         b.append(token[i].split("\t"))
#     for i in range(0,len(token)):
#         if len(b[i][0])>0:
#
#             tagEncID = b[i][15].rstrip()
#             title = b[i][2] + ' [' + b[i][0] + ']'
#             desc = b[i][3] + b[i][4] + "\nBus Route:" + b[i][6]
#             loc = 'Millenium'
#
#             data = json.dumps({"moreInfo": {"Address":"","Address2":"","Address1":"","Mobile number":""},"interactionID":"CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG","title": title,"desc": desc})
#             print tagEncID
#             result_json = updateDetails(headers1, data, tagEncID)
#             print result_json


def feed_data(headers, title, desc, ZviceID, BASE_URL):
    data = json.dumps({ "interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG", "title": title, "desc": desc})
    return LL.invoke_rest('POST', BASE_URL + 'zvice/interaction/' + ZviceID, data, headers)
            # print tagEncID
    # result_json = updateDetails(headers1, data, tagEncID)
    # print result_json


def getBaseStructure(zbotID, headers1, BASE_URL):
    url = BASE_URL + 'zvice/detailscard/' + zbotID
    print "$^%^&%*^&*^&^*^&*^&^*&^"
    print (url, zbotID)
    RequestBody = {}
    response = hit_url(RequestBody, headers1, zbotID, url)
    with open('/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/rundir/tmp', 'w') as f:
        f.write(str(response))
    return json.loads(response)


def modifyMembershipDetailsValid(BASE_URL, ZviceID, headers1, validity):
    body ={}
    url = BASE_URL + 'zvice/interaction/' + ZviceID
    body['columnid'] = "ID_Validity"
    body['validupto'] = validity
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_MODIFY_ZVICESTATIC_INFO"
    method = "POST"
    response = hit_url_method(json.dumps(body), headers1, method, url)
    return response

def modifyMembershipDetailsType(BASE_URL, ZviceID, headers1, type):
    body = {}
    url = BASE_URL + 'zvice/interaction/' + ZviceID
    body['columnid'] = "ID_Type"
    body['membershiptype'] = type
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_MODIFY_ZVICESTATIC_INFO"
    method = "POST"
    response = hit_url_method(json.dumps(body), headers1, method, url)
    return response





if __name__ == '__main__':
    ### credentials
    email = "archanahp14@gmail.com"
    pwd = "zestl123"
    ZbotID = "A4CJ2VHTTJS9Y"
    BASE_URL = "https://www.twig.me/v1/"
    fname = "/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/millennium/script_inputs/uts_userdetails.csv"
    # today = "2016-07-23"

    headers, headers1 = LL.req_headers(email, pwd, ZbotID, BASE_URL)
    # headers, headers1 = LL.req_headers()
    # print headers
    # jsonreply = getBaseStructure(ZviceID, headers1, BASE_URL)
    # print "***********Base structure written to temp file ***********"

    # jsonreply = getMembershipDetails(BASE_URL, ZviceID, headers1)
    # print "++++++++++++++++++++++++++++++++++++++++++"
    # print "++++++++++++++++++++++++++++++++++++++++++"
    # print "++++++++++++++++++++++++++++++++++++++++++"
    # print "membership details"


    with open(fname, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        for row in data:
            print row


            ZviceID = row[1]
            validity = row[3]
            jsonreply = modifyMembershipDetailsValid(BASE_URL, ZviceID, headers1, validity)
            print "===================="
            print jsonreply
            print "+++++++++++++++++"

            type = row[4]
            jsonreply = modifyMembershipDetailsType(BASE_URL, ZviceID, headers1, type)
            print "===================="
            print jsonreply
            print "+++++++++++++++++"

            title = row[0]
            desc = row[2]
            jsonreply = feed_data(headers1, title, desc, ZviceID, BASE_URL)
            print "===================="
            print json.loads(jsonreply['reply'])['message']
            print "+++++++++++++++++"

            # feed_data(headers, headers1)
