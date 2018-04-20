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
import logon as LL
from datetime import datetime

BASE_URL = "http://35.154.64.119/v13/"  # test url
email = 'admin@zestl.com'
passkey = 'TwigMeNow'
ZbotID = "WH4ULS9BHSAKZ"
inputFile = "/home/adi/Desktop/zestl/hlt7-json/output/userinfo.csv"
result={}

createNewUser = "Y"
tagCol = 1
alt_pid=2
surnameCol=3
nameCol=4
birthdate=5
mobColumn=12

addressCol=8
zipCol=11
notename = [None] * 20
noteCol = [None] * 20
noOfNotes=4

# notename[0]="pid"
# noteCol[0]=1
# notename[1]="Alternate PID"
# noteCol[1]=2
# notename[2] = "Surname"
# noteCol[2] = 3
# notename[3] = "Gender"
# noteCol[3] = 6
# notename[4] = "Race_Id"
# noteCol[4] = 7
# notename[5] = "Address"
# noteCol[5] = 8
# notename[6] = "city"
# noteCol[6] = 9
# notename[7] = "state"
# noteCol[7] = 10
# notename[8] = "zip"
# noteCol[8] = 11
# notename[9] = "language"
# noteCol[9] = 12
# notename[10] = "Martialstatus"
# noteCol[10] = 13
# notename[12] = "Ethenic id"
# noteCol[12] = 14
# notename[13] = "Ethenic text"
# noteCol[13] = 15
# notename[14] = "Ethenic name_of_coding"
# noteCol[14] = 16

notename[0]="pid"
noteCol[0]=1
notename[1]="Alternate PID"
noteCol[1]=2
notename[2] = "Date"
noteCol[2] = 5
notename[3] = "Address"
noteCol[3] = 8

#url = BASE_URL + "org/" + ZbotID + "/user/search/moredetails?filter={\"md_header\":\"PID\",\"search\":    \"209470\"   }"
errorFile = "saptpadi_UCG.txt"
headers, headers1 = LL.req_headers(email, passkey, BASE_URL)

def update_user(user_tagid):
    with open(inputFile, "r") as rf:
        with open(errorFile, "a") as ef:
            data = csv.reader(rf, delimiter=',')
            row1=data.next()
            body={}

            for row in data:
                        # body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat', 'long': 'long',
                        #         'tagprofile': 0,
                        #         'media_type': 'image/jpg',
                        #         'media_ext': 'jpg', 'media': "", 'media_size': 0, 'zbotid': ZbotID}
                        # title = CM.force_decode(row[nameCol].strip())
                        # body['title'] = CM.force_decode(row[nameCol].strip())
                        # body['linkemail'] = ''
                        # body['autogentag'] = "true"
                        # body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"
                        #
                        # method = "POST"
                        # url = BASE_URL + 'zvice/interaction/' + ZbotID
                        # jsonreply = CM.hit_url_method(body, headers1, method, url)
                        # jsonreply = json.loads(jsonreply)
                        # print(jsonreply)
                        # zviceID = jsonreply['data']['usertagid']
                        # print zviceID
                        # #                       print(jsonreply)
                        #
                        # if jsonreply['error'] == True:
                        #     print "Error creating " + title
                        #     print jsonreply['message']
                        #     ef.write(p_id + "  ::  " + title + " :: " + jsonreply['message'] + "\n")
                        # else:
                        #     print "==========User " + title + " " + " created ==========="
                        #     print jsonreply['data']

                        #   post contact details
                        method = "POST"
                        body = {}
                        mobile = row[mobColumn].strip()
                        # address = row[addressCol].strip( url = BASE_URL + 'zvice/interaction/' + zviceID)
                        body['Contact'] = mobile
                        # body['address'] = address
                        body["interactionID"] = "CommonInteraction_INTERACTION_TYPE_MODIFY_CONTACT_INFO"
                        url = BASE_URL + 'zvice/interaction/' + user_tagid
                        jsonreply = CM.hit_url_method(body, headers1, method, url)
                     #   ef.write(user_tagid + "  ::  " + title + " :: " + jsonreply + "\n")
                        print jsonreply

                        #put notes
                        method = "PUT"
                        url = BASE_URL + 'ztag/notes_PP/' + user_tagid
                        for i in range(0, noOfNotes):
                            if noteCol[i] == -1:
                                note = ""
                            else:
                                note = row[noteCol[i]].strip()
                            tagNote = {"NoteHeader": notename[i], "Note": note};
                            body = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes',
                                    'tagnotes': json.dumps(tagNote)}
                            jsonreply = CM.hit_url_method(body, headers1, method, url)
                            print jsonreply

                          #  ef.write(zviceID + "  ::  " + title + " :: " + jsonreply + "\n")


