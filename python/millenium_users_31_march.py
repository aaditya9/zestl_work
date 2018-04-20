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
import password as PP

akey = 'dfd8f390c6cbd8fd95c34f79aa4a9480eff582befdb1d86f0027d2703de42996d230fed3ae4c2bb59a7995d9a99c390acbee86d1fd86f20dfb72f81e0a4e5a68'
hasec = '984e6a3c9253b494d96ee364efa203d306e88b180d9c630711d4f07ce787d7ed79df0a28adc0ed5de9c8e353b4110b4f181796b563ea9776d05730399a528e3a'

def login_user(email, pwd, BASE_URL):
    sha512pwd = hashlib.sha512(pwd).hexdigest()
    sha512apwd = hashlib.sha512(akey + hasec + email + sha512pwd).hexdigest()
    payload = {'email': email, 'password': sha512pwd}
    header = {'AKEY': akey, 'APWD': sha512apwd}
    jsonreply = invoke_rest('POST', BASE_URL + 'user/login', payload, header)
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
    email = "admin@zestl.com"
    passkey = PP.pwd
    BASE_URL = "https://www.twig.me/v8/"
    ZbotID = "9J5EDAR3Y2PZA"
    errorFile = "mill_new.txt"
    # inputFile = "/home/ec2-user/scripts/input_files/millenium_update_users_4April.csv"
    inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_users.csv"
    createNewUser = "Y"
    uploadpicture = "N"
    tagCol = 0
    NameCol = 5
    emailCol = 16
    descCol = 2
    useAdminLink = "N"
    hasHeader = "Y"
    media = ""
    media_size = 0
    photo = -1
    localUpload = True
    hasmoredetails = "Y"
    mobColumn = 12

    hasnotes = "Y"
    notename = [None] * 20
    noteCol = [None] * 20
    noOfNotes = 16

    notename[0] = "Student Standard"
    noteCol[0] = 9
    notename[1] = "Student Division"
    noteCol[1] = 10
    notename[2] = "Student DOB"
    noteCol[2] = 8
    notename[3] = "Student Blood Group"
    noteCol[3] = 13
    notename[4] = "House"
    noteCol[4] = 17
    notename[5] = "Student Roll No"
    noteCol[5] = 11
    notename[6] = "SMS No"
    noteCol[6] = 12
    notename[7] = "Email ID registered with school"
    noteCol[7] = 16
    notename[8] = "Bus Route No"
    noteCol[8] = 14
    notename[9] = "DAY BOARDING/ONLY SCHOOL"
    noteCol[9] = 20
    notename[10] = "Father First Name"
    noteCol[10] = 6
    notename[11] = "Mother First Name"
    noteCol[11] = 7
    notename[12] = "QR - parent ID"
    noteCol[12] = 1
    notename[13] = "Status"
    noteCol[13] = 15
    notename[14] = "REF no of sibling if in school"
    noteCol[14] = 18
    notename[15] = "Regular/RTE"
    noteCol[15] = 19

    headers, headers1 = req_headers(email, passkey, BASE_URL)

    body = {}
    body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat',
            'long': 'long',  'tagprofile': 0, 'media_type': 'image/jpg',
    'media_ext': 'jpg', 'media': media, 'media_size': media_size, 'zbotid': ZbotID}
with open(errorFile, 'a') as ef:
    with open(inputFile, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        if hasHeader == "Y":
            row1 = data.next()
        counter = 0
        for row in data:
            counter += 1
            print counter
            zviceID = CM.force_decode(row[tagCol].strip())
            print "Working for this Zvice ID :- " + zviceID

            if createNewUser == "Y" or createNewUser == "y":
                if photo > -1:
                    media = row[photo]
                if useAdminLink == "Y":
                    emailID = adminemail
                else:
                    if emailCol == -1:
                        emailID = ""
                    else:
                        emailID = row[emailCol].strip()
                title = CM.force_decode(row[NameCol].strip())
                zviceID = CM.force_decode(row[tagCol].strip())
                if descCol == -1:
                    if title == "":
                        desc = "User"
                    else:
                        desc = title
                else:
                    desc = CM.force_decode(row[9].strip() + row[10].strip()+ "\n" + "Bus Route : "+row[14])
                method = "POST"
                url = BASE_URL + 'zvice/interaction/' + ZbotID
                body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat',
                        'long': 'long', 'tagprofile': 0, 'media_type': 'image/jpg',
                        'media_ext': 'jpg', 'media': media, 'media_size': media_size, 'zbotid': ZbotID}
                if title == "":
                    body['title'] = zviceID
                else:
                    body['title'] = title
                # if emailID != "":
                # mobile = row[mobColumn]
                body['linkemail'] = emailID
                body['zviceinfo'] = desc
                body['zviceid'] = zviceID
                # body['zviceid'] = "5EUVCWNTLCKB2"

                body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"
                # body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zviceinfo': desc, 'zvicelink': 'NEW', 'lat': 'lat',
                #         'long': 'long', 'zbotid': ZbotID, 'title': title, 'tagprofile': 0, 'media_type': 'image/jpg',
                        # 'media_ext': 'jpg', 'media': media, 'media_size': media_size}

                jsonreply = hit_url_method(body, headers1, method, url)
                # time.sleep(500.0 / 1000.0);
                jsonreply = json.loads(jsonreply)
                if jsonreply['error'] == True:
                    print "Error creating " + title
                    print jsonreply['message']
                    ef.write("Error creating : " + title + " : " + zviceID + "\n")
                else:
                    print "==========User " + title + " " + emailID + " created ==========="
                    print jsonreply['data']
                    # ef.write(jsonreply['data'])

            if uploadpicture == "Y":
                method = "POST"
                # body = {}
                url = BASE_URL + 'zvice/interaction/' + zviceID
                body = {"interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
                if NameCol > -1 :
                    title = CM.force_decode(row[NameCol])
                    body["title"] = title
                if descCol > -1 :
                    desc = CM.force_decode(row[10].strip()+row[11].strip() + "\n" +"Bus Route : " +row[14].strip())
                    body["desc"] = desc
                if photo > -1:
                    media = row[photo]
                    body["profilepic"] = media
                print body
                jsonreply = hit_url_method(body, headers1, method, url)
                print jsonreply
                # time.sleep(5000.0 / 1000.0);

            if hasmoredetails == "Y":
                body = {}
                if mobColumn == -1:
                    mobile = ''

                else:
                    mobile = CM.force_decode(row[mobColumn].strip())
                    body["Contact"] = mobile

                if emailCol == -1:
                    email = ""
                else:
                    body["EmailID"] = CM.force_decode(row[emailCol].strip())
                method = "POST"
                url = BASE_URL + 'zvice/interaction/' + zviceID
                body["interactionID"] = "CommonInteraction_INTERACTION_TYPE_MODIFY_CONTACT_INFO"
                # print body
                jsonreply = hit_url_method(body, headers1, method, url)
                # time.sleep(5000.0 / 1000.0);
                ef.write(jsonreply + "\n")
                print jsonreply

            if hasnotes == "Y":
                method = "PUT"
                url = BASE_URL + 'ztag/notes_PP/' + zviceID
                for i in range(0, noOfNotes):
                    if noteCol[i] == -1 :
                        note = ""
                    else:
                        note = CM.force_decode(row[noteCol[i]].strip())

                    tagNote = {"NoteHeader": notename[i], "Note": note};
                    body = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes': json.dumps(tagNote)}
                    # print body
                    jsonreply = hit_url_method(body, headers1, method, url)
                    ef.write(jsonreply + "\n")
                    # time.sleep(1000.0 / 1000.0);
                    print jsonreply