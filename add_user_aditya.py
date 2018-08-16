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
import common_aditya as CM
import logon as LL
import login1 as LP
import logging
from datetime import datetime

#BASE_URL = "http://35.154.64.119/v13/"  # test url
#email = 'admin@zestl.com'
#passkey = 'TwigMeNow'
#ZbotID = "WH4ULS9BHSAKZ"


BASE_URL=LP.BASE_URL
email=LP.email
passkey=LP.pwd
ZbotID=LP.zbotID
form_ID=7082
#inputFile = "/home/adi/Desktop/zestl/hlt7-json/output/userinfo.csv"
result={}

createNewUser = "Y"
tagCol = 1
alt_pid=2
surnameCol=3
nameCol=4
birthdate=5
mobColumn=9

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
# noteCol[4]=9
# noteCol[5]=10
# noteCol[6]=11

#url = BASE_URL + "org/" + ZbotID + "/user/search/moredetails?filter={\"md_header\":\"PID\",\"search\":    \"209470\"   }"
errorFile = "saptpadi_UCG.txt"
headers, headers1 = LL.req_headers(email, passkey, BASE_URL)

def update_user(inputFile,user_tagid):
    with open(inputFile, "r") as rf:
        with open(errorFile, "a") as ef:
            data = csv.reader(rf, delimiter=',')
         #   row1=data.next()
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
                            print('ALready created !!')
                            print jsonreply

                          #  ef.write(zviceID + "  ::  " + title + " :: " + jsonreply + "\n")

                        # :{"Cmd": "form-submit", "BusinessTag": "FWSMGL6USVKDW", "FormID": "7082",
                        #   "FormTitle": "User Master", "FormSubmissionID": 7126,
                        #   "FormData": {"Patient name": "user 6 test", "PID": "7700",
                        #                "Address": "621 UBER WAILEA HOPE MILLS NC 28348", "Alternate ID": null,
                        #                "Contact No. ": null, "Parent Name": null, "Email": null,
                        #                "User ID": "95KYGDN6BTFV3"}, "SubmittedBy": "66C4U8H3U585T", "tags": [],
                        #   "url_params": []}
                        #

                        try:
                            pid = row[noteCol[0]].strip()
                        except:
                            pid=" "

                        try:
                            aid = row[noteCol[1]].strip()
                        except:
                            aid= " "

                        try:
                            u_name = row[nameCol].strip() + ' ' + row[surnameCol].strip()
                        except:
                            u_name= " "
                        # address = row[noteCol[3]].strip() + " " + row[noteCol[4]].strip() + " " + row[
                        #     noteCol[5]].strip() + " " + row[
                        #               noteCol[6]].strip()

                        try:
                            address = row[noteCol[3]].strip()
                        except:
                            address = " "

                        inputdata = {"Patient name": u_name,
                                     "PID": pid,
                                     "Contact No. ": mobile,
                                     "Address": address,
                                     "Alternate ID": aid,
                                     "User ID": user_tagid    # USER TAGID
                                     }

                        result = CM.form_submission_using_NEW_API(LL.BASE_URL, ZbotID, headers1, form_ID, inputdata)


def create_new_user(inputFile,p_id):
    with open(inputFile, "r") as rf:
        with open(errorFile, "a") as ef:
            data = csv.reader(rf, delimiter=',')
         #   row1 = data.next()
            body = {}
    #        try:
            for row in data:
                        body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat', 'long': 'long',
                                'tagprofile': 0,
                                'media_type': 'image/jpg',
                                'media_ext': 'jpg', 'media': "", 'media_size': 0, 'zbotid':ZbotID}
                        title=CM.force_decode(row[3]) + " " + CM.force_decode(row[4]) + ' ' +"("+  CM.force_decode(row[1])+")"
                        #title=CM.force_decode(row[nameCol].strip())
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

                        pid=row[noteCol[0]].strip()
                        aid = row[noteCol[1]].strip()
                        #u_name = row[nameCol].strip() + ' ' + row[surnameCol].strip()
                        # address = row[noteCol[3]].strip() + " " + row[noteCol[4]].strip() + " " + row[
                        #     noteCol[5]].strip() + " " + row[
                        #               noteCol[6]].strip()
                        address=row[noteCol[3]].strip()
                        inputdata = {"Patient name": title,
                                     "PID": pid,
                                     "Contact No. ": mobile,
                                     "Address": address,
                                     "Alternate ID": aid,
                                     "User ID": zviceID  # USER TAGID
                                     }

                        result = CM.form_submission_using_NEW_API(BASE_URL, ZbotID, headers1, form_ID, inputdata)
                        logging.warning(result)
                        logging.warning('FORM SUBMITTED !!')



            # except:
            #     print("problem in creating new user")

def user_info(inputFile,p_id):
    body={}
    url = BASE_URL + "org/" + ZbotID + "/user/search/moredetails?filter={\"md_header\":\"PID\",\"search\":" + "\"" + p_id + "\"" + "}"
    method="GET"
    #response = CM.hit_url_method(body, headers1, method, url)
    result=CM.hit_url_method(body, headers1, method, url)
    print(result)
    rr=    json.loads(result)
    user_array=rr["data"]["users"]
    print(user_array)

    if len(user_array)!=0:
        user_tagid = user_array[0]
        update_user(inputFile,user_tagid)  # calling update func for update user info
    else:
        create_new_user(inputFile,p_id)  # creating new  user

def adduser_main(inputFile):
        with open(inputFile,"r") as rf:
            data = csv.reader(rf, delimiter=',')
       #     row1=data.next()
            for row in data:
                p_id=(row[tagCol].strip())
#                print p_id
        user_info(inputFile,p_id)

# if __name__ == '__main__':
#     main()