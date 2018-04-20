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
# <<<<<<< HEAD
    # email = "manasi@zestl.com"
    # passkey = "Zestl123"
    # BASE_URL = "https://www.twig.me/v1/"
    # adminemail = "vsc@zestl.com"
    # adminemail = "iisp@zestl.com"
    # adminemail =  "vka@zestl.com"
    # adminemail = "kpca@zestl.com"
    # adminemail = "oxford@zestl.com"
    # adminemail = "goldsgym@gmail.com"
    # BASE_URL = "http://twig-me.com/v1/"
    BASE_URL = "https://www.twig.me/v1/"  ### Production
    # BASE_URL = "http://35.154.64.11/v1/"    ###Test
    # email = 'admin@zestl.com'
    # passkey = 'TwigMeNow'
    # passkey = 'Zspladmin99'
    email = 'manasi@zestl.com'
    passkey = "zestl123"
    # ZbotID = "876MD568TAUH2"    ##MINAL Test
    # ZbotID = "B969YSR37AT7G" ####INDUS
    # ZbotID = "DKV9YUW3MY68K"
    # ZbotID = '9J5EDAR3Y2PZA'  ### Millenium
    # ZbotID = "EYBC2NFB8BJ4C"
    # ZbotID = "2G59JWRQDTHXZ"  #### KPCA
    ZbotID = "EYBC2NFB8BJ4C"    ###Vrushali
    # ZbotID = "8SFBUKFZCALEE"  ### Golds Gym
    # ZbotID = "5AGURR84SUC2K" ### VKA
    # ZbotID = "8SSLEZVJXHTSA"    #Oxford Jiggly Kids
    # ZbotID = "4R3W683S6F3U6"    ###SMP Reality
    # ZbotID = "WPQMNBNMN4PXD"    ###Nandan Gumaste
    # ZbotID = "AY83W94K9T25L"    ### NIO
    # ZbotID = "XVL5PPENFYRN2" ## fiber fitness
    errorFile = "errorfile.txt"

    # inputFile = "C:/Users/user/Dropbox/Zestl-scripts/python/tmpfile"
    inputFile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/vsc_try_9jan.csv"
    # inputFile = "C:/Users/user/Dropbox/Zestl-scripts/python/tmpfile"
# =======
#     email = "admin@zestl.com"
#     passkey = "Zspladmin99"
#     BASE_URL = "https://www.twig.me/v4/"
#     adminemail = "drivers@zestl.com"
#     ZbotID = "9KTT97HP4ZX3A"
#
#     inputFile = "/home/ec2-user/python/inputs/VSC-KR.csv"
#     inputFile = "/home/ec2-user/python/inputs/Pilot_Users_part1_more.csv"
#     inputFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/drivers.csv"
# >>>>>>> 759a935472b9a1a42258b58d29b5482a44fff032
    # / home / ec2 - user / python / inputs
 #   inputFile = "/home/ec2-user/python/inputs/VSC-KR.csv"
  #  inputFile = "/home/ec2-user/python/inputs/Pilot_Users_part1_more.csv"
#     Kunte_mayurOUT.csv
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
    NameCol = 1
# <<<<<<< HEAD
#     emailCol = 3
#     descCol = 3
# =======
    emailCol = 7
    descCol = 9
# >>>>>>> 759a935472b9a1a42258b58d29b5482a44fff032
    useAdminLink = "N"
    hasHeader = "Y"
    media = ""
    media_size = 0
    photo = -1


    hasmoredetails = "Y"
    mobColumn = 6

    hasnotes = "Y"

