import urllib
import json
import login1 as LL
import common_aditya as CM
import csv
import urllib2
nameCol = 14
mobColumn = 15

notename = [None] * 20
noteCol = [None] * 20
noOfNotes = 4

notename[0] = "pid"
noteCol[0] = 0
notename[1] = "Alternate PID"
noteCol[1] = 12
notename[2] = "Date"
noteCol[2] = 17
notename[3] = "Address"
noteCol[3] = 16


headers, headers1 = LL.req_headers()

hasHeader = 'Y'
businessID = LL.zbotID
#zviceID = "WH4ULS9BHSAKZ"
decurl = "http://twig.me/v1/push/dectest/" + businessID
response = urllib2.urlopen(decurl)
html = response.read()
decTag = json.loads(html)['decTagID']


decTag = json.loads(html)['decTagID']

def getBaseStructure(zbotID, headers1):
    url = LL.BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    response = hit_url(RequestBody, headers1, zbotID, url)
#    with open('C:/Users/Minal Thorat/Dropbox/Zestl-scripts/rundir/tmp', 'w') as f:
#        f.write(str(response))
    return json.loads(response)

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']

def create_events(body, headers, business_ID, calendarID):
    result= LL.invoke_rest('POST', LL.BASE_URL + business_ID + '/calendars/' + calendarID + '/events', json.dumps(body),
                          headers)
    return result
    print result

# def create_default_event(inputfile,dept_tagid,calendarID):
#     parseResults = CM.parse_files(inputfile)
#     counter = 0
#     if parseResults == "errors":
#         print "File has encoding errors"
#     else:
#
#         with open(inputfile, 'r') as rf:
#             data = csv.reader(rf, delimiter=',')
#             if hasHeader == "Y":
#                 row1 = data.next()
#             method = "POST"
#             for row in data:
#                 pid = CM.force_decode(row[0])
#                 counter = counter + 1
#                 eventTitle = CM.force_decode(row[1])
#                 desc = CM.force_decode(row[2])
#                 start = CM.force_decode(row[3]) + " " + CM.force_decode(row[4])
#                 end = CM.force_decode(row[5]) + " " + CM.force_decode(row[6])
#                 remind = 0
#                 repeat = None
#                 self = 'Yes'
#                 allDay = 'No'
#                 colour = '#F44336'
#                 loc = CM.force_decode(row[8])
#                 remind_2 = 0
#                 comm_pref_reminder = 'FALSE'
#                 publish_draft = 'Save & Publish'
#                 occur = ''
#                 tag = CM.force_decode(row[10]) + " " + CM.force_decode(row[11])
#                 RequestBody = {"Title": eventTitle,
#                                "StartDateTime": start,
#                                "EndDateTime": end,
#                                "Color": colour,
#                                "Description": desc,
#                                "PublishAction": publish_draft,
#                                "Tags": tag,  # doc name
#                                "AllDay": allDay,
#                                "RepeatEvent": repeat,
#                                "Occurrences": occur,
#                                "Location": loc,
#                                "Timezone": "Asia/Kolkata",
#                                "RemindCommPref": comm_pref_reminder,
#                                "SelfRSVP": self,
#                                "MaxAttendees": 1,
#                                "NotifyRSVPStatusToAdmin": "true",
#                                "NotifyRSVPStatusToOperator": "true",
#                                "OwnerID": "",
#                                "EventID": "",
#                                "categorytype": "CalendarEvent",
#                                "PreReminder2": {"CustomMessage": "", "ReminderType": "PRE", "ReminderOffset": ""},
#                                "PreReminder1": {"CustomMessage": "", "ReminderType": "POST", "ReminderOffset": "",
#                                                 "ActionCardID": ""},
#                                "PostReminder1": {"CustomMessage": "", "ReminderType": "PRE", "ReminderOffset": remind,
#                                                  "ActionCardID": ""},
#                                "ReminderDetails": {"PreReminder1": "", "PreReminder2": "", "PostReminder1": ""},
#                                "ModerateRSVP": "true",
#                                "IgnoreGuestCount": "true",
#                                "MaxGuestCount": "",
#                                "ShowOnBehalfOf": "false",
#                                "ZviceID": decTag,
#                                "CalendarID": calendarID,
#                                }
#
#             dept_tagid=dept_tagid
#             calendarID=calendarID
#             response = create_events(RequestBody, headers1, dept_tagid, calendarID)
#
#             #  print response
#             result = json.loads(response['reply'])
#             EventID = result['cardid']
#             u_name = row[nameCol].strip()
#             u_email = ''
#             mobile = row[mobColumn].strip()
#             print('Now finding user ids of patient\n')
#             user_id = CM.findtagid(pid, businessID, LL.BASE_URL, headers1)  # finding userid using pid
#             print(user_id)
#
#             if len(user_id) != 0:  # already user is created
#                 #         user_tagid= user_id[0]
#                 zviceID = user_id[0]
#                 print('Got userid:', zviceID)
#                 CM.add_contactdetails(zviceID, LL.BASE_URL, headers1, mobile)
#
#                 print('Adding moredetails\n')
#
#                 for i in range(0, noOfNotes):
#                     if noteCol[i] == -1:
#                         note = ""
#                     else:
#                         note = row[noteCol[i]].strip()
#                     CM.add_moredetails(zviceID, LL.BASE_URL, notename[i], note, headers1)
#
#             else:  # user will create here now!
#                 print ('USERID are not present so Creating new user \n')
#                 json_user_tagid = CM.add_user_InBusiness(businessID, u_name, u_email, headers1, LL.BASE_URL)
#
#                 json_user_tagid = json.loads(json_user_tagid)
#                 zviceID = json_user_tagid['data']['usertagid']  # usertagid
#
#                 CM.add_contactdetails(zviceID, LL.BASE_URL, headers1, mobile)
#
#                 print('Adding moredetails\n')
#
#                 for i in range(0, noOfNotes):
#                     if noteCol[i] == -1:
#                         note = ""
#                     else:
#                         note = row[noteCol[i]].strip()
#                     CM.add_moredetails(zviceID, LL.BASE_URL, notename[i], note, headers1)
#
#                 print('MoreDetails get added !\n')
#
#                 print('\nReturn from add user bussiness', json_user_tagid)
#
#             print('USER ID:', zviceID)
#     #                print 'We get user id :',user_id
#
#             rr = CM.patientinfo(calendarID, businessID, zviceID, headers1, EventID, LL.BASE_URL)
#
#             print 'Event gets generated !!\n'
#             print 'Event ID:', EventID
#             print 'Counter', counter
#             print "==========================="
#             print rr
#

