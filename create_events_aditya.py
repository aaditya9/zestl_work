# !/usr/local/bin/python

# usage create_groups.py <file_containing_grpnames_to_create>
# ensure the file dev_millennium.py in the lib directory is configured correctly

import json
import sys
import csv
import requests
import urllib2
import urllib

import hashlib
import login1 as LL
import common_aditya as CM
import copy_getbasejson as CG
nameCol1=13
nameCol2 = 14
mobColumn = 15
businessID = LL.zbotID
notename = [None] * 20
noteCol = [None] * 20
noOfNotes = 4

form_ID=7082

notename[0] = "pid"
noteCol[0] = 0
notename[1] = "Alternate PID"
noteCol[1] = 12
notename[2] = "Date"
noteCol[2] = 17
notename[3] = "Address"
noteCol[3] = 16

headers, headers1 = LL.req_headers()

#inputfile = "/home/adi/Downloads/TwigMeScripts-master/hlt7-json/siu/output/userinfo1.csv"

hasHeader = 'Y'
# read from a file
# ZbotID = "WH4ULS9BHSAKZ"
#businessID = "WH4ULS9BHSAKZ"
businessID = LL.zbotID

# zviceID = 'WH4ULS9BHSAKZ'
# EYP / EYP\:\ Academic\ and \ Activity\ Calendar /
cardname = "Text card 5"
# calendar = "Grade 10: Academic and Activity Calendar"
# calendar = "Calendar Grade 10: Academics and Activities"
decurl = "http://twig.me/v1/push/dectest/" + businessID
response = urllib2.urlopen(decurl)
html = response.read()
decTag = json.loads(html)['decTagID']

errorFile = "saptpadi_UCG.txt"


def create_events(body, headers, businessID, calendarID):
    return LL.invoke_rest('POST', LL.BASE_URL + businessID + '/calendars/' + calendarID + '/events', json.dumps(body),
                          headers)

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def delete_events(BASE_URL,dept_tagid,jsonresponse1,start,end,doc):
    for card in json.loads(jsonresponse1)['data']['elements']:
        if 'Calendar' == card['title']:
            calendarID = card['cardID']

            for a in card['actions']:
                if "Explore" == a['title']:
                    print("inside")
                    year, month, day = start.split('-')
                    actionurl = []
                    actionurl = a['actionUrl']
                    result = actionurl.replace('first_click=1', '')
                    f = {"year": year, "month": month, 'interval': 30}
                    grp = urllib.quote(json.dumps(f))  # we use this quote function for encoding send to filter
                    actionurl = result + 'filter=' + grp
                    method = a['method']
                    body = {}
                    jsonresponse = hit_url_method(body, headers1, method, actionurl)

                    if json.loads(jsonresponse)['data']['elements']:
                        for info in json.loads(jsonresponse)['data']['elements']:
                            data = info['content']
                            title = info['title']
                            start_time = json.loads(data)['StartDateTime']
                            end_time = json.loads(data)['EndDateTime']
                            s_date, s_time = start_time.split(' ')  # splits start date and time from server data
                            e_date, e_time = end_time.split(' ')  # splits end date and time from server data
                            dd = json.loads(data)['tags']
                            eventID = json.loads(data)['EventID']
                            start1,time1=start.split(' ')
                            end1,time2=end.split(' ')

                            if (start1 == s_date) and (doc == json.loads(data)['tags']) and(end1 == e_date) :  # and ((doc_s_time == s_time)or (doc_e_time == e_time)):
                                    result = CM.delete_event(BASE_URL, dept_tagid, calendarID, eventID, headers1)

                            else:
                                print('No event')
    return result


