import json
import csv
import logon as LL
import common as CM
import re
import requests
import auth as AA
import urllib2

SERVER = "https://twig.me/"
version = "v8/"
BASE_URL = SERVER + version


zviceID = "4R9NAJP6NKWAR"    ####  Business ID
email = "admin@zestl.com"
pwd = AA.pwd

inputfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"
hasHeader = 'Y'
counter = 0
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
decurl = "http://twig.me/v1/push/dectest/" + zviceID
response = urllib2.urlopen(decurl)
html = response.read()
decTag = json.loads(html)['decTagID']

# def create_events(body, headers, zviceID, calendarID):
#     return LL.invoke_rest('POST', LL.BASE_URL + zviceID + '/calendars/' + calendarID + '/events', json.dumps(body),
#                           headers)

# zviceID = 'EUNXYEQF7TGHR'
cardname = "School"
calendar = "Holiday"

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for card in jsondata['data']['elements']:
    if cardname in card['title']:
        if card['cardtype'] == "buttoncard":
            method = "GET"
            url = card['actions'][0]['actionUrl']
            body = {}
            jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
            print jsondata
            for a in jsondata['data']['elements']:
                # title = "16 May Calendar"
                if calendar == a['title']:
                    print "found"
                    calendarID = a['cardID']
                    calendarID = str(calendarID)
                    for b in a['actions']:
                        if "Explore" in b['title']:
                            body = b['data']
                            method = b['method']
                            url = b['actionUrl']

                            jasub = CM.hit_url_method(body, headers1, method, url)
                            print "-------------------------------------------------------------"

                            for ac in json.loads(jasub)['data']['elements']:
                                with open(inputfile, 'r') as rf:
                                    data = csv.reader(rf, delimiter=',')
                                    if hasHeader == "Y":
                                        row1 = data.next()
                                    for row in data:

                                        eventTitle = CM.force_decode(row[0])
                                        desc = CM.force_decode(row[1])
                                        start = CM.force_decode(row[2]) + " " + CM.force_decode(row[3])
                                        end = CM.force_decode(row[4]) + " " + CM.force_decode(row[5])
                                        remind1 = CM.force_decode(row[8])
                                        repeat = CM.force_decode(row[9])
                                        self = CM.force_decode(row[12])
                                        allDay = CM.force_decode(row[13])
                                        colour = CM.force_decode(row[15])
                                        loc = CM.force_decode(row[7])
                                        remind2 = CM.force_decode([row[16]])
                                        # title = "Exam"
                                        if eventTitle == ac['title']:
                                            print "Found 2"
                                            body = json.loads(ac['content'])
                                            url = ac['cturl']
                                            method = ac['ctmethod']
                                            jsondata = CM.hit_url_method(body, headers1, method, url)
                                            print jsondata

                                            for subac in json.loads(jsondata)['data']['elements']:
                                                # title = "Exam"
                                                if eventTitle == subac['title']:
                                                    print "Found 3"

                                                    for subac1 in subac['actions']:
                                                        # title = "More actions"
                                                        if "More actions" == subac1['title']:
                                                            print "3rd level"
                                                            body = {}
                                                            url = subac1['actionUrl']
                                                            method = subac1['method']
                                                            jsondata = CM.hit_url_method(body, headers1, method, url)
                                                            print jsondata

                                                            for subedit in json.loads(jsondata)['data']['ondemand_action']:
                                                                if "Edit" == subedit['title']:
                                                                    print "editing"
                                                                    calurl = subedit['actionUrl']
                                                                    counter = counter + 1
                                                                    RequestBody = {"AllDay": allDay,
                                                                                   "OwnerID": "",
                                                                                   "EventID": "",
                                                                                   "categorytype": "CalendarEvent",
                                                                                   "Title": eventTitle,
                                                                                   "Occurrences": "1",
                                                                                   "Description": desc,
                                                                                   "ZviceID": decTag,
                                                                                   "RemindBefore": remind1,
                                                                                   "RepeatEvent": repeat,
                                                                                   "SelfRSVP": self,
                                                                                   "Location": loc,
                                                                                   "Color": colour,
                                                                                   "StartDateTime": start,
                                                                                   "MaxAttendees": "",
                                                                                   "CalendarID": calendarID,
                                                                                   "EndDateTime": end,
                                                                                   "RemindBeforeTwo": remind2,
                                                                                   "RemindCommPref": "true",
                                                                                   "Slots": ""
                                                                                   }
                                                                    print RequestBody
                                                                    method = "PUT"
                                                                    url = calurl
                                                                    print url
                                                                    jsondata = CM.hit_url_method(RequestBody, headers1,method, url)
                                                                    print jsondata
                                                                    print counter

# parseResults = CM.parse_files(inputfile)
# # counter = 0
# if parseResults == "errors":
#     print "File has encoding errors"
# else:
#
#     with open(inputfile, 'r') as rf:
#         data = csv.reader(rf, delimiter=',')
#         if hasHeader == "Y":
#             row1 = data.next()
#         for row in data:
#             counter = counter + 1
#             eventTitle = CM.force_decode(row[0])
#             desc = CM.force_decode(row[1])
#             start = CM.force_decode(row[2]) + " " + CM.force_decode(row[3])
#             end = CM.force_decode(row[4]) + " " + CM.force_decode(row[5])
#             remind1 = CM.force_decode(row[8])
#             repeat = CM.force_decode(row[9])
#             self = CM.force_decode(row[12])
#             allDay = CM.force_decode(row[13])
#             colour = CM.force_decode(row[15])
#             loc = CM.force_decode(row[7])
#             remind2 = CM.force_decode([row[16]])
#
#             RequestBody = {"AllDay": allDay,
#                            "OwnerID": "",
#                            "EventID": "",
#                            "categorytype": "CalendarEvent",
#                            "Title": eventTitle,
#                            "Occurrences": "1",
#                            "Description": desc,
#                            "ZviceID": decTag,
#                            "RemindBefore": remind1,
#                            "RepeatEvent": repeat,
#                            "SelfRSVP": self,
#                            "Location": loc,
#                            "Color": colour,
#                            "StartDateTime": start,
#                            "MaxAttendees": "",
#                            "CalendarID": calendarID,
#                            "EndDateTime": end,
#                            "RemindBeforeTwo": remind2,
#                            "RemindCommPref": "true",
#                            "Slots": ""
#                            }
#             print RequestBody
#             method = "PUT"
#             url = calurl
#             print url
#             jsondata = CM.hit_url_method(RequestBody, headers1, method, url)
#             print jsondata