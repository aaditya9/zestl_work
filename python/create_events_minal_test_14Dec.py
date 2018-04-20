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
  
        inputfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/radhika.csv"
        # inputfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"

        hasHeader = 'Y'
  #read from a file
        #
        zviceID = '8SFKZCV5PFAXV'
        # EYP / EYP\:\ Academic\ and \ Activity\ Calendar /
        cardname = "Text"
        # cardname = "Calendar"
        calendar = "Date"
        decurl = "https://twig.me/v1/push/dectest/" + zviceID
        response = urllib2.urlopen(decurl)
        html = response.read()
        decTag =  json.loads(html)['decTagID']

        jsondata = CM.getBaseStructure(zviceID, headers1, LL.BASE_URL)
        for card in jsondata['data']['elements']:
            if cardname in card['title']:
                if card['cardtype'] == "buttoncard":
                    method = "GET"
                    url = card['actions'][0]['actionUrl']
                    body = {}
                    jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
                    print jsondata

                    for subcard in jsondata['data']['elements']:
                        if calendar in subcard['title']:
                            if subcard['cardtype'] == "buttoncard":
                                method = "GET"
                                url = subcard['actions'][0]['actionUrl']
                                body = {}
                                jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
                                print jsondata
                                for action in jsondata['data']['elements']:
                                    if calendar == action['title']:
                                        print "present"
                                        for subaction in action['actions']:
                                            if "Explore" == subaction['title']:
                                                url = subaction['actionUrl']
                                                method = subaction['method']
                                                data = json.loads(subaction['data'])
                                                calendarID = data['CalendarID']
                                                # print id
                                                body = subaction['data']
                                                jsondata = CM.hit_url_method(body, headers1, method, url)
                                                print jsondata
                                                for cal in json.loads(jsondata)['data']['floating_menu']['floating_buttons']:
                                                    if "Add Event" == cal['title']:
                                                        print "found"
                                                        method = cal['method']
                                                        url = cal['actionUrl']
                                                        # parseResults = CM.parse_files(inputfile)

                                                        # if parseResults == "errors":
                                                        #     print "File has encoding errors"
                                                        # else:

                                                        with open(inputfile, 'r') as rf:
                                                            data = csv.reader(rf, delimiter=',')
                                                            if hasHeader == "Y":
                                                                row1 = data.next()
                                                            method = "POST"
                                                            for row in data:
                                                                eventTitle = CM.force_decode(row[0])
                                                                desc = CM.force_decode(row[1])
                                                                start = CM.force_decode(
                                                                    row[2]) + " " + CM.force_decode(row[3])
                                                                end = CM.force_decode(
                                                                    row[4]) + " " + CM.force_decode(row[5])
                                                                remind = CM.force_decode(row[8])
                                                                repeat = CM.force_decode(row[9])
                                                                self = CM.force_decode(row[12])
                                                                allDay = CM.force_decode(row[13])
                                                                colour = CM.force_decode(row[15])
                                                                attendees = CM.force_decode(row[11])

                                                                RequestBody = {"AllDay": allDay,
                                                                               "OwnerID": "",
                                                                               "EventID": "",
                                                                               "categorytype": "CalendarEvent",
                                                                               "Title": eventTitle,
                                                                               "Occurrences": "1",
                                                                               "Description": desc,
                                                                               "ZviceID": decTag,
                                                                               "RemindBefore": remind,
                                                                               "RepeatEvent": repeat,
                                                                               "SelfRSVP": self,
                                                                               "Location": "pune",
                                                                               "Color": colour,
                                                                               "StartDateTime": start,
                                                                               "MaxAttendees": attendees,
                                                                               "CalendarID": calendarID,
                                                                               "EndDateTime": end
                                                                               }

                                                                print RequestBody
                                                                print url
                                                                print method

                                                                # response = create_events(RequestBody, headers1, zviceID, calendarID)
                                                                response = create_events(RequestBody,headers1, method, url)
                                                                print response
                                                                print "==========================="
                                                                # CM.hit_url_method(body, headers1, method, url)



        # for card in jsondata['data']['elements']:
        #     if cardname in card['title']:
        #         print cardname
        #         calendarID = 112
        #         # calendarID = 66
        #         calendarID = str(calendarID)




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

        #
        # parseResults = CM.parse_files(inputfile)
        #
        # if parseResults == "errors":
        #     print "File has encoding errors"
        # else:
        #
        #     with open(inputfile, 'r') as rf:
        #         data = csv.reader(rf, delimiter=',')
        #         if hasHeader == "Y":
        #             row1 = data.next()
        #         method = "POST"
        #         for row in data:
        #             eventTitle = CM.force_decode(row[0])
        #             desc = CM.force_decode(row[1])
        #             start = CM.force_decode(row[2]) + " " + CM.force_decode(row[3])
        #             end = CM.force_decode(row[4]) + " " + CM.force_decode(row[5])
        #             remind = CM.force_decode(row[8])
        #             repeat = CM.force_decode(row[9])
        #             self = CM.force_decode(row[12])
        #             allDay = CM.force_decode(row[13])
        #             colour = CM.force_decode(row[15])
        #             attendees = CM.force_decode(row[11])
        #
        #             RequestBody = {     "AllDay": allDay,
        #                                 "OwnerID": "",
        #                                 "EventID": "",
        #                                 "categorytype": "CalendarEvent",
        #                                 "Title": eventTitle,
        #                                 "Occurrences": "4",
        #                                 "Description": desc,
        #                                 "ZviceID": decTag,
        #                                 "RemindBefore": remind,
        #                                 "RepeatEvent": repeat,
        #                                 "SelfRSVP": self,
        #                                 "Location": "pune",
        #                                 "Color": colour,
        #                                 "StartDateTime": start,
        #                                 "MaxAttendees": attendees,
        #                                 "CalendarID": calendarID,
        #                                 "EndDateTime": end
        #                             }
        #
        #
        #             print RequestBody
        #
        #             response = create_events(RequestBody, headers1, zviceID, calendarID)
        #             print response
        #             print "==========================="