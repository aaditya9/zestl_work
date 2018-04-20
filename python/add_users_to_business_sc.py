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
import re
import sys
import csv
import hashlib
import csv
import pprint
import argparse

# import lib.login_prod as LL
# import common_functions as CF



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



if __name__ == '__main__':
    #### identity section
    email = "admin@zestl.com"
    passkey = "zsplADMIN999"
    BASE_URL = "https://www.twig.me/v11/"
    adminemail = ""
    ZbotID = "B969YSR37AT7G"


    inputFile = "/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/millennium/script_inputs/NewTeachers-indus-24aug.csv"

#     Kunte_mayurOUT.csv
#
# Kunte_pycOUT.csv
#
# Kunte_walveOUT.csv
#
# Kunte_aundhOUT.csv


    #### structure of the input file

    tagCol = -1
    NameCol = 0
    emailCol = 4
    descCol = 3
    useAdminLink = "N"
    hasHeader = "Y"
    media = ""
    media_size = 0
    photo = -1

    hasmoredetails = "Y"
    mobColumn = -1

    hasnotes = "Y"
    notename = [None] * 20
    noteCol = [None] * 20
    noOfNotes = 4

    notename[0] = "Bus Route"
    noteCol[0] = 5
    notename[1] = "Gender"
    noteCol[1] = 6
    notename[2] = "Date Of Birth"
    noteCol[2] = 1
    notename[3] = "Date of Joining"
    noteCol[3] = 2
    notename[4] = "Blood Group"
    noteCol[4] = 8
    notename[5] = "House"
    noteCol[5] = 17
    notename[6] = "Phone"
    noteCol[6] = 13
    notename[7] = "Status"
    noteCol[7] = 11
    notename[8] = "School Package ID"
    noteCol[8] = 14
    notename[9] = "Parent QR code"
    noteCol[9] = 16
    notename[10] = "Drop Bus Route number"
    noteCol[10] = 10



    # login
    headers, headers1 = req_headers(email, passkey, BASE_URL)

    body = {}
    body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat',
            'long': 'long',  'tagprofile': 0, 'media_type': 'image/jpg',
    'media_ext': 'jpg', 'media': media, 'media_size': media_size, 'zbotid': ZbotID}

    ### input management
    with open(inputFile, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        if hasHeader == "Y":
            row1 = data.next()
        method = "POST"
        for row in data:
            if photo > -1:
                media = row[photo]
            if useAdminLink == "Y":
                emailID = adminemail
            else:
                emailID = row[emailCol]
            title = row[NameCol]
            # zviceID = row[tagCol]
            zviceID = ""
            if descCol == -1:
                if title == "":
                    desc = "User"
                else:
                    desc = title
            else:
                desc = row[descCol]
            method = "POST"
            url = BASE_URL + 'zvice/interaction/' + ZbotID
            body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat',
                    'long': 'long', 'tagprofile': 0, 'media_type': 'image/jpg',
                    'media_ext': 'jpg', 'media': media, 'media_size': media_size, 'zbotid': ZbotID}
            if title == "":
                body['title'] = zviceID
            else:
                body['title'] = title
            body['linkemail'] = emailID
            body['zviceinfo'] = desc
            body['zviceid'] = ""
            body['autogentag'] = "true"
            # body['zviceid'] = "5EUVCWNTLCKB2"

            body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"
            # body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zviceinfo': desc, 'zvicelink': 'NEW', 'lat': 'lat',
            #         'long': 'long', 'zbotid': ZbotID, 'title': title, 'tagprofile': 0, 'media_type': 'image/jpg',
                    # 'media_ext': 'jpg', 'media': media, 'media_size': media_size}

            jsonreply = hit_url_method(body, headers1, method, url)
            jsonreply = json.loads(jsonreply)
            if jsonreply['error'] == True:
                print "Error creating " + title
                print jsonreply['message']
            else:
                print "==========User " + title + " " + emailID + " created ==========="
                print jsonreply['data']
                zviceID = jsonreply['data']['usertagid']

            if hasmoredetails == "Y":
                if mobColumn == '-1':
                    mobile = ''
                else:
                    mobile = row[mobColumn]
                method = "POST"
                url = BASE_URL + 'zvice/interaction/' + zviceID
                body = {"moreInfo": {"Mobile number": mobile},
                 "interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG", "title": title,
                 "desc": desc, "profilepic" : media}
                jsonreply = hit_url_method(body, headers1, method, url)
                print jsonreply
                body = {"Contact" : mobile, "EmailID" : row[emailCol], "interactionID" : "CommonInteraction_INTERACTION_TYPE_MODIFY_CONTACT_INFO"}
                jsonreply = hit_url_method(body, headers1, method, url)
                print jsonreply

            if hasnotes == "Y":
                method = "PUT"
                url = BASE_URL + 'ztag/notes_PP/' + zviceID
                for i in range(0, noOfNotes):

                    tagNote = {"NoteHeader": notename[i], "Note": row[noteCol[i]]};
                    body = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes': json.dumps(tagNote)}
                    jsonreply = hit_url_method(body, headers1, method, url)
                    print jsonreply




