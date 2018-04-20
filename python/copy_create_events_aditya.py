#!/usr/local/bin/python

# usage create_groups.py <file_containing_grpnames_to_create>
# ensure the file dev_millennium.py in the lib directory is configured correctly

import json
import sys
import csv
import requests
import urllib2

import hashlib
import lib.login1 as LL
import common as CM
import add_user_aditya as AU

headers, headers1 = LL.req_headers()
inputfile = "/home/adi/Downloads/TwigMeScripts-master/hlt7-json/siu/output/userinfo1.csv"

hasHeader = 'Y'
notename = [None] * 20
noteCol = [None] * 20
noOfNotes=4

notename[0]="pid"
noteCol[0]=1
notename[1]="Alternate PID"
noteCol[1]=12
notename[2] = "Date"
noteCol[2] = 17
notename[3] = "Address"
noteCol[3] = 16


ZbotID = "WH4ULS9BHSAKZ"
# EYP / EYP\:\ Academic\ and \ Activity\ Calendar /
cardname = "Calendar new"
# calendar = "Grade 10: Academic and Activity Calendar"
# calendar = "Calendar Grade 10: Academics and Activities"
decurl = "http://twig.me/v1/push/dectest/" + zviceID
response = urllib2.urlopen(decurl)
html = response.read()
decTag = json.loads(html)['decTagID']
nameCol=14
mobColumn=15

def create_events(body, headers, zviceID, calendarID):
    return LL.invoke_rest('POST', LL.BASE_URL + zviceID + '/calendars/' + calendarID + '/events', json.dumps(body),
                          headers)
errorFile = "saptpadi_UCG.txt"
#
#
# URL: [http://www.twig-me.com/v1/zvice/interaction/596MAZH8ZKUGM]
#
# Payload: [{"interactionID":"CommonInteraction_INTERACTION_TYPE_LINK_USERPROFILE","linkemail":"sachin@zestl.com"}]
#
# Response:{"error":false,"message":"User Linked Successfully","error_code":-1,"data":{"elements":null},"title":"Pagdandi - Reading Cafe","homeurl":"http:\/\/www.twig-me.com\/v1\/zvice\/detailscard\/3KMGPB7EPJBWP","homemethod":"POST","homejsondata":null,"showmessage":true}
# "{"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_CALENDAR_EVENTS","CalendarID":107,"ZviceID":3000004598,"DefaultView":"Month","categoryType":"CalendarCard"}"
def create_user(p_id):
    with open(inputfile, "r") as rf:
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
                        url =LL.BASE_URL + 'zvice/interaction/' + ZbotID
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
                        url = LL.BASE_URL + 'zvice/interaction/' + zviceID
                        jsonreply = CM.hit_url_method(body, headers1, method, url)
                        ef.write(zviceID + "  ::  " + title + " :: " + jsonreply + "\n")
                        print jsonreply


                        # #post notes
                        method = "PUT"
                        url = LL.BASE_URL + 'ztag/notes_PP/' + zviceID
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

            return zviceID
            # except:
            #     print("problem in creating new user")




