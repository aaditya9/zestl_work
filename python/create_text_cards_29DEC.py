#!/usr/bin/python

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
# import user_groups as UG
import StringIO
import itertools
#
# import warnings
# warnings.filterwarnings("ignore")
# from urllib import urlopen
#
# from fuzzywuzzy import fuzz

import hashlib\

# import lib.login_admin as LL



akey = 'dfd8f390c6cbd8fd95c34f79aa4a9480eff582befdb1d86f0027d2703de42996d230fed3ae4c2bb59a7995d9a99c390acbee86d1fd86f20dfb72f81e0a4e5a68'
hasec = '984e6a3c9253b494d96ee364efa203d306e88b180d9c630711d4f07ce787d7ed79df0a28adc0ed5de9c8e353b4110b4f181796b563ea9776d05730399a528e3a'


def set_card_permissions(allowedusers, cardID, zviceID, acttype, headers1, ZbotID):
    BASE_URL = "https://twig.me/v4/"
    usergroups = getAllUserGroups(headers1, ZbotID, BASE_URL)
    grplist = json.loads(usergroups)['output']['usergroup']
    grpID = grplist[allowedusers]
    print grpID
    actionType = acttype
    RequestBody = {
                   "opType": "1",
                   "actionType": actionType,
                   "groupID": grpID,
                   "cardID": cardID,
                   "cardType": "GenericCard"
                   }
    # zbotID = zviceID  "interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN",
    # u'http://52.53.210.213/v4/9J5EDAR3Y2PZA'
    url = BASE_URL + 'card/permissions/' + zviceID
    response = change_view_permissions_fullurl(RequestBody, headers1, url)
    return response


# # actionType = 'MAIL'
# # RequestBody = {"interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN",
# #                "opType": "5",
# #                "actionType": actionType,
# #                "groupID": grpID,
# #                "cardID": cid,
# #                "cardType": "GenericCard"
# #                }
# # response = change_view_permissions_fullurl(RequestBody, headers1, url)
# print response

def create_txt_card(tcardname, icardDes, zviceID, headers1, parentCardID):
    body = {}
    # url = "https://twig.me/v1/fastscan/attendance/" + zviceID
    url = "https://twig.me/v4/zvice/interaction/" + zviceID

    method = "POST"
    body['Title'] = tcardname
    if parentCardID > 0:
        body['parentCardID'] = parentCardID

    body['cardData'] = {"title": tcardname, "desc": icardDes, "Flags": True}
    # body['desc'] = details['cid']
    body['cardType'] = "TEXT"
    body['opType'] = 1
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
    print body

    jsonreply = hit_url_method(body, headers1, method, url)
    print json.loads(jsonreply)
    jsonreply = json.loads(jsonreply)
    return jsonreply['cardid']



def login_user(email, pwd, BASE_URL):
    sha512pwd = hashlib.sha512(pwd).hexdigest()
    sha512apwd = hashlib.sha512(akey + hasec + email + sha512pwd).hexdigest()
    payload = {'email': email, 'password': sha512pwd}
    header = {'AKEY': akey, 'APWD': sha512apwd}
    jsonreply = invoke_rest('POST', BASE_URL + 'user/login', payload, header)
    # print jsonreply
    return jsonreply


def getMPWD(authkey_salt, timestamp, pwd):
    sha512pwd = hashlib.sha512(pwd).hexdigest()
    hpwd = hashlib.sha512(sha512pwd + authkey_salt).hexdigest()
    mpwd = hashlib.sha512(hpwd + str(timestamp) + hasec).hexdigest()
    return mpwd


def invoke_rest(request_type, rest_url, payload=None, headers=None):
    count = 1
    while True:
        try:
            api_url = rest_url
            if request_type == 'GET':
                r = requests.get(api_url, headers=headers)

                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            elif request_type == 'POST':
                r = requests.post(api_url, data=payload, headers=headers)
                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            elif request_type == 'PUT':
                r = requests.put(api_url, data=payload, headers=headers)
                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            else:
                return "Invalid request type ", request_type
        except Exception, e:
            print "Error in invoking " + request_type + ", " + api_url + ", Reattempting " + str(count)
            count = count + 1
            time.sleep(50.0 / 1000.0);  # Sleep 50 milli sec
            # return "Exception:", e, " in getting the API call"



