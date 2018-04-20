#********************* EXCEL EXAMPLE *********************************#

# import csv
#
# outfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/try_excel.csv"
#
# # writer=csv.writer(open(outfile,'a'))
# # header=['type','id','numberOfUpdates','isPingEnabled','lastUpdated']
# # length_list=len(header)
# # i=0
# #
# # while i!=length_list :
# #     data=header[i]
# #     print data
# #     i=i+1
# #     writer.writerow([data])
#
#
#
# with open(outfile,'a') as f:
# # writer=csv.writer(open(outfile,'a'))
#     header=['type','id','numberOfUpdates','isPingEnabled','lastUpdated']
#     for item in header:
#         f.write(item + ',')


#********************  GRID CALENDAR  *************************************#

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
    return LL.invoke_rest('POST', LL.BASE_URL + zviceID + '/calendars/' + calendarID + '/events', json.dumps(body),
                          headers)
if __name__ == '__main__':
    # log in of course
    headers, headers1 = LL.req_headers()

    inputfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/Grade11-FinalExam.csv"

    hasHeader = 'Y'
    # read from a file

    zviceID = 'CW7ZBJ8C3H9DL'
    cardname = "Grade 11"
    calendar = "Grade 11: Calendar - Academic and Activity"
    decurl = "http://twig.me/v1/push/dectest/" + zviceID
    response = urllib2.urlopen(decurl)
    html = response.read()
    decTag = json.loads(html)['decTagID']

    jsondata = CM.getBaseStructure(zviceID, headers1, LL.BASE_URL)
    print  jsondata
    for card in jsondata['data']['elements']:
        if cardname in card['title']:
            if card['cardtype'] == "buttoncard":
                method = "GET"
                url = card['actions'][0]['actionUrl']
                body = {}
                jsondata = CM.hit_url_method(body, headers1, method, url)
                print jsondata
                # card = jsondata['data']['elements'][0]
                for j in json.loads(jsondata)['data']['elements']:
                    if calendar == j['title']:
                        print "present"
                        if j['cardtype'] == "buttoncard":
                            print "present"
                            method = "GET"
                            url = j['actions'][0]['actionUrl']
                            body = {}
                            jsondata = CM.hit_url_method(body, headers1, method, url)
                            print jsondata

                            for id in json.loads(jsondata)['data']['elements']:
                                if calendar == id['title']:
                                    print "present"
                                    calendarID = id['cardID']
                                    calendarID = str(calendarID)
                                    print calendarID

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
                               "Location": loc,
                               "Color": colour,
                               "StartDateTime": start,
                               "MaxAttendees": "",
                               "CalendarID": calendarID,
                               "EndDateTime": end
                               }
                print RequestBody
                response = create_events(RequestBody, headers1, zviceID, calendarID)
                print response
                print "==========================="
                print counter