def make_events(user_id):
    # def generate_events(inputfile)
    # log in of course

    # read from a file

    jsondata = CM.getBaseStructure(ZbotID, headers1, LL.BASE_URL)

    # print  jsondata

    for card in jsondata['data']['elements']:
        if cardname == card['title']:
            calendarID = card['cardID']
            print calendarID
            calendarID = str(calendarID)
            # calendarID = str(173)
            # calendarID = str(112)
            # if card['cardtype'] == "buttoncard":
            #     method = "GET"
            #     url = card['actions'][0]['actionUrl']
            #     body = {}
            #     jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
            #     card = jsondata['data']['elements'][0]
            #     print card
            # print cardname
            # url = card['cturl']
            # body = json.loads(card['ctjsondata'])
            # method = card['ctmethod']
            # jdata = CM.hit_url_method(body, headers1, method, url)
            # print "******************"
            # jdata = json.loads(jdata)
            # for j in jdata['data']['elements']:
            #     if calendar in j['title']:
            #         calendarID = json.loads(j['content'])['CalendarID']
            #         print calendarID
            #         calendarID = str(calendarID)

    parseResults = CM.parse_files(inputfile)
    counter = 0
    if parseResults == "errors":
        print "File has encoding errors"
    else:

        with open(inputfile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            method = "POST"
            for row in data:
                pid = CM.force_decode(row[0])
                counter = counter + 1
                eventTitle = CM.force_decode(row[1])
                desc = CM.force_decode(row[2])
                start = CM.force_decode(row[3]) + " " + CM.force_decode(row[4])
                end = CM.force_decode(row[5]) + " " + CM.force_decode(row[6])
                remind = 0
                repeat = None
                self = 'Yes'
                allDay = 'No'
                colour = '#F44336'
                loc = CM.force_decode(row[8])
                remind_2 = 0
                comm_pref_reminder = 'FALSE'
                publish_draft = 'Save & Publish'
                occur = ''
                tag = CM.force_decode(row[10]) + " " + CM.force_decode(row[11])
                RequestBody = {"Title": eventTitle,
                               "StartDateTime": start,
                               "EndDateTime": end,
                               "Color": colour,
                               "Description": desc,
                               "PublishAction": publish_draft,
                               "Tags": tag,
                               "AllDay": allDay,
                               "RepeatEvent": repeat,
                               "Occurrences": occur,
                               "Location": loc,
                               "Timezone": "Asia/Kolkata",
                               "RemindCommPref": comm_pref_reminder,
                               "SelfRSVP": self,
                               "MaxAttendees": 1,
                               "NotifyRSVPStatusToAdmin": "true",
                               "NotifyRSVPStatusToOperator": "true",
                               "OwnerID": "",
                               "EventID": "",
                               "categorytype": "CalendarEvent",
                               "PreReminder2": {"CustomMessage": "", "ReminderType": "PRE", "ReminderOffset": ""},
                               "PreReminder1": {"CustomMessage": "", "ReminderType": "POST", "ReminderOffset": "",
                                                "ActionCardID": ""},
                               "PostReminder1": {"CustomMessage": "", "ReminderType": "PRE", "ReminderOffset": remind,
                                                 "ActionCardID": ""},
                               "ReminderDetails": {"PreReminder1": "", "PreReminder2": "", "PostReminder1": ""},
                               "ModerateRSVP": "true",
                               "IgnoreGuestCount": "true",
                               "MaxGuestCount": "",
                               "ShowOnBehalfOf": "false",
                               "ZviceID": decTag,
                               "CalendarID": calendarID,
                               }

                # RequestBody = {     "AllDay": allDay,
                #                     "OwnerID": "",
                #                     "EventID": "",
                #                     "categorytype": "CalendarEvent",
                #                     "Title": eventTitle,
                #                     "Occurrences": occur,
                #                     "Description": desc,
                #                     "ZviceID": decTag,
                #                     "RemindBefore": remind,
                #                     "RepeatEvent": repeat,
                #                     "SelfRSVP": self,
                #                     "Location": loc,
                #                     "Color": colour,
                #                     "StartDateTime": start,
                #                     "MaxAttendees": "",
                #                     "CalendarID": calendarID,
                #                     "EndDateTime": end,
                #                     "RemindBeforeTwo": remind_2,
                #                     "RemindCommPref": comm_pref_reminder,
                #                     "PublishAction": publish_draft,
                #                     "Timezone" : "Asia/Kolkata"
                #                 }
                print RequestBody
                response = create_events(RequestBody, headers1, zviceID, calendarID)
                print response

                result = json.loads(response['reply'])
                EventID = result['cardid']

                #  url = "http://twig-me.com/v13/"  # prod
                #                url="http://35.154.64.119/v13/"
                user_id = CM.findtagid(pid, zviceID, LL.BASE_URL, headers1)  # finding userid using pid

                print 'We get user id :', user_id

                rr = CM.patientinfo(calendarID, zviceID, user_id, headers1, EventID, LL.BASE_URL)

                print EventID
                print counter
                print "==========================="

                print rr