def req_headers(email, pwd, BASE_URL):
    BASE_URL = BASE_URL
    email = email
    pwd = pwd
    jsondata = login_user(email, pwd, BASE_URL)
    if jsondata['code'] == 200:
        try:
            reply = jsondata['reply']
            json_reply = json.loads(reply)
            loginToken = json_reply['loginToken']
            authorization = json_reply['AuthKey']
            timestamp = int(time.time())
            mpwd = getMPWD(authorization, timestamp, pwd)


            headers = {'Authorization': authorization, 'LoginToken': loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey,
                   'MPWD': mpwd}
            headers1 = {'Content-type': 'application/json;charset=UTF-8', 'Authorization': authorization,
                    'LoginToken': loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey, 'MPWD': mpwd}
            return (headers, headers1)
        except KeyError:
            return (None, None)
    else:
        return (None, None)

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']



def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']



def getBaseStructure(zbotID, headers1, BASE_URL):
    url = BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    response = hit_url(RequestBody, headers1, zbotID, url)
    # with open('/Users/sujoychakravarty/Dropbox/Zestl-scripts/rundir/tmp', 'w') as f:
    #     f.write(str(response))
    return json.loads(response)


def getAllUserGroups(headers, zbotID, BASE_URL):
    jsondata = invoke_rest('GET', BASE_URL + 'usergroups/' + zbotID + "?filter={\"limit\":1000,\"offset\":0}", None, headers)
    #
    # print "User Group API response : Code : " + str(jsondata['code'])
    # print "======================="
    # print jsondata['reply']
    # print "======================="
    return jsondata['reply']


def change_view_permissions_fullurl(body, headers, BASE_URL):
    jsondata = invoke_rest('POST', BASE_URL , json.dumps(body), headers)
    return jsondata['reply']


if __name__ == "__main__":
    # args = json.loads(sys.argv[1])
    BASE_URL = "https://www.twig.me/v4/"
    email = "admin@zestl.com"

    # ipAddress = getPublicIp()
    # BASE_URL = "http://" + ipAddress + "/v1/"


    passkey = "Zspladmin99"

    # ZbotID = "B969YSR37AT7G"

    # zviceID = "5G7TAGSAERZPS"
    hasHeader = "Y"
    tagIDCol = 0
    setPermissions = False

    inputFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/AddTermReportsTextCard.csv"
    # inputFile = "/home/ec2-user/python/inputs/IndusUsers/AddTermReportsTextCard.csv"


    headers, headers1 = req_headers(email, passkey, BASE_URL)

    print "&&&&&&&&&&&&&&&&&&&&&&&"



    # print grplist['Linked Users']

    presentTag = ""
    with open(inputFile, 'r') as f:
        data = csv.reader(f, delimiter=',')
        if hasHeader == "Y":
            row1 = data.next()

        for row in data:
            zviceID = row[0].strip()
            tcardname = row[1].strip()
            try:
                icardDes = row[2].strip()
            except:
                icardDes = ""
            if setPermissions:
                allowedusers = row[3].strip()
            if zviceID != presentTag:
                presentTag = zviceID
                # ZbotID = zviceID
                jsondata = getBaseStructure(zviceID, headers1, BASE_URL)

            cardID = create_txt_card(tcardname, icardDes, zviceID)


            if setPermissions:

                response = set_card_permissions(allowedusers, cardID, zviceID, "VIEW", headers1, ZbotID)

                print response
                print "======================="
                #
                # ## set allowed users
                # url = "https://twig.me/v1/zvice/interaction/" + zviceID
                # body = {}
                # body["interactionID"] = "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN"
                # body["cardType"] = "GenericCard"
                # body["cardID"] = str(cardID)
                # body["opType"] = 5
                # body["actionType"] = "ALLOWED_USERS"
                # body["groupID"] = grpID
                # jsonreply = hit_url_method(body, headers1, method, url)
                print "+_____++++++++_________"

                # print jsonreply

                print " = = = = Created a attendance card " + tcardname + " permitting " + allowedusers + "  = = = ="
                    # print jsondata