def check_appointment(inputfile,centre_list,loc):

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
            url1 = card['cturl']
            method1 = card['ctmethod']
            body1 = json.loads(card['ctjsondata'])  # {"parentCardID":16410}

            jsonresponse1 = hit_url_method(body1, headers1, method1, url1)
            print jsonresponse1

            for card in json.loads(jsonresponse1)['data']['elements']:
                if 'Calendar' == card['title']:
                    calendarID = card['cardID']

                    filepath = LL.output_path
                    with open(filepath, "r") as rf:
                        data = csv.reader(rf, delimiter=',')
                        #  row1 = data.next()
                        for row in data:
                            doc = CM.force_decode(row[10]) + " " + CM.force_decode(row[11])
                            u_start_time = CM.force_decode(row[3]) + " " + CM.force_decode(row[4])  # user start time
                            u_end_time = CM.force_decode(row[5]) + " " + CM.force_decode(row[6])  # user end time
                            p_start_date = CM.force_decode(row[3])
                            p_end_date = CM.force_decode(row[5])
                            u_s_time = CM.force_decode(row[4])
                            u_e_time = CM.force_decode(row[6])
                            date=p_start_date.split('-')
                            year=date[0]
                            month=date[1]

                            for a in card['actions']:
                                if "Explore" == a['title']:
                                        print("inside")
                                        actionurl=[]
                                        actionurl = a['actionUrl']
                                        result = actionurl.replace('first_click=1', '')
                                       # actionurl = result + 'filter={"year":' + year + ',"month":' + month + ',"interval":30}'
                                        f = {"year": year,"month":month,'interval':30}
                                        grp = urllib.quote(json.dumps(f)) # we use this quote function for encoding send to filter
                                        actionurl = result + 'filter='+grp
#                                        actionurl = result + 'filter=%7B%22year%22%3A2018%2C%22month%22%3A7%2C%22interval%22%3A30%7D'
                                        method=a['method']
                                        body={}
                                        jsonresponse = hit_url_method(body, headers1, method, actionurl)
            #                    print(jsonresponse)
                                #filepath = "/home/adi/Downloads/TwigMeScripts-master/hlt7-json/siu/output/userinfo1.csv"

                                # p_start_date = CM.force_decode(row[3])
                                        list_start = []
                                        list_end = []
                                # u_s_time = CM.force_decode(row[4])
                                # u_e_time = CM.force_decode(row[6])
                                # doc = CM.force_decode(row[10]) + " " + CM.force_decode(row[11])

                                        print(doc)
                                        print 'Start time :',u_s_time
                                        print 'End Date :',u_e_time
                                        if json.loads(jsonresponse)['data']['elements']:
                                            for info in json.loads(jsonresponse)['data']['elements']:
                                                data = info['content']
                                                start_time=json.loads(data)['StartDateTime']
                                                end_time=json.loads(data)['EndDateTime']
                                                s_date,s_time=start_time.split(' ')#splits start date and time from server data
                                                e_date,e_time=end_time.split(' ')#splits end date and time from server data



                                                if ( s_date==p_start_date) and (doc == json.loads(data)['tags']):# if date and doc sould be same
                                                    print(doc)
                                                    list_start.append(s_time)
                                                    list_end.append(e_time)
                                                    print ('List start time', list_start)
                                                    print('List end time', list_end)
                                                    print ('start time:', s_time)
                                                    print ('End time :', e_time)
                                                    print ('user start time:', u_s_time)
                                                    print ('user End time :', u_e_time)

                                                else:
                                                    flag= True
                                        else:
                                           # create_default_event(inputfile,dept_tagid,calendarID)
                                            return  True

                                        for i, j in zip(list_start, list_end): # assigning appointments
                                            if u_e_time <= i:
                                                flag = True
                                            elif j <= u_s_time:
                                                flag = True
                                            else:
                                                return False

                                        return flag

