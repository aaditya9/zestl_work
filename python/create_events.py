#!/usr/local/bin/python

# usage create_groups.py <file_containing_grpnames_to_create>
# ensure the file dev_millennium.py in the lib directory is configured correctly

import json
import sys
import csv

import hashlib\

import lib.login1 as LL

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
  
        inputfile = "/Users/user/Dropbox/Zestl-scripts/millennium/script_inputs/IBDP_13dec_cal.csv"
        hasHeader = 'Y'
  #read from a file
        # 
        with open(inputfile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            method = "POST"
            for row in data:
                eventTitle = row[0]
                desc = row[1]
                # desc = "some description here"
                start = row[2] + " " + row[3]
                end = row[4] + " " + row[5]
                remind = row[8]
                repeat = row[9]
                self = row[12]
                allDay = row[13]
                colour = row[15]

        #     for line in f:
        #         details = line.split('\t')
        #         zviceID = details[0].strip()
        #         emailID = details[1].strip()
        #         body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_LINK_USERPROFILE","linkemail": emailID}
        #         response = change_linked_user(body, headers1, zviceID)
        #         print zviceID
        #         print emailID
        #         print response
        #
        # "{"
        # interactionID
        # ":"
        # CommonInteraction_INTERACTION_TYPE_SHOW_CALENDAR_EVENTS
        # ","
        # CalendarID
        # ":173,"
        # ZviceID
        # ":3000004597,"
        # DefaultView
        # ":"
        # Month
        # ","
        # categoryType
        # ":"
        # CalendarCard
        # "}"

        #link single users
                zviceID = 'CW7ZBJ8C3H9DL'
                calendarID = '125'
                # eventTitle = "Trial_sujoy_script"

                RequestBody = {     "AllDay": allDay,
                                    "OwnerID": "",
                                    "EventID": "",
                                    "categorytype": "CalendarEvent",
                                    "Title": eventTitle,
                                    "Occurrences": "1",
                                    "Description": desc,
                                    "ZviceID": "3000004598",
                                    "RemindBefore": remind,
                                    "RepeatEvent": repeat,
                                    "SelfRSVP": self,
                                    "Location": "",
                                    "Color": colour,
                                    "StartDateTime": start,
                                    "MaxAttendees": "",
                                    "CalendarID": calendarID,
                                    "EndDateTime": end
                                }


                print RequestBody

                response = create_events(RequestBody, headers1, zviceID, calendarID)
                print response

        
        
        
        # 
        # # open the file specified on command line    
        # with open(sys.argv[1], 'r') as my_file:
        #     groupnames = my_file.read().split()
        #     print groupnames
        # # go ahead and create those groups    
        # for grpname in groupnames: 
        #     body =  {'groupName': grpname}
        #     print set_groups(body, headers1, LL.zbotID)
        #     # print result_setgrps
        # 
 
