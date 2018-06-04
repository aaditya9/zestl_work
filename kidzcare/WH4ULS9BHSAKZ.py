
import update_appointment as UA
import final_hl7_to_json as FA
import common_aditya as CM
import login1 as LL
import urllib2
import json
businessID = LL.zbotID

# zviceID = 'WH4ULS9BHSAKZ'
# EYP / EYP\:\ Academic\ and \ Activity\ Calendar /
cardname = "Calendar new"
decurl = "http://twig.me/v1/push/dectest/" + businessID
response = urllib2.urlopen(decurl)
html = response.read()
decTag = json.loads(html)['decTagID']

errorFile = "saptpadi_UCG.txt"

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def create_events(body, headers, businessID, calendarID):
    return LL.invoke_rest('POST', LL.BASE_URL + businessID + '/calendars/' + calendarID + '/events', json.dumps(body),
                          headers)

def check_appointment(start,end,doctor, centre_list,centre,jsonresponse1):
    for card in json.loads(jsonresponse1)['data']['elements']:
        if 'Calendar' == card['title']:
            calendarID = card['cardID']

            for a in card['actions']:
                if "Explore" == a['title']:
                    print("inside")
                    actionurl = a['actionUrl']
                    method = a['method']
                    body = {}
                    jsonresponse = hit_url_method(body, headers1, method, actionurl)
                #                    print(jsonresponse)
                # filepath = "/home/adi/Downloads/TwigMeScripts-master/hlt7-json/siu/output/userinfo1.csv"

                doc_s_date,doc_s_time = start.split(' ')
                doc_s_date,doc_e_time = end.split(' ')
                doc = doctor
                print(doc)

                if json.loads(jsonresponse)['data']['elements']:
                    for info in json.loads(jsonresponse)['data']['elements']:
                        data = info['content']
                        start_time = json.loads(data)['StartDateTime']
                        end_time = json.loads(data)['EndDateTime']
                        s_date, s_time = start_time.split(' ')  # splits start date and time from server data
                        e_date, e_time = end_time.split(' ')  # splits end date and time from server data
                        dd=json.loads(data)['tags']
                        if (doc_s_date == s_date) and (doc == json.loads(data)['tags']) and ((doc_s_time == s_time)and (doc_e_time == e_time)):  # if date and doc sould be same
                                return False
                        else:
                            flag = True
                else:
                    # create_default_event(inputfile,dept_tagid,calendarID)
                    return True

                return flag