# <<<<<<< HEAD
# =======
#     hasnotes = "N"
# >>>>>>> 759a935472b9a1a42258b58d29b5482a44fff032
    notename = [None] * 20
    noteCol = [None] * 20
    noOfNotes = 5

    # notename[0] = "Bus Route"
    notename[0] = "Birth Date"
    noteCol[0] = 2
    notename[1] = "Joining Date"
    noteCol[1] = 3
    notename[2] = "Last Date"
    noteCol[2] = 4
    notename[3] = "Program"
    noteCol[3] = 5
    notename[4] = "Branch"
    noteCol[4] = 8
    # notename[5] = "RF.NO"
    # noteCol[5] = 11
    # notename[6] = "Details of Father"
    # noteCol[6] = 13
    # notename[7] = "Mobile number of father"
    # noteCol[7] = 14
    # notename[8] = "Email of mother"
    # noteCol[8] = 15
    # notename[9] = "Email of father"
    # noteCol[9] = 16
    # notename[10] = "Known allergies and medical conditions"
    # noteCol[10] = 17
    # notename[11] = "Academic Year"
    # noteCol[11] = 18
    # notename[11] = "Class"
    # noteCol[11] = 19
    # notename[12] = "Division Name"
    # noteCol[12] = 20
    # notename[13] = "Date Of Birth"
    # noteCol[13] = 21

    # login
    headers, headers1 = req_headers(email, passkey, BASE_URL)

    body = {}
    body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat',
            'long': 'long',  'tagprofile': 0, 'media_type': 'image/jpg',
    'media_ext': 'jpg', 'media': media, 'media_size': media_size, 'zbotid': ZbotID}

    ### input management
    with open(inputFile, 'r') as rf:
        with open(errorFile, "w") as ef:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            method = "POST"

            counter = 0
            for row in data:

                counter += 1
                print counter
                zviceID = row[tagCol]
                if createNewUser == "Y" or createNewUser == "y":
                    if photo > -1:
                        media = row[photo]
                    if useAdminLink == "Y":
                        emailID = adminemail
                    else:
                        emailID = row[emailCol]
                    title = row[NameCol]
                    zviceID = row[tagCol]
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
                    body['zviceid'] = zviceID
                    # body['zviceid'] = "5EUVCWNTLCKB2"

                    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"
                    # body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zviceinfo': desc, 'zvicelink': 'NEW', 'lat': 'lat',
                    #         'long': 'long', 'zbotid': ZbotID, 'title': title, 'tagprofile': 0, 'media_type': 'image/jpg',
                            # 'media_ext': 'jpg', 'media': media, 'media_size': media_size}

                    jsonreply = hit_url_method(body, headers1, method, url)
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
                    url = BASE_URL + 'zvice/interaction/' + zviceID
                    # body = {"moreInfo": {"Mobile number": mobile},
                    body = {"interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
                    if NameCol > -1 :
                        title = row[NameCol]
                        body["title"] = title
                    if descCol > -1 :
                        desc = row[descCol]
                        body["desc"] = desc
                    if photo > -1:
                        media = row[photo]
                        body["profilepic"] = media
                    jsonreply = hit_url_method(body, headers1, method, url)
                    print jsonreply

                if hasmoredetails == "Y":
                    body = {}
                    if mobColumn == -1:
                        mobile = ''

                    else:
                        mobile = row[mobColumn]
                        body["Contact"] = mobile
                    method = "POST"
                    if emailCol == -1:
                        email = ""
                    else:
                        body["EmailID"] = row[emailCol]

                    url = BASE_URL + 'zvice/interaction/' + zviceID
                    # body = {"moreInfo": {"Mobile number": mobile},
                    # body = { "interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
                    # if photo > -1:
                    #     body["profilepic"] =  media
                    # jsonreply = hit_url_method(body, headers1, method, url)
                    # print jsonreply
                    body["interactionID"] = "CommonInteraction_INTERACTION_TYPE_MODIFY_CONTACT_INFO"
                    jsonreply = hit_url_method(body, headers1, method, url)
                    print jsonreply

                if hasnotes == "Y":
                    method = "PUT"
                    url = BASE_URL + 'ztag/notes_PP/' + zviceID
                    for i in range(0, noOfNotes):
                        if noteCol[i] == -1 :
                            note = ""
                        else:
                            note = row[noteCol[i]]

                        tagNote = {"NoteHeader": notename[i], "Note": note};
                        body = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes': json.dumps(tagNote)}
                        jsonreply = hit_url_method(body, headers1, method, url)
                        print jsonreply