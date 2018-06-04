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

import credentials as CV
#import kidzcare_paths as CV

# BASE_URL="http://54.153.24.183/v1/"
# email = 'archanahp14@gmail.com'
# pwd = 'underthesky123'

BASE_URL=CV.BASE_URL
email = CV.email
pwd = CV.pwd
zbotID = CV.zbotID

input_path=CV.inp_path
output_path=CV.out_path
outputfiles=CV.outputfiles

#ADT
adt_inp=CV.ADT_inp
adt_opt=CV.ADT_opt

adt_outfiles=CV.ADT_outputfiles


sha512pwd = hashlib.sha512(pwd).hexdigest()
akey = 'dfd8f390c6cbd8fd95c34f79aa4a9480eff582befdb1d86f0027d2703de42996d230fed3ae4c2bb59a7995d9a99c390acbee86d1fd86f20dfb72f81e0a4e5a68'
hasec = '984e6a3c9253b494d96ee364efa203d306e88b180d9c630711d4f07ce787d7ed79df0a28adc0ed5de9c8e353b4110b4f181796b563ea9776d05730399a528e3a'
sha512apwd = hashlib.sha512(akey + hasec + email + sha512pwd).hexdigest()

def login_user():
        payload = {'email': email, 'password' : sha512pwd}
        # print payload
        header = {'AKEY': akey, 'APWD': sha512apwd}
        return invoke_rest('POST', BASE_URL + 'user/login', payload, header)


def getMPWD(authkey_salt, timestamp):
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

                            to_ret = {'code':r.status_code, 'reply':r.text}
                            return to_ret
                    elif request_type == 'POST':
                            r = requests.post(api_url, data=payload, headers=headers)
                            to_ret = {'code':r.status_code, 'reply':r.text}
                            return to_ret
                    elif request_type == 'PUT':
                            r = requests.put(api_url, data=payload, headers=headers)
                            to_ret = {'code':r.status_code, 'reply':r.text}
                            return to_ret
                    else:
                            return "Invalid request type ", request_type
            except Exception, e:
                print "Error in invoking " + request_type + ", " + api_url + ", Reattempting " + str(count)
                count = count + 1
                time.sleep (50.0 / 1000.0); #Sleep 50 milli sec
                    #return "Exception:", e, " in getting the API call"
# 
# def invoke_rest(request_type, rest_url, payload=None, headers=None):
#     count = 1
#     while True:
#             try:
#                     api_url = rest_url
#                     if request_type == 'GET':
#                             # r = requests.get(api_url, headers=headers)
#                             r = requests.get(api_url, headers=headers)
#                             to_ret = {'code':r.status_code, 'reply':r.text}
#                             print "error code" + r.code()
#                             return to_ret
#                     elif request_type == 'POST':
#                             r = requests.post(api_url, data=payload, headers=headers)
#                             to_ret = {'code':r.status_code, 'reply':r.text}
#                             return to_ret
#                     elif request_type == 'PUT':
#                             r = requests.put(api_url, data=payload, headers=headers)
#                             to_ret = {'code':r.status_code, 'reply':r.text}
#                             return to_ret
#                     else:
#                             return "Invalid request type ", request_type
#             except Exception, e:
#                 print "Error in invoking " + request_type + ", " + api_url + ", Reattempting " + str(count)
#                 count = count + 1
#                 time.sleep (50.0 / 1000.0); #Sleep 50 milli sec
#                     #return "Exception:", e, " in getting the API call"
#             

def req_headers():
        jsondata = login_user()
        print jsondata
        if jsondata['code'] == 200:
            reply = jsondata['reply']
            json_reply = json.loads(reply)
            loginToken =  json_reply['loginToken']
            authorization = json_reply['AuthKey']
            timestamp = int(time.time())
            mpwd = getMPWD(authorization, timestamp)
        
            print "============================="
            print "LoginToken:" + loginToken
            print "authorization:" + authorization
            print "timestamp:" + str(timestamp)
            print "mpwd:" + mpwd
            print "============================="
        
            #headers = {'Content-type': 'application/json;charset=UTF-8', 'Authorization':authorization, 'LoginToken':loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey, 'MPWD': mpwd}
            headers = {'Authorization':authorization, 'LoginToken':loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey, 'MPWD': mpwd}
            headers1 = {'Content-type': 'application/json;charset=UTF-8', 'Authorization':authorization, 'LoginToken':loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey, 'MPWD': mpwd}
            # headers1 = {'Content-type': 'application/json;charset=UTF-8', 'Authorization':authorization, 'LoginToken':loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey, 'MPWD': mpwd}
            return (headers, headers1)
            # feed_data(headers, headers1)