def generate_events(start,end,doctor, centre_list,centre):
        print('Control in Event function now')
        # jsondata = CM.getBaseStructure(businessID, headers1, LL.BASE_URL)
        # #   print  jsondata
        #
        # for card in jsondata['data']['elements']:
        #     if cardname == card['title']:
        #         calendarID = card['cardID']
        #         print calendarID
        #         calendarID = str(calendarID)

        for k, v in centre_list.items():
                if centre in k:
                    dept_tagid = v

        print dept_tagid

        url = LL.BASE_URL + 'genericcards/' + dept_tagid
        body = {}
        method = "POST"
        # flag=True

        jsonresponse = hit_url_method(body, headers1, method, url)

        # jsondata = CM.getBaseStructure(dept_tagid, headers1, LL.BASE_URL)

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
                        print calendarID
                        calendarID = str(calendarID)

        parseResults = ""
        counter = 0
        if parseResults == "errors":
            print "File has encoding errors"
        else:
                    method = "POST"
                    pid = ""
                    counter = counter + 1
                    eventTitle = ""
                    desc ="Doctor not available"
                    start = start
                    end = end
                    remind = 0
                    repeat = None
                    self = 'Yes'
                    allDay = 'No'
                    colour = '#F44336'
                    loc = ""
                    remind_2 = 0
                    comm_pref_reminder = 'FALSE'
                    publish_draft = 'Save & Publish'
                    occur = ''
                    tag = doctor
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
                                   "SelfRSVP": '',
                                   "MaxAttendees": 0,
                                   "NotifyRSVPStatusToAdmin": "true",
                                   "NotifyRSVPStatusToOperator": "true",
                                   "OwnerID": "",
                                   "EventID": "",
                                   "categorytype": "CalendarEvent",
                                   "PreReminder2": {"CustomMessage": "", "ReminderType": "PRE", "ReminderOffset": ""},
                                   "PreReminder1": {"CustomMessage": "", "ReminderType": "POST", "ReminderOffset": "",
                                                    "ActionCardID": ""},
                                   "PostReminder1": {"CustomMessage": "", "ReminderType": "PRE",
                                                     "ReminderOffset": remind,
                                                     "ActionCardID": ""},
                                   "ReminderDetails": {"PreReminder1": "", "PreReminder2": "", "PostReminder1": ""},
                                   "ModerateRSVP": "true",
                                   "IgnoreGuestCount": "true",
                                   "MaxGuestCount": "",
                                   "ShowOnBehalfOf": "false",
                                   "ZviceID": decTag,
                                   "CalendarID": calendarID,
                                   }


        flag = check_appointment(start,end,doctor, centre_list,centre,jsonresponse1)

        if flag == False:
                        print('Already set !!')
        else:

                    response = create_events(RequestBody, headers1, dept_tagid, calendarID)

                        #  print response
                    result = json.loads(response['reply'])
                    EventID = result['cardid']
                    u_email=""

                    tagid= CM.get_user_tagid(LL.BASE_URL, headers1,businessID,doctor )  # finding userid using doc name

                    # for a  in json.loads(jsonresponse)['data']['elements']:
                    #     if doctor == a['title']:
                    #         tagid = a['tagId']


                    print(tagid)

                    if len(tagid) != 0:  # already user is created
                        #
                        zviceID = tagid

                    else:
                        print ('USERID are not present so Creating new user \n')
                        json_user_tagid = CM.add_user_InBusiness(businessID, doctor, u_email, headers1, LL.BASE_URL)

                        json_user_tagid = json.loads(json_user_tagid)
                        zviceID = json_user_tagid['data']['usertagid']  # usertagid

                    print('Assigning appointment to doctor !!! \n')
                    rr = CM.patientinfo(calendarID, businessID, zviceID, headers1, EventID, LL.BASE_URL)

                    print 'Event gets generated !!\n'
                    print 'Event ID:', EventID
                    print 'Counter', counter
                    print "==========================="
                    print rr








def mainworkflow(body, h1, B_URL):
    global BASE_URL
    global headers1
    BASE_URL = B_URL
    headers1 = h1

    doc_start_time=0
    doc_del_time=0

#body=json.loads(r'{"Cmd":"form-submit","BusinessTag":"WH4ULS9BHSAKZ","FormID":"24204","FormTitle":"Doctor Master",
    # "FormSubmissionID":24207,
    # "FormData":{"Doctors":"D6","Center":"Burlington,NC","Start Date":"2018-05-22","End Date":"2018-05-22","Start Time":"16:30:00","End Time":"17:00:00","Monday":"false","Tuesday":"false","Wednesday":"false","Thursday":"false","Friday":"false"},"SubmittedBy":"FX5283PU679LC","tags":[],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
    if body['FormID'] == "24204":
        doc_start_date=body['FormData']['Start Date']
        doc_end_date=body['FormData']['End Date']
        doc_start_time=body['FormData']['Start Time']
        doc_end_time=body['FormData']['End Time']
        center=body['FormData']['Center']
        doctor=body['FormData']['Doctors']

        start=str(doc_start_date )+" " +str(doc_start_time)
        end=str(doc_end_date)+ " " + str(doc_end_time)
        print  doc_del_time
        print  doc_start_time

        new_start= str(doc_start_date) + " " + str('00:01:00')
        new_end=str(doc_end_date) + " " + str('23:59:00')

        centre_list = {'Burlignton,NC': 'FZYBZ2UTVUW3D', 'Spring Lake,NC': 'A8K6NKM8QSS87', 'Wilmington,NC': 'CSBZ7F4CJZYQV',
                   'Morrisville,NC': '8VPQRJEWKEGHC', 'Hope Mills,NC': 'XNEFDGYNKJ97K'}

        generate_events(new_start,start,doctor,centre_list,center)
        generate_events(end,new_end,doctor,centre_list,center)



    elif body['FormID'] == "6905":
        centre_list = {'Burlignton, NC': 'FZYBZ2UTVUW3D', 'Spring Lake, NC': 'A8K6NKM8QSS87',
                       'Wilmington, NC': 'CSBZ7F4CJZYQV',
                       'Morrisville, NC': '8VPQRJEWKEGHC', 'Hope Mills, NC': 'XNEFDGYNKJ97K'}

        UA.main(centre_list)   # calling main function assigning appointment

    elif body['FormID'] == "":

        FA.main()

