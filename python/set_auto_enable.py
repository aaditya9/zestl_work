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
import common as CM
import hashlib\

akey = 'dfd8f390c6cbd8fd95c34f79aa4a9480eff582befdb1d86f0027d2703de42996d230fed3ae4c2bb59a7995d9a99c390acbee86d1fd86f20dfb72f81e0a4e5a68'
hasec = '984e6a3c9253b494d96ee364efa203d306e88b180d9c630711d4f07ce787d7ed79df0a28adc0ed5de9c8e353b4110b4f181796b563ea9776d05730399a528e3a'


# def set_card_permissions(allowedusers, cardID, zviceID, acttype, headers1, ZbotID, BASE_URL):
def set_card_permissions(cardID, zviceID, acttype, headers1, ZbotID, BASE_URL,policyval):

    policyType = acttype
    RequestBody = {
                   #"opType": "1",
                   "policyType": policyType,
                   "policyVal": policyval,
                   # "groupID": grpID,
                   "cardID": cardID,
                   "cardType": "GenericCard"
                   }

    url = 'https://twig.me/v5/cards/policy/9YZ2HAZE4B5TN'
    url = BASE_URL + 'card/permissions/' + zviceID

    url = BASE_URL + 'cards/policy/' + zviceID
    response = change_view_permissions_fullurl(RequestBody, headers1, url)
    return response

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
    # BASE_URL = "http://35.154.64.11/v5/"
    # SERVER = "http://35.154.64.11/"
    BASE_URL = "https://twig.me/v5/"  ### prodddddddddddddddddddd
    email = "admin@zestl.com"
    passkey = "Zspladmin99"
    # passkey = "TwigMeNow"

    headers, headers1 = req_headers(email, passkey, BASE_URL)

    print "&&&&&&&&&&&&&&&&&&&&&&&"
    # infile = "/home/ec2-user/python/inputs/Dhanaji_Team_Structure_Projects_p1.csv"
    # zbotFile = "/home/ec2-user/scripts/input_files/sujoy/first_4_usr_permission.csv"
    zbotFile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/spare_1st_try.csv"
    # spare_1st_try.csv
    hasHeaders = True
    with open(zbotFile, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        if hasHeaders:
            row1 = data.next()
        for row in data:
            zviceID = row[0]
            jsondata11 = CM.getBaseStructure(zviceID, headers1, BASE_URL)
            ############# i think you havent understood what we are doing.

            for a in jsondata11['data']['elements']:
                title = "Workout Plan"
                if title in a['title']:
                    parentCardID = json.loads(a['ctjsondata'])['parentCardID']
                    url = a['cturl']
                    body = json.loads(a['ctjsondata'])
                    method = "POST"
                    ja = CM.hit_url_method(body, headers1, method, url)
                    print "Found 1st level"

                    for ac in json.loads(ja)['data']['elements']:
                        if "Monday" in ac['title']:
                            print "2nd level"

                            data1 = json.loads(ac['content'])
                            cardID = data1['formID']
                            print cardID

                            ### wait . open the xls and show me where allowed users needs to be set. go to your script to that card.. allowed users set to Linked users... great show me where you are setting the other things for that cardin your script
                            ### 1st i have to go to allowed user.
                            #### please go to your script where you set "View"
                            # data1 = json.loads(ac['data'])
                            # cardID = data1['cardID']  what do you need?.... it is not working.. please show me
                            response = set_card_permissions(cardID, zviceID, "AUTO_UPDATE_CARD_MAIL", headers1,"8SFBUKFZCALEE", BASE_URL,"true")
                            print response
                            #et_card_permissions(cardID, zviceID, acttype, headers1, ZbotID, BASE_URL,policyval):
                            # url = "https://twig.me/v5/permissions/communication/9YZ2HAZE4B5TN"
#### why new file? i am trying to write fuction for this. why new file?... i will try then copy in old file
  #