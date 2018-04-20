#!/usr/local/bin/python

# usage create_groups.py <file_containing_grpnames_to_create>
# ensure the file dev_millennium.py in the lib directory is configured correctly

import json
import sys
import csv
import requests
import urllib2


import hashlib\

import lib.login1 as LL
import common as CM

def set_groups(body, headers, zviceID):
    return LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/add/' + zviceID, json.dumps(body), headers)

def change_linked_user(body, headers, zviceID):
    return LL.invoke_rest('POST', LL.BASE_URL + 'zvice/interaction/' + zviceID, json.dumps(body), headers)

def create_events(body, headers, zviceID, calendarID):
    return LL.invoke_rest('POST', LL.BASE_URL + zviceID + '/calendars/' + calendarID + '/events' , json.dumps(body), headers)
# 
# 
# URL: [http://www.twig-me.com/v1/zvice/interaction/596MAZH8ZKUGM]
# 
# Payload: [{"interactionID":"CommonInteraction_INTERACTION_TYPE_LINK_USERPROFILE","linkemail":"sachin@zestl.com"}]
# 
# Response:{"error":false,"message":"User Linked Successfully","error_code":-1,"data":{"elements":null},"title":"Pagdandi - Reading Cafe","homeurl":"http:\/\/www.twig-me.com\/v1\/zvice\/detailscard\/3KMGPB7EPJBWP","homemethod":"POST","homejsondata":null,"showmessage":true}
# "{"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_CALENDAR_EVENTS","CalendarID":107,"ZviceID":3000004598,"DefaultView":"Month","categoryType":"CalendarCard"}"


if __name__ == '__main__':
        #log in of course
        headers, headers1 = LL.req_headers()
  
        inputfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"

        hasHeader = 'Y'
  #read from a file
        #


        zviceID = 'AZSG5JLYPJVB5'
        # EYP / EYP\:\ Academic\ and \ Activity\ Calendar /
        cardname = "Annual Calendar"
        # calendar = "Grade 10: Academic and Activity Calendar"
        # calendar = "Calendar Grade 10: Academics and Activities"
        decurl = "http://twig.me/v1/push/dectest/" + zviceID
        response = urllib2.urlopen(decurl)
        html = response.read()
        decTag = json.loads(html)['decTagID']

        jsondata = CM.getBaseStructure(zviceID, headers1, LL.BASE_URL)
        print  jsondata
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
                    counter = counter + 1
                    eventTitle = CM.force_decode(row[0])
                    desc = CM.force_decode(row[1])
                    start = CM.force_decode(row[2]) + " " + CM.force_decode(row[3])
                    end = CM.force_decode(row[4]) + " " + CM.force_decode(row[5])
                    remind = CM.force_decode(row[8])
                    repeat = CM.force_decode(row[9])
                    self = CM.force_decode(row[12])
                    allDay = CM.force_decode(row[13])
                    colour = CM.force_decode(row[15])
                    loc = CM.force_decode(row[7])
                    remind_2 = CM.force_decode(row[16])
                    comm_pref_reminder = str(CM.force_decode(row[17]))
                    publish_draft = CM.force_decode(row[18])
                    occur = CM.force_decode(row[10])

                    RequestBody = {"Title": eventTitle,
                                   "StartDateTime" : start,
                                   "EndDateTime": end,
                                   "Color": colour,
                                   "Description": desc,
                                   "PublishAction": publish_draft,
                                   "Tags" : "",
                                   "AllDay": allDay,
                                   "RepeatEvent": repeat,
                                   "Occurrences": occur,
                                   "Location": loc,
                                   "Timezone": "Asia/Kolkata",
                                   "RemindCommPref": comm_pref_reminder,
                                   "SelfRSVP": self,
                                   "MaxAttendees": "",
                                   "NotifyRSVPStatusToAdmin" : "false",
                                   "NotifyRSVPStatusToOperator" : "false",
                                   "OwnerID": "",
                                   "EventID": "",
                                   "categorytype": "CalendarEvent",
                                   "PreReminder2": {"CustomMessage": "", "ReminderType": "PRE", "ReminderOffset": ""},
                                   "PreReminder1": {"CustomMessage": "", "ReminderType": "POST", "ReminderOffset": "","ActionCardID": ""},
                                   "PostReminder1": {"CustomMessage": "", "ReminderType": "PRE","ReminderOffset": remind, "ActionCardID": ""},
                                   "ReminderDetails" : {"PreReminder1":"","PreReminder2":"","PostReminder1":""},
                                   "ModerateRSVP": "false",
                                   "IgnoreGuestCount": "false",
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
                    print counter
                    print "==========================="