def create_new_user(p_id):
    with open(inputFile, "r") as rf:
        with open(errorFile, "a") as ef:
            data = csv.reader(rf, delimiter=',')
            row1 = data.next()
            body = {}
    #        try:
            for row in data:
                        body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat', 'long': 'long',
                                'tagprofile': 0,
                                'media_type': 'image/jpg',
                                'media_ext': 'jpg', 'media': "", 'media_size': 0, 'zbotid':ZbotID}
                        title=CM.force_decode(row[nameCol].strip())
                        body['title'] =title
                        body['linkemail'] = ''
                        body['autogentag'] = "true"
                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"

                        method = "POST"
                        url = BASE_URL + 'zvice/interaction/' + ZbotID
                        jsonreply = CM.hit_url_method(body, headers1, method, url)
                        jsonreply = json.loads(jsonreply)
                        zviceID=jsonreply['data']['usertagid']
                        print zviceID
 #                       print(jsonreply)

                        if jsonreply['error'] == True:
                            print "Error creating " + title
                            print jsonreply['message']
                            ef.write(p_id + "  ::  " + title+ " :: " + jsonreply['message'] + "\n")
                        else:
                            print "==========User " + title + " " +  " created ==========="
                            print jsonreply['data']

                     #   post contact details
                        method = "POST"
                        body={}
                        mobile = row[mobColumn].strip()
#                        address = row[addressCol].strip( url = BASE_URL + 'zvice/interaction/' + zviceID)
                        body['Contact'] = mobile
 #                       body['address'] = address
                        body["interactionID"]="CommonInteraction_INTERACTION_TYPE_MODIFY_CONTACT_INFO"
                        url = BASE_URL + 'zvice/interaction/' + zviceID
                        jsonreply = CM.hit_url_method(body, headers1, method, url)
                        ef.write(zviceID + "  ::  " + title + " :: " + jsonreply + "\n")
                        print jsonreply


                        # #post notes
                        method = "PUT"
                        url = BASE_URL + 'ztag/notes_PP/' + zviceID
                        for i in range(0, noOfNotes):
                            if noteCol[i] == -1:
                                note = ""
                            else:
                                note = row[noteCol[i]].strip()
                            tagNote = {"NoteHeader": notename[i], "Note": note};
                            body = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes',
                                    'tagnotes': json.dumps(tagNote)}
                            jsonreply = CM.hit_url_method(body, headers1, method, url)
                            print jsonreply
                            ef.write(zviceID + "  ::  " + title + " :: " + jsonreply + "\n")

            # except:
            #     print("problem in creating new user")

def user_info(p_id):
    body={}
    url = BASE_URL + "org/" + ZbotID + "/user/search/moredetails?filter={\"md_header\":\"PID\",\"search\":" + "\"" + p_id + "\"" + "}"
    method="GET"
    #response = CM.hit_url_method(body, headers1, method, url)
    result=CM.hit_url_method(body, headers1, method, url)
    print(result)
    rr=    json.loads(result)
    user_array=rr["data"]["users"]
    print(user_array)
    # if len(user_array)!=0:
    #     user_tagid=user_array[0]
# print(user_tagid)

    if len(user_array)!=0:
        user_tagid = user_array[0]
        update_user(user_tagid)  # calling update func for update user info
    else:
        create_new_user(p_id)  # creating new  user

def main():
        with open(inputFile,"r") as rf:
            data = csv.reader(rf, delimiter=',')
            row1=data.next()
            for row in data:
                p_id=(row[tagCol].strip())
#                print p_id
        user_info(p_id)

if __name__ == '__main__':
    main()