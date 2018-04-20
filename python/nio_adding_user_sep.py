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
import password as PW
import common as CM

akey = 'dfd8f390c6cbd8fd95c34f79aa4a9480eff582befdb1d86f0027d2703de42996d230fed3ae4c2bb59a7995d9a99c390acbee86d1fd86f20dfb72f81e0a4e5a68'
hasec = '984e6a3c9253b494d96ee364efa203d306e88b180d9c630711d4f07ce787d7ed79df0a28adc0ed5de9c8e353b4110b4f181796b563ea9776d05730399a528e3a'


global JWT
global BASE_URL


def login_user(email, pwd):
    sha512pwd = hashlib.sha512(pwd).hexdigest()
    sha512apwd = hashlib.sha512(akey + hasec + email + sha512pwd).hexdigest()
    payload = {'email': email, 'password': sha512pwd}
    headers = {'jwt': 'true'}
    jsonreply = invoke_rest('POST', BASE_URL + 'user/login', payload, headers)
    # print jsonreply
    try:
        jwtjson = json.loads(jsonreply['reply'])
        jwt = jwtjson['loginToken']
        headers1 = {'Content-type': 'application/json;charset=UTF-8', 'jwt' : jwt}

        return headers1
    except:
        return "error"


def getMPWD(authkey_salt, timestamp, pwd):
    sha512pwd = hashlib.sha512(pwd).hexdigest()
    hpwd = hashlib.sha512(sha512pwd + authkey_salt).hexdigest()
    mpwd = hashlib.sha512(hpwd + str(timestamp) + hasec).hexdigest()
    return mpwd


def invoke_rest(request_type, rest_url, payload=None, headers=None):
    headers1 = {}
    headers1 = headers
    count = 1
    while True:
        try:
            api_url = rest_url
            if request_type == 'GET':
                r = requests.get(api_url, headers=headers1)

                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            elif request_type == 'POST':
                r = requests.post(api_url, data=payload, headers=headers1)
                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            elif request_type == 'PUT':
                r = requests.put(api_url, data=payload, headers=headers1)
                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            else:
                return "Invalid request type ", request_type
        except Exception, e:
            print "Error in invoking " + request_type + ", " + api_url + ", Reattempting " + str(count)
            count = count + 1
            time.sleep(50.0 / 1000.0);  # Sleep 50 milli sec
            # return "Exception:", e, " in getting the API call"



