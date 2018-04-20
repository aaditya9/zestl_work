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
import StringIO
import itertools

import warnings
warnings.filterwarnings("ignore")
from urllib import urlopen

from fuzzywuzzy import fuzz

import hashlib\

# import lib.login_admin as LL



akey = 'dfd8f390c6cbd8fd95c34f79aa4a9480eff582befdb1d86f0027d2703de42996d230fed3ae4c2bb59a7995d9a99c390acbee86d1fd86f20dfb72f81e0a4e5a68'
hasec = '984e6a3c9253b494d96ee364efa203d306e88b180d9c630711d4f07ce787d7ed79df0a28adc0ed5de9c8e353b4110b4f181796b563ea9776d05730399a528e3a'



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


def getPublicIp():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    # data = '<html><head><title>Current IP Check</title></head><body>Current IP Address: 65.96.168.198</body></html>\r\n'

    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)




def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


args = json.loads(sys.argv[1])
BASE_URL = "http://www.twig-me.com/v7/"
# ipAddress = getPublicIp()
# BASE_URL = "http://" + ipAddress + "/v1/"

# with open("/opt/provision/temp", 'w') as wf:
#     wf.write(str(args))

passkey = args['password']
response = {}
response['success'] = True
response["error"] = ''
response["data"] = "<h1>A response here</h1>"


headers, headers1 = req_headers("admin@zestl.com", passkey, "http://www.twig-me.com/v7/")


reqTag  = 0
#  = > $_POST['pCustomerName'],
#  = > $_POST['pNewCustomer'],
#  = > $_POST['pNoOfTags'],
#  = > $_POST['pExtraTags'],
# 'primary_itag' = > $
# _POST['pPrimaryITag'],
# 'secondary_itag' = > $_POST['pSecondaryITag'],
# ];


CustomerName = args['customer_name']
if(args['new_customer'] == "Y"):
    addTags = 1
else :
    addTags = 2
# addTags = int(raw_input("Do you want to \n 1) add a new curtomer  OR \n 2) add more tags to an existing customer\n : "))
if addTags != 1 and addTags != 2:
    sys.exit("illegal input")

NeedTags = 'N'
Maxtags = args['no_of_tags']
if(args['extra_tags'] == 'Y'):
    NeedTags = 'Y'
else:
    NeedTags = 'N'



if NeedTags == 'Y' or NeedTags == 'y':
    reqTag  = args['no_of_extra_tags']



Cname = re.sub('[\W_]+', '', CustomerName)
# print Cname
# print Maxtags
if addTags == 1:
    data = {}
    responseData = {}

    body = { "DisplayName": Cname, "MaxAllowedTags": Maxtags}

    url = BASE_URL +  "customers"
    method = "POST"

    jsonreply = hit_url_method(body, headers1, method, url)
#    with open("/opt/provision/temp", 'w') as wf:
 #       wf.write(str(jsonreply))

    # print jsonreply
    jsondata =  json.loads(jsonreply)
    ZbotID =  jsondata['data'][0]['ZbotID']

    responseData['customerName'] = CustomerName
    responseData['zbotID'] =  ZbotID

    # ZbotID = 'A4CJ2VHTTJS9Y'

    url = BASE_URL + "zvice/register_pre"
    body = {"zviceid" : ZbotID, "title" : CustomerName,  "zvicetype" : "ZTAG", "zviceinfo" : "enter description here", "category" : "ORGANISATION",  "lat" : 'lat', "long" : "long", "zviceloc" : '--', "zvicelink" : 'NEW'}

    method = "PUT"

    jsonreply = hit_url_method(body, headers1, method, url)
    response['data'] = "<h1> Customer Name : " + CustomerName + "</h1><h1> Tag ID : " + ZbotID + "</h1><h1> Server IP address : " + BASE_URL + "</h1>"
  # response['data'] = responseData


if addTags == 2:
    method = "GET"
    url = BASE_URL + 'customers'
    body = {}
    # print " .... Working ....."
    jsonreply = hit_url_method(body, headers1, method, url)
    jsonreply = json.loads(jsonreply)
    for elements in jsonreply['data']:
        # print elements['mapped_customers']
        try:
            for cust in elements['mapped_customers']:
                if fuzz.partial_ratio(CustomerName, cust['Title']) > 96:
                    # confirm = str(raw_input("Is \"" + cust['Title'] +" \" the customer you are interested in : "))
                    # if confirm == 'y' or confirm == 'Y':
                    ZbotID = cust['ZbotID']
        except KeyError:
            # print "keyerror"
            sys.exit(response)
# else:
#     print "---------------------------"

if NeedTags == 'Y' or NeedTags == 'y':
    url = BASE_URL + "nexttag/" + ZbotID + "/tags/" + str(reqTag)
    method = "GET"
    body = {}
    jsonreply = hit_url_method(body, headers1, method, url)
    jsonreply = json.loads(jsonreply)
    tagIDs = " ".join(str(x) for x in jsonreply['available_tagIDs'])
    response['data'] += "<h1> Extra tags : " + tagIDs
    # print jsonreply

if addTags == 2:
    method = "GET"
    url = BASE_URL + 'customers'
    body = {}
    # print " .... Working ....."
    jsonreply = hit_url_method(body, headers1, method, url)
    jsonreply = json.loads(jsonreply)
    for elements in jsonreply['data']:
        # print elements['mapped_customers']
        try:
            for cust in elements['mapped_customers']:
                if fuzz.partial_ratio(CustomerName, cust['Title']) > 95:
                    # confirm = str(raw_input( "Do you want to change \"" + cust['Title'] + "\" maximum number of tags from " + str(elements['MaxAllowedTags']) + " to " + str(Maxtags) + ": " ))
                    # if confirm == 'y' or confirm == 'Y':
                    body['DisplayName'] = elements['DisplayName']
                    body['MaxAllowedTags'] = Maxtags
                    body['ZbotID'] = cust['ZbotID']
                    url = BASE_URL + "customers/" + str(elements['CustomerID'])
                    method = "PUT"
                        # print cust['ZbotID']
                    jsonreply = hit_url_method(body, headers1, method, url)
                        # print jsonreply

        except KeyError:
            print "keyerror"

print json.dumps(response)
