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
    passkey = "Zspladmin99"
    # passkey = "TwigMeNow"
    # BASE_URL = "http://35.154.64.11/v5/"
    BASE_URL = "https://www.twig.me/v4/"
    # adminemail = "iisp@zestl.com"
    # ZbotID = "B969YSR37AT7G"
    # ZbotID = "876MD568TAUH2" ## Minal test
    ZbotID = "AY83W94K9T25L"  ### NIO

    errorFile = "errorfile.txt"

    # inputFile = "/home/ec2-user/python/inputs/VSC-KR.csv"
    # inputFile = "/home/ec2-user/python/inputs/Pilot_Users_part1_more.csv"
    # inputFile = "/home/ec2-user/python/inputs/IndusUsers/TwigmeUserDataIGCSE.csv"
    # / home / ec2 - user / python / inputs
    # inputFile = ""
    # inputFile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/full_script_try_jan_1st_user.csv"
    inputFile = "/home/ec2-user/scripts/input_files/APR_15.csv"

#     Kunte_mayurOUT.csv:w

#
# Kunte_pycOUT.csv
#
# Kunte_walveOUT.csv
#
# Kunte_aundhOUT.csv


    #### structure of the input file

    createNewUser = "Y"

    uploadpicture = "N"

    tagCol = 0
    NameCol = -1
    # emailCol = -1
    emailCol = -1
    descCol = 3
    useAdminLink = "N"
    hasHeader = "Y"
    media = ""
    media_size = 0
    # photo = 12
    photo = -1
    localUpload = True


    hasmoredetails = "Y"
    # mobColumn = -1
    mobColumn = 12

    hasnotes = "N"
    notename = [None] * 20
    noteCol = [None] * 20
    noOfNotes = -1

    notename[0] = "age"
    noteCol[0] = 4
    notename[1] = "Bus Route"
    noteCol[1] = 4
    notename[2] = "Gender"
    noteCol[2] = 5
    notename[3] = "Boarder / Day Scholar"
    noteCol[3] = 6
    notename[4] = "DOB"
    noteCol[4] = 7
    notename[5] = "Father's Name and Contact Details"
    noteCol[5] = 8
    notename[6] = "Mothers's Name and Contact Details"
    noteCol[6] = 9
    notename[7] = "Guardian's Name and Contact Details"
    noteCol[7] = 10
    notename[8] = "Address"
    noteCol[8] = 11
    notename[9] = "Email of father"
    noteCol[9] = 16
    notename[10] = "Known allergies and medical conditions"
    noteCol[10] = 10
    notename[11] = "Academic Year"
    noteCol[11] = 6
    notename[11] = "Class"
    noteCol[11] = 7
    notename[12] = "Division Name"
    noteCol[12] = 8
    notename[13] = "Date Of Birth"
    noteCol[13] = 11




    # login
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
                        title = CM.force_decode(row[2]+" (MRD - "+row[1]+")")
                        zviceID = CM.force_decode(row[tagCol])
                        if descCol == -1:
                            if title == "":
                                desc = "User"
                            else:
                                desc = title
                        else:
                            if row[4] != "":
                                row[4] = row[4] + ", "

                            if row[5] != "":
                                row[5] = row[5] + ", "

                            if row[6] != "":
                                row[6] = row[6] + ", "

                            if row[7] != "":
                                row[7] = row[7] + ", "

                            if row[8] != "":
                                row[8] = row[8] + ", "

                            if row[9] != "":
                                row[9] = row[9] + ", "

                            if row[10] != "":
                                row[10] = row[10] + " "

                            if row[11] != "":
                                row[11] = "- " + row[11]

                            if row[3] != "":
                                row[3] = row[3]
                                desc = CM.force_decode(row[4] + row[5] + row[6] + row[7] + row[8] + row[9] + row[10] + row[11] + ".\n\n RegDate - " + row[3])

                            # desc = CM.force_decode(row[descCol])
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
                        # body['zviceid'] = "5EUVCWNTLCKB2"

                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"
                        # body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zviceinfo': desc, 'zvicelink': 'NEW', 'lat': 'lat',
                        #         'long': 'long', 'zbotid': ZbotID, 'title': title, 'tagprofile': 0, 'media_type': 'image/jpg',
                                # 'media_ext': 'jpg', 'media': media, 'media_size': media_size}

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