def generate_events(inputfile,centre_list):
    print('Control in Event function now')

    with open(inputfile, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        #if hasHeader == "Y":
            #row1 = data.next()
        for row in data:
                loc = CM.force_decode(row[8])

    for k, v in centre_list.items():
        if loc in k:
            dept_tagid = v
    print dept_tagid


    url = LL.BASE_URL + 'genericcards/' + dept_tagid
    body = {}
    method = "POST"
    # flag=True

    jsonresponse = hit_url_method(body, headers1, method, url)

    for card in json.loads(jsonresponse)['data']['elements']:
        if "Admin Appointment" == card['title']:
           url1=card['cturl']
           method1=card['ctmethod']
           body1=json.loads(card['ctjsondata'])#{"parentCardID":16410}

           jsonresponse1 = hit_url_method(body1, headers1, method1, url1)
           print jsonresponse1

           for card in json.loads(jsonresponse1)['data']['elements']:
                if 'Calendar' == card['title']:
                    calendarID = card['cardID']
                    print calendarID
                    calendarID = str(calendarID)

    parseResults = CM.parse_files(inputfile)
    counter = 0
    if parseResults == "errors":
        print "File has encoding errors"
    else:

        with open(inputfile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
        #    if hasHeader == "Y":
                # row1 = data.next()
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
                status=CM.force_decode(row[18])
                RequestBody = {"Title": eventTitle,
                               "StartDateTime": start,
                               "EndDateTime": end,
                               "Color": colour,
                               "Description": desc,
                               "PublishAction": publish_draft,
                               "Tags": tag,  # doc name
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

             #  is status is cancel then delete event
                #list_status=['Cancelled']
                booked_list=['BOOKED','booked','Booked']
                CANCEL_status = ['Cancelled', 'CANCELLED', 'cancelled']
                noshow_list=['NO_SHOW','no_show','No_show','No_Show','COMPLETED','Completed','completed']
                if status in CANCEL_status:

                    result = delete_events(LL.BASE_URL, dept_tagid, jsonresponse1, start, end, tag)

                if status in noshow_list:
                    print('Status is Noshow, so delting prev and create new !!!')
                    result = delete_events(LL.BASE_URL, dept_tagid, jsonresponse1, start, end, tag)
                    flag = CG.check_appointment(inputfile, centre_list, loc)

                    if flag == False:
                        print('Time slot is not availabe for this doctor !!')
                    else:
                        print('Creating new events !!')
                        response = create_events(RequestBody, headers1, dept_tagid, calendarID)
                        result = json.loads(response['reply'])
                        EventID = result['cardid']
                        u_name = row[nameCol1].strip() + ' ' + row[nameCol2].strip()
                        u_name = u_name + " " + '(' + pid + ')'
                        u_email = ''
                        mobile = row[mobColumn].strip()
                        user_id = CM.findtagid(pid, businessID, LL.BASE_URL, headers1)  # finding userid using pid
                        if len(user_id) != 0:  # already user is created
                            zviceID = user_id[0]
                            print('Got userid:', zviceID)
                            CM.add_contactdetails(zviceID, LL.BASE_URL, headers1, mobile)

                            for i in range(0, noOfNotes):
                                if noteCol[i] == -1:
                                    note = ""
                                else:
                                    note = row[noteCol[i]].strip()
                                CM.add_moredetails(zviceID, LL.BASE_URL, notename[i], note, headers1)

                            u_name = row[nameCol1].strip() + ' ' + row[nameCol2].strip()
                            aid = row[noteCol[1]].strip()
                            address = row[noteCol[3]].strip()

                            inputdata = {"Patient Name": u_name,
                                         "PID": pid,
                                         "Contact No. ": mobile,
                                         "Address": address,
                                         "Alternate ID": aid,
                                         "User ID": user_id[0]
                                         }
                            rr = CM.patientinfo(calendarID, dept_tagid, zviceID, headers1, EventID, LL.BASE_URL)

                            result = CM.form_submission_using_NEW_API(LL.BASE_URL, businessID, headers1, form_ID,
                                                                      inputdata)

                        else:  # user will create here now!
                            print ('USERID are not present so Creating new user \n')
                            json_user_tagid = CM.add_user_InBusiness(dept_tagid, u_name, u_email, headers1, LL.BASE_URL)

                            json_user_tagid = json.loads(json_user_tagid)
                            zviceID = json_user_tagid['data']['usertagid']  # usertagid

                            CM.add_contactdetails(zviceID, LL.BASE_URL, headers1, mobile)

                            print('Adding moredetails\n')

                            for i in range(0, noOfNotes):
                                if noteCol[i] == -1:
                                    note = ""
                                else:
                                    note = row[noteCol[i]].strip()
                                CM.add_moredetails(zviceID, LL.BASE_URL, notename[i], note, headers1)

                            rr = CM.patientinfo(calendarID, dept_tagid, zviceID, headers1, EventID, LL.BASE_URL)
                            aid = row[noteCol[1]].strip()

                            address = row[noteCol[3]].strip()
                            inputdata = {"Patient name": u_name,
                                         "PID": pid,
                                         "Contact No. ": mobile,
                                         "Address": address,
                                         "Alternate ID": aid,
                                         "User ID": zviceID
                                         }

                            result = CM.form_submission_using_NEW_API(LL.BASE_URL, businessID, headers1, form_ID,
                                                                      inputdata)
                if status in booked_list:
                                                             # checking if apoointment slot is busy or not
                        flag = CG.check_appointment(inputfile,centre_list,loc)

                        if flag == False:
                            print('Time slot is not availabe for this doctor !!')
                        else:
                            print('Creating new events !!')
                            response = create_events(RequestBody, headers1, dept_tagid, calendarID)
                            result = json.loads(response['reply'])
                            EventID = result['cardid']
                            u_name = row[nameCol1].strip()+' '+ row[nameCol2].strip()
                            u_name=u_name + " " + '('+ pid+')'
                            u_email = ''
                            mobile = row[mobColumn].strip()
                            user_id = CM.findtagid(pid, businessID, LL.BASE_URL, headers1)  # finding userid using pid
                            if len(user_id) != 0:  # already user is created
                                zviceID = user_id[0]
                                print('Got userid:', zviceID)
                                CM.add_contactdetails(zviceID, LL.BASE_URL, headers1, mobile)

                                for i in range(0, noOfNotes):
                                    if noteCol[i] == -1:
                                        note = ""
                                    else:
                                        note = row[noteCol[i]].strip()
                                    CM.add_moredetails(zviceID, LL.BASE_URL, notename[i], note, headers1)

                                u_name = row[nameCol1].strip() + ' ' + row[nameCol2].strip()
                                aid = row[noteCol[1]].strip()
                                address = row[noteCol[3]].strip()

                                inputdata = {"Patient Name": u_name,
                                             "PID": pid,
                                             "Contact No. ": mobile,
                                             "Address": address,
                                             "Alternate ID": aid,
                                             "User ID": user_id[0]
                                             }
                                rr = CM.patientinfo(calendarID, dept_tagid, zviceID, headers1, EventID, LL.BASE_URL)

                                result = CM.form_submission_using_NEW_API(LL.BASE_URL, businessID, headers1, form_ID, inputdata)

                            else:  # user will create here now!
                                print ('USERID are not present so Creating new user \n')
                                json_user_tagid = CM.add_user_InBusiness(dept_tagid, u_name, u_email, headers1, LL.BASE_URL)

                                json_user_tagid = json.loads(json_user_tagid)
                                zviceID = json_user_tagid['data']['usertagid']  # usertagid

                                CM.add_contactdetails(zviceID, LL.BASE_URL, headers1, mobile)

                                print('Adding moredetails\n')

                                for i in range(0, noOfNotes):
                                    if noteCol[i] == -1:
                                        note = ""
                                    else:
                                        note = row[noteCol[i]].strip()
                                    CM.add_moredetails(zviceID, LL.BASE_URL, notename[i], note, headers1)

                                rr = CM.patientinfo(calendarID, dept_tagid, zviceID, headers1, EventID, LL.BASE_URL)
                                aid = row[noteCol[1]].strip()

                                address=row[noteCol[3]].strip()
                                inputdata={"Patient name":u_name,
                                      "PID":pid,
                                      "Contact No. ":mobile,
                                        "Address":address,
                                        "Alternate ID":aid,
                                           "User ID":zviceID
                                      }

                                result=CM.form_submission_using_NEW_API(LL.BASE_URL,businessID,headers1,form_ID,inputdata)