def req_headers(email, pwd):
    # BASE_URL = BASE_URL
    email = email
    pwd = pwd
    jsondata = login_user(email, pwd)
    return jsondata
    # if jsondata['code'] == 200:
    #     try:
    #         reply = jsondata['reply']
    #         json_reply = json.loads(reply)
    #         loginToken = json_reply['loginToken']
    #         authorization = json_reply['AuthKey']
    #         timestamp = int(time.time())
    #         mpwd = getMPWD(authorization, timestamp, pwd)
    #
    #
    #         headers = {'Authorization': authorization, 'LoginToken': loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey,
    #                'MPWD': mpwd}
    #         headers1 = {'Content-type': 'application/json;charset=UTF-8', 'Authorization': authorization,
    #                 'LoginToken': loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey, 'MPWD': mpwd}
    #         return (headers, headers1)
    #     except KeyError:
    #         return (None, None)
    # else:
    #     return (None, None)

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
    adminemail = ""
    # BASE_URL = "http://twig-me.com/v1/"
    # BASE_URL = "https://www.twig.me/v13/"  ### Production
    BASE_URL ="http://www.twig-me.com/v13/" ## dev server
    # BASE_URL = "http://35.154.64.11/v8/"    ###Test
    email = 'admin@zestl.com'
    passkey = "TwigMeNow"
    # passkey = PW.pwd
    # email = 'manasi@zestl.com'
    # passkey = 'zestl123'
    # passkey = 'TwigMeNow'
    # ZbotID = "XVL5PPENFYRN2" ## Fiber Fitness
    # ZbotID = "XBEER2UPJ4KN2"    #Banglore Indus
    # ZbotID = "BP35PXQDYZ3F6" ## Saptpadi
    # ZbotID = "B5MMNKYM8JWGT"  ## Unique Multi-specialty Hospital
    # ZbotID = "AYX6T62MU62D4"   ## lavasa Intit
    # ZbotID = "2HRKLHBPPYXSN"  ## Zestl
    # ZbotID = "876MD568TAUH2"    ##MINAL Test
    # ZbotID = "EGV228Q8N9HM3"    ## sayali test
    # ZbotID = "B969YSR37AT7G" ####INDUS
    # ZbotID = "AQPWC94SXRC8V"   # PrograMitra
    # ZbotID = "DKV9YUW3MY68K"
    # ZbotID = "9J5EDAR3Y2PZA"  ### Millenium
    # ZbotID = "EYBC2NFB8BJ4C"
    # ZbotID = "2G59JWRQDTHXZ"  #### KPCA2 fy
    # ZbotID = "EYBC2NFB8BJ4C"    ###Vrushali
    # ZbotID = "8SFBUKFZCALEE"  ### Golds Gym
    # ZbotID = "5AGURR84SUC2K" ### VKA
    # ZbotID = "8SSLEZVJXHTSA"    #Oxford Jiggly Kids
    # ZbotID = "4R3W683S6F3U6"    ###SMP Reality
    # ZbotID = "WPQMNBNMN4PXD"    ###Nandan Gumaste
    # ZbotID = "AY83W94K9T25L"    ### NIO
    # ZbotID = "2N4N5HQ6P9YK8"    ##Phoenix sports club
    # ZbotID = "82YXAC9BJX686"    #### Biggest Looses Wins
    # ZbotID = "AKSZFSQR8BUPX"   ### Slimwell Fitness studio
    # ZbotID = "EYF5BNLC8JTQF"    #### Studio Elements
    # ZbotID = "WPQMNBNMN4PXD"    # Nandan Gumaste
    # ZbotID = "EYBC2NFB8BJ4C"  # VSC
    # ZbotID = "82YXAC9BJX686"    #Biggest Loosers
    # ZbotID = "5ADXHJJ8B9PH3"    #The Story Station
    # ZbotID = "8SFKZCV5PFAXV"    #MInal Prod
    # ZbotID = "5WRSD3YBC62QH"    #Summer
    # ZbotID = "6KX4PVHCYAAJ8"    # satara road gold gym
    # ZbotID = "9J5EDAR3Y2PZA"    #Millennium
    # ZbotID = "3TMECHKDYA7CH"    # indus hydrabad
    # ZbotID = "87ZWFB9AKKCK8"    # humpy A2
    ZbotID = "83H6LVUBRXWZ5"    # Future grp (dev server)
    # ZbotID = "X9FYBNR8PUL9A"    # Army Public School

    # inputFile = "C:/Users/user/Dropbox/Zestl-scripts/python/tmpfile"
    # inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
    # inputFile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/scrip t_inputs/try1.csv"SaptapadiUsers_19March
    # inputFile = "/home/ec2-user/scripts/input_files/NIO_SEP.csv"
    # inputFile = "C:/Users/user/Dropbox/Zestl-scripts/python/tmpfile"
    path = "/Users/sujoychakravarty/Downloads/"
    inputFile = path + "NewFGUserAddition.csv"
    outFile = path + "NewFGUserAdditiontags.csv"


