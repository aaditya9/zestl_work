#!/usr/local/bin/python
# -*- coding: utf-8 -*-

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
import common as CM
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
    # email = "manasi@zestl.com"
    passkey = "Zspladmin99"
    # passkey = "TwigMeNow"
    # BASE_URL = "http://35.154.64.11/v7/"
    BASE_URL = "https://www.twig.me/v7/"
    # ZbotID = "AY83W94K9T25L"  ### NIO
    ZbotID = "8WATL6URGUT42"  ### Bookspace_lib
    adminemail = ""

    errorFile = "errorfile.txt"
    inputFile = "C:/Users/MInal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/extra_note.csv"
    # inputFile = "/home/ec2-user/scripts/input_files/APR_15.csv"
    createNewUser = "N"
    uploadpicture = "N"
    tagCol = 0
    NameCol = -1
    emailCol = -1
    descCol = -1
    useAdminLink = "N"
    hasHeader = "Y"
    media = ""
    media_size = 0
    photo = -1
    localUpload = True


    hasmoredetails = "N"
    # mobColumn = -1
    mobColumn = 5

    hasnotes = "Y"
    notename = [None] * 20
    noteCol = [None] * 20
    noOfNotes = 3

    notename[0] = "Category"
    noteCol[0] = 1
    notename[1] = "Category_Id"
    noteCol[1] = 2
    notename[2] = "Shelf_Position1"
    noteCol[2] = 3

    headers, headers1 = req_headers(email, passkey, BASE_URL)

    body = {}
    body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat',
            'long': 'long',  'tagprofile': 0, 'media_type': 'image/jpg',
    'media_ext': 'jpg', 'media': media, 'media_size': media_size, 'zbotid': ZbotID}

    ### input management
    parseResults = CM.parse_files(inputFile)

    if parseResults == "errors":
        print "File has encoding errors"
    else:
        with open(inputFile, 'r') as rf:
            with open(errorFile, "w") as ef:

                data = csv.reader(rf, delimiter=',')
                if hasHeader == "Y":
                    row1 = data.next()
                method = "POST"
                for row in data:
                    zviceID = CM.force_decode(row[tagCol])
                    if createNewUser == "Y" or createNewUser == "y":
                        if photo > -1:
                            media = CM.force_decode(row[photo])
                        if useAdminLink == "Y":
                            emailID = adminemail
                        else:
                            if emailCol == -1:
                                emailID = ""
                            else:
                                emailID = CM.force_decode(row[emailCol])
                            # emailID = CM.force_decode(row[emailCol])
                        title = CM.force_decode(row[NameCol])
                        zviceID = CM.force_decode(row[tagCol])
                        if descCol == -1:
                            if title == "":
                                desc = "User"
                            else:
                                desc = title
                        else:
                            if row[6] != "":
                                row[6] = row[6]

                            if row[4] != "":
                                row[4] = row[4]
                                desc = CM.force_decode(row[6] + ".\n\n RegDate - " + row[4])

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
                        body['zviceid'] = zviceID
                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"

                        jsonreply = hit_url_method(body, headers1, method, url)
                        time.sleep(500.0 / 1000.0);
                        jsonreply = json.loads(jsonreply)

                        if jsonreply['error'] == True:
                            message = "Error creating " + zviceID + " : " + title + "\t" + jsonreply['message'] + "\n"
                            ef.write(message)
                            print "Error creating " + title
                            print jsonreply['message']
                        else:
                            print "==========User " + title + " " + emailID + " created ==========="
                            print jsonreply['data']

                    if uploadpicture == "Y":
                        jdata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
                        try:
                            for input1 in jdata['data']['elements'][0]['actions'][0]['inputs']:
                                for prop in input1['properties']:
                                    if prop['value'] == 'title':
                                        title = input1['properties'][1]['value']
                                    elif prop['value'] == 'desc':
                                        description =  input1['properties'][1]['value']
                        except:
                            print "couldnt get base json"



                        url = BASE_URL + 'zvice/interaction/' + zviceID
                        # body = {"moreInfo": {"Mobile number": mobile},
                        body = {"interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
                        if NameCol > -1 :
                            title = row[NameCol]
                            body["title"] = title
                        else:
                            body["title"] = title
                        if descCol > -1 :
                            desc = CM.force_decode(row[descCol])
                            body["desc"] = desc
                        else:
                            body["desc"] = description
                        if photo > -1 and localUpload == False:
                            media = CM.force_decode(row[photo])
                            body["profilepic"] = media
                        elif photo > -1 and localUpload == True:
                            try:
                                filename = CM.force_decode(row[photo])
                                with open(filename, "rb") as image_file:
                                    encoded_string = base64.b64encode(image_file.read())
                                encoded_string = encoded_string.encode('utf8')
                                # print encoded_string
                                # body = {}
                                body['media'] = encoded_string
                                body['media_type'] = "image/jpeg"
                                body['media_ext'] = "jpg"
                                body['media_size'] = 120000
                            except:
                                print "No image file specified"

                        jsonreply = hit_url_method(body, headers1, method, url)
                        print jsonreply

                    if hasmoredetails == "Y":
                        if mobColumn == '-1':
                            mobile = ''
                        else:
                            mobile = CM.force_decode(row[mobColumn])
                        method = "POST"
                        url = BASE_URL + 'zvice/interaction/' + zviceID
                        # body = {"moreInfo": {"Mobile number": mobile},
                        # body = { "interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
                        # if photo > -1:
                        #     body["profilepic"] =  media
                        # jsonreply = hit_url_method(body, headers1, method, url)
                        # print jsonreply
                        # body = {"Contact" : mobile, "EmailID" : row[emailCol], "interactionID" : "CommonInteraction_INTERACTION_TYPE_MODIFY_CONTACT_INFO"}
                        body = {"Contact": mobile ,"interactionID": "CommonInteraction_INTERACTION_TYPE_MODIFY_CONTACT_INFO"}
                        jsonreply = hit_url_method(body, headers1, method, url)
                        time.sleep(500.0 / 1000.0);
                        print jsonreply

                    if hasnotes == "Y":
                        method = "PUT"
                        url = BASE_URL + 'ztag/notes_PP/' + zviceID
                        for i in range(0, noOfNotes):
                            if noteCol[i] == -1 :
                                note = ""
                            else:
                                note = CM.force_decode(row[noteCol[i]])

                            tagNote = {"NoteHeader": notename[i], "Note": note};
                            body = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes': json.dumps(tagNote)}
                            jsonreply = hit_url_method(body, headers1, method, url)
                            print jsonreply