# =======
#     email = "admin@zestl.com"
#     passkey = "Zspladmin99"
#     BASE_URL = "https://www.twig.me/v4/"
#     adminemail = "drivers@zestl.com"
#     ZbotID = "9KTT97HP4ZX3A"

    #### structure of the input file

    createNewUser = "Y"

    uploadpicture = "N"

    tagCol = 0
    NameCol = 0
    emailCol = 1
    descCol = 2
    useAdminLink = "Y"
    hasHeader = "Y"
    media = ""
    media_size = 0
    photo = -1

    errorFile = "saptpadi_UCG.txt"
    hasmoredetails = "Y"
    mobColumn = -1
    hasnotes = "N"

    notename = [None] * 20
    noteCol = [None] * 20
    noOfNotes = -1

    notename[0] = "Grade & Section"
    noteCol[0] = 2
    notename[1] = "Date Of Birth"
    noteCol[1] = 3
    notename[2] = "Address"
    noteCol[2] = 6
    notename[3] = "Father Info"
    noteCol[3] = 4
    notename[4] = "Mother Info"
    noteCol[4] = 5
    # notename[5] = "Address"
    # noteCol[5] = 8
    # notename[6] = "SMS No"
    # noteCol[6] = 15
    # notename[7] = "Email ID registered with school"
    # noteCol[7] = 17
    # notename[8] = "Bus Route No"
    # noteCol[8] = 16
    # notename[9] = "DAY BOARDING/ONLY SCHOOL"
    # noteCol[9] = 20
    # notename[10] = "Father First Name"
    # noteCol[10] = 7
    # notename[11] = "Mother First Name"
    # noteCol[11] = 8
    # notename[12] = "QR - parent ID"
    # noteCol[12] = 1
    # notename[13] = "Status"
    # noteCol[13] = 2
    # notename[14] = "REF no of sibling if in school"
    # noteCol[14] = 18
    # notename[15] = "Regular/RTE"
    # noteCol[15] = 19

    # login
    headers1 = req_headers(email, passkey)




    body = {}
    body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat',
            'long': 'long',  'tagprofile': 0, 'media_type': 'image/jpg',
    'media_ext': 'jpg', 'media': media, 'media_size': media_size, 'zbotid': ZbotID}

    ### input management


    with open(outFile, 'wb') as wf:
        csvwrite = csv.writer(wf, delimiter=',')

        with open(inputFile, 'r') as rf:
            with open(errorFile, "a") as ef:
                data = csv.reader(rf, delimiter=',')
                if hasHeader == "Y":
                    row1 = data.next()
                method = "POST"

                counter = 0
                for row in data:

                    counter += 1
                    print counter
                    zviceID = CM.force_decode(row[tagCol].strip())
                    if createNewUser == "Y" or createNewUser == "y":
                        if photo > -1:
                            media = CM.force_decode(row[photo])
                        if useAdminLink == "Y":
                            emailID = adminemail
                        else:
                            if emailCol == -1:
                                emailID = ""
                            else:
                                emailID = CM.force_decode(row[emailCol].strip())
                        title = CM.force_decode(row[NameCol].strip())
                        zviceID = CM.force_decode(row[tagCol].strip())
                        if descCol == -1:
                            if title == "":
                                desc = "User"
                            else:
                                desc = title
                        else:
                            desc = CM.force_decode(row[descCol].strip())
                        method = "POST"

                        # result = CM.add_user_InBusiness(body['BusinessTag'], title, emailID, headers1, BASE_URL)
                        # # result = '{"error":false,"message":"","error_code":-1,"data":{"usertagid":"EJSWWXDFF4B6G","elements":null,"disableExpandToolbar":true},"title":"Future Group","toolbarbgimgurl":"https:\/\/s3-ap-south-1.amazonaws.com\/dev-zestl-4\/1507537696_556864179_FutureConsumerWhiteBg%5B1%5D.png","isBusiness":true,"homeurl":"http:\/\/www.twig-me.com\/v11\/zvice\/detailscard\/WHGJ7HTVTDFH3","homemethod":"POST","homejsondata":null,"businesstagid":"WHGJ7HTVTDFH3","users":[{"usertagid":"33PQMYD4N77DP","usertagtitle":"Super Admin User"},{"usertagid":"FJBSBPYQMRZZN","usertagtitle":"ALL","selected":true}],"bottom_bar":[{"title":"My Reports","icon":"ic_action_timelapse","url":"Test","method":"GET","jsonData":null},{"title":"My Tasks","icon":"ic_action_dns","url":"http:\/\/twig-me.com\/v13\/user\/tasks\/get\/WHGJ7HTVTDFH3","method":"GET","jsonData":null},{"title":"My Projects","icon":"ic_action_dashboard","url":"http:\/\/twig-me.com\/v13\/myworkflows\/WHGJ7HTVTDFH3","method":"GET","jsonData":null},{"title":"My Team","icon":"ic_action_group","url":"http:\/\/www.twig-me.com\/v13\/usergroups\/business\/user\/","method":"GET","jsonData":null},{"title":"Workflow","icon":"ic_action_open_in_browser","url":"http:\/\/twig-me.com\/v11\/workflow\/WHGJ7HTVTDFH3\/cards","method":"GET","jsonData":null},{"title":"L My Projects","icon":"ic_action_local_offer","url":"http:\/\/twig-me.com\/lankesh\/v13\/myworkflows\/WHGJ7HTVTDFH3","method":"GET","jsonData":null}]}'
                        # jsonreply = json.loads(result)
                        # user_id = jsonreply['data']['usertagid']


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
                        # body['zviceid'] = zviceID
                        body['autogentag'] = "true"

                        # body['zviceid'] = "5EUVCWNTLCKB2"

                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"
                        # body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zviceinfo': desc, 'zvicelink': 'NEW', 'lat': 'lat',
                        #         'long': 'long', 'zbotid': ZbotID, 'title': title, 'tagprofile': 0, 'media_type': 'image/jpg',
                                # 'media_ext': 'jpg', 'media': media, 'media_size': media_size}

                        jsonreply = hit_url_method(body, headers1, method, url)
                        # print jsonreply
                        # time.sleep(500.0 / 1000.0);
                        jsonreply = json.loads(jsonreply)
                        if jsonreply['error'] == True:
                            print "Error creating " + title
                            print jsonreply['message']
                            zviceID = ""
                            ef.write(zviceID + "  ::  "+ title + " :: " + jsonreply['message'] + "\n")
                        else:
                            print "==========User " + title + " " + emailID + " created ==========="
                            # print jsonreply['data']
                            zviceID = jsonreply['data']['usertagid']

                            writearray = [zviceID]
                            writearray.extend(row)
                            csvwrite.writerow(writearray)

                            print zviceID + "\n"

            # print counter
                # for counter in data:
                #     if jsonreply['data'] == True:
                #         print "done"

                    if uploadpicture == "Y":
                        url = BASE_URL + 'zvice/interaction/' + zviceID
                        # body = {"moreInfo": {"Mobile number": mobile},
                        body = {"interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
                        method = "POST"
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
                        ef.write(zviceID + "  ::  " + title + " :: " + jsonreply + "\n")

                    if hasmoredetails == "Y":
                        body = {}
                        if mobColumn == -1:
                            mobile = ''

                        else:
                            mobile = row[mobColumn].strip()
                            body["Contact"] = mobile
                        method = "POST"
                        if emailCol == -1:
                            email = ""
                        else:
                            body["EmailID"] = row[emailCol].strip()

                        url = BASE_URL + 'zvice/interaction/' + zviceID
                        # body = {"moreInfo": {"Mobile number": mobile},
                        # body = { "interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
                        # if photo > -1:
                        #     body["profilepic"] =  media
                        # jsonreply = hit_url_method(body, headers1, method, url)
                        # print jsonreply
                        body["interactionID"] = "CommonInteraction_INTERACTION_TYPE_MODIFY_CONTACT_INFO"
                        jsonreply = hit_url_method(body, headers1, method, url)
                        ef.write(zviceID + "  ::  " + title + " :: " + jsonreply + "\n")
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
                            jsonreply = hit_url_method(body, headers1, method, url)
                            print jsonreply
                            ef.write(zviceID + "  ::  " + title + " :: " + jsonreply + "\n")