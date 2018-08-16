import calendar
import update_appointment as UA
#import final_adt as FA
import common_aditya as CM
import login1 as LL
import urllib2
import json
import urllib
import logging
businessID = LL.zbotID
from datetime import datetime,timedelta
import credentials as CR

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

def search_alreadyexit_ornot(center,centre_list,doctor,start,doc_title):
    for k, v in centre_list.items():
        if center in k:
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

                    for a in card['actions']:
                        if "Explore" == a['title']:
                            print("inside")

                            #date, time = start.split(' ')
                            year,month,day = start.split('-')
                            #year = start[0]
                            #month = start[1]
                            actionurl = []
                            actionurl = a['actionUrl']
                            result = actionurl.replace('first_click=1', '')
                            # actionurl = result + 'filter={"year":' + year + ',"month":' + month + ',"interval":30}'
                            f = {"year": year, "month": month, 'interval': 30}
                            grp = urllib.quote(json.dumps(f))  # we use this quote function for encoding send to filter
                            actionurl = result + 'filter=' + grp

                            method = a['method']
                            body = {}
                            jsonresponse = hit_url_method(body, headers1, method, actionurl)

 #           doc_s_date, doc_s_time = start.split(' ')
#            doc_s_date, doc_e_time = end.split(' ')
            doc = doctor
            list_start = []
            list_end = []
            print(doc)
            eventID_list = []
            if json.loads(jsonresponse)['data']['elements']:
                for info in json.loads(jsonresponse)['data']['elements']:
                    data = info['content']
                    title = info['title']
                    start_time = json.loads(data)['StartDateTime']
                    end_time = json.loads(data)['EndDateTime']
                    s_date, s_time = start_time.split(' ')  # splits start date and time from server data
                    #e_date, e_time = end_time.split(' ')  # splits end date and time from server data
                    dd = json.loads(data)['tags']
                    eventID = json.loads(data)['EventID']


                    if (start == s_date) and (doc == json.loads(data)['tags']) and (doc_title == title):# and ((doc_s_time == s_time)or (doc_e_time == e_time)):
                            eventID_list.append(eventID)
                           # date,time=start_time.split(' ')
        #                result = CM.delete_event(BASE_URL, dept_tagid, calendarID, eventID, headers1)

                        #return result
                    else:
                        print('No event')
            else:
                print('No data')

            for i in eventID_list:
                result = CM.delete_event(BASE_URL, dept_tagid, calendarID, i, headers1)

    return result


def check_appointment(start,end,doctor, centre_list,centre,jsonresponse1,dept_tagid,doc_title):
    for card in json.loads(jsonresponse1)['data']['elements']:
        if 'Calendar' == card['title']:
            calendarID = card['cardID']

            for a in card['actions']:
                if "Explore" == a['title']:
                    print("inside")

                    date,time=start.split(' ')
                    final_date = date.split('-')
                    year = final_date[0]
                    month = final_date[1]
                    actionurl = []
                    actionurl = a['actionUrl']
                    result = actionurl.replace('first_click=1', '')
                    # actionurl = result + 'filter={"year":' + year + ',"month":' + month + ',"interval":30}'
                    f = {"year": year, "month": month, 'interval': 30}
                    grp = urllib.quote(json.dumps(f))  # we use this quote function for encoding send to filter
                    actionurl = result + 'filter=' + grp


                    method = a['method']
                    body = {}
                    jsonresponse = hit_url_method(body, headers1, method, actionurl)
                #                    print(jsonresponse)
                # filepath = "/home/adi/Downloads/TwigMeScripts-master/hlt7-json/siu/output/userinfo1.csv"

                doc_s_date,doc_s_time = start.split(' ')
                doc_s_date,doc_e_time = end.split(' ')
                doc = doctor
                list_start = []
                list_end = []
                print(doc)

                if json.loads(jsonresponse)['data']['elements']:
                    for info in json.loads(jsonresponse)['data']['elements']:
                        data = info['content']
                        title=info['title']
                        start_time = json.loads(data)['StartDateTime']
                        end_time = json.loads(data)['EndDateTime']
                        s_date, s_time = start_time.split(' ')  # splits start date and time from server data
                        e_date, e_time = end_time.split(' ')  # splits end date and time from server data
                        dd=json.loads(data)['tags']
                        eventID = json.loads(data)['EventID']

                        # if date and doc sould be same , start and end time will be same then event will not create!
                        if (doc_s_date == s_date) and (doc == json.loads(data)['tags']) and ((doc_s_time == s_time)and (doc_e_time == e_time)):
                                return False
                        # if (doc_s_date == s_date) and (doc == json.loads(data)['tags']) and(doc_title == title):#and ((doc_s_time != s_time)or (doc_e_time != e_time)):
                        #
                        #         #date,time=start_time.split(' ')
                        #         result=CM.delete_event(BASE_URL, dept_tagid, calendarID, eventID,headers1)
                        #
                        #         return True
                        else:
                            flag = True
                else:
                    # create_default_event(inputfile,dept_tagid,calendarID)
                    return True

                return flag

def generate_events(start,end,doctor, centre_list,centre,doc_title):
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
                    eventTitle =doc_title
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
                                   #
                                   # "RepeatOn":{"su":final_days['Sunday'],"fr":final_days['Friday'],"mo":final_days['Monday'],"tu":final_days['Tuesday'],
                                   #             "sa":final_days['Saturday'],"we":final_days['Wednesday'],"th":final_days['Thurday']},

                                   "ModerateRSVP": "true",
                                   "IgnoreGuestCount": "true",
                                   "MaxGuestCount": "",
                                   "ShowOnBehalfOf": "false",
                                   "ZviceID": decTag,
                                   "CalendarID": calendarID,
                                   }


        flag = check_appointment(start,end,doctor, centre_list,centre,jsonresponse1,dept_tagid,doc_title)

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

    #body=json.loads(r'{"Cmd":"form-submit","BusinessTag":"FWSMGL6USVKDW","FormID":"6903","FormTitle":"Doctor Master",
    # "FormSubmissionID":"6908","FormData":{"Doctors":"Test Doctor 1","Center":"Test Department, NC","Start Date":"2018-06-02",
    # "End Date":"2018-06-02","Start Time":"09:00:00","End Time":"18:00:00","Monday":"false","Tuesday":"false","Wednesday":"false",
    # "Thursday":"false","Friday":"false"},"SubmittedBy":null,"tags":[],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')


    if body['FormID'] == "6903":
        doc_start_date=body['FormData']['Start Date']
        doc_end_date=body['FormData']['End Date']
        doc_start_time=body['FormData']['Start Time']
        doc_end_time=body['FormData']['End Time']
        center=body['FormData']['Center']
        doctor=body['FormData']['Doctors']
        doc_title=body['FormData']["Blocking event title"]
        Monday=body['FormData']["Monday"]
        Tuesday = body['FormData']["Tuesday"]
        Wednesday = body['FormData']["Wednesday"]
        Thursday = body['FormData']["Thursday"]
        Friday = body['FormData']["Friday"]
        disable_appointment = body['FormData']['Disable appointment ']
        Saturday = body['FormData']["Saturday"]
        Sunday=body['FormData']["Sunday"]

        # s1='05:00:00'
        # format = '%H:%M:%S'
        # doc_start_time = datetime.strptime(doc_start_time, format) - datetime.strptime(s1, format)
        # doc_end_time=datetime.strptime(doc_end_time, format) - datetime.strptime(s1, format)

        final_days={}
        final_days={'Monday' : Monday,'Tuesday' : Tuesday,'Wednesday' : Wednesday,'Thursday' : Thursday,'Friday' :Friday,'Saturday':Saturday,'Sunday':Sunday}

        total_days=[]
        remaining_days=[]
        for k, v in final_days.items():
            if 'true' == v:
                day = k
                total_days.append(day)
            if 'false' == v:
                day = k
                remaining_days.append(day)
            #else:

        print total_days  # days which are selected by doctor



        centre_list=CR.centre_list
        if   doc_start_date:
            year, month, day = doc_start_date.split('-')
            start_date = datetime(int(year), int(month), int(day))
            start_date.strftime("%Y-%m-%d")
        else:
           print('')

        if  doc_end_date:
            year, month, day = doc_end_date.split('-')
            end_date = datetime(int(year), int(month), int(day))
            end_date.strftime("%Y-%m-%d")



        def cal_date(start,end,total_days):
            d = start
            datelist = []
            delta = timedelta(days=1)
            while d <= end:
                # final = d.strftime("%Y-%m-%d")
                cal_day = calendar.day_name[d.weekday()]
                for i in total_days:
                    if (cal_day == i):
                        print(d)
                        final = d.strftime("%Y-%m-%d")
                        datelist.append(final)
                d += delta

            return datelist

        if total_days == []:
                d = start_date
                date_list = []
                delta = timedelta(days=1)
                while d <= end_date:
                    final = d.strftime("%Y-%m-%d")
                    date_list.append(final)
                    d += delta
        else:
                date_list=cal_date(start_date,end_date,total_days)  # returns particular dates which doctor select days

        for final in date_list:
            new_start= str(final) +' '+str('00:01:00')
            start=str(final)+' '+str(doc_start_time)

            new_end=str(final)+' '+ str('23:59:00')
            end=str(final) + ' '+str(doc_end_time)

            flag = False

            if (disable_appointment) == 'true':
                RESPONSE = search_alreadyexit_ornot(center, centre_list, doctor, final, doc_title)
                print(RESPONSE)
                flag = True

            if flag == False:
                RESPONSE=search_alreadyexit_ornot(center,centre_list,doctor,final,doc_title)
                print(RESPONSE)
                generate_events(new_start, start, doctor, centre_list, center,doc_title)
                generate_events(end,new_end,doctor,centre_list,center,doc_title)

############### code for without mentioned days #########

        if remaining_days == []:
            d = start_date
            date_list = []
            delta = timedelta(days=1)
            while d <= end_date:
                final = d.strftime("%Y-%m-%d")
                #date_list.append(final)
                d += delta
        else:
            date_list = cal_date(start_date, end_date, remaining_days)  # returns particular dates which doctor select days


        for final in date_list:
            new_start = str(final) + ' ' + str('00:01:00')
            start = str(final) + ' ' + str('12:00:00')
            new_end = str(final) + ' ' + str('23:59:00')
            end = str(final) + ' ' + str('12:01:00')
            flag = False

            if (disable_appointment) == 'true':
                RESPONSE = search_alreadyexit_ornot(center, centre_list, doctor, final, doc_title)
                print(RESPONSE)
                flag = True

            if flag == False:
                RESPONSE = search_alreadyexit_ornot(center, centre_list, doctor, final, doc_title)
                print(RESPONSE)
                generate_events(new_start, start, doctor, centre_list, center, doc_title)
                generate_events(end, new_end, doctor, centre_list, center, doc_title)

##########################################################################################################################





    if body['FormID'] == "7069":
        doc_start_date=body['FormData']['Start Date']
        doc_end_date=body['FormData']['End Date']
        doc_start_time=body['FormData']['Start Time']
        doc_end_time=body['FormData']['End Time']
        center=body['FormData']['Center']
        doctor=body['FormData']['Doctors']
        doc_title = body['FormData']["Blocking event title"]
        disable_appointment=body['FormData']['Disable appointment ']

        centre_list = CR.centre_list
        year, month, day = doc_start_date.split('-')

        start_date = datetime(int(year), int(month), int(day))
        start_date.strftime("%Y-%m-%d")

        year, month, day = doc_end_date.split('-')
        end_date = datetime(int(year), int(month), int(day))
        end_date.strftime("%Y-%m-%d")

        d = start_date
        delta = timedelta(days=1)
        while d <= end_date:
            # print d.strftime("%Y-%m-%d")
            final = d.strftime("%Y-%m-%d")

            #new_start = str(final) + ' ' + str('00:01:00')
            start = str(final) + ' ' + str(doc_start_time)

            #new_end = str(final) + ' ' + str('23:59:00')
            end = str(final) + ' ' + str(doc_end_time)

            RESPONSE = search_alreadyexit_ornot(center, centre_list, doctor, final, doc_title)

            generate_events(start, end, doctor, centre_list, center, doc_title)
            #generate_events(end, new_end, doctor, centre_list, center, doc_title)

            print(final)
            d += delta




    if body["FormID"]== "7082":
        # {"Cmd": "form-submit", "BusinessTag": "FWSMGL6USVKDW", "FormID": "7082",
        #               "FormTitle": "User Master", "FormSubmissionID": 7083,
        #               "FormData": {"Patient name": "KAILAS Bhosale", "PID": "928371", "Address": null,
        #                            "Alternate ID": null, "Contact No. ": null, "Parent Name": null,
        #                            "Email": "Abc@abc.com"}, "SubmittedBy": "66C4U8H3U585T", "tags": [],
        #               "url_params": {"users": "{\"selected\":\"5QJGA7PJX3F36\"}"}}


        UserID=body['FormData']['User ID']

        #
        # body = {}
        # url = "https://www.twig.me/v13/"+ UserID +'/linktotwigmeuser'
        # method = "GET"
        # jsonreply = CM.hit_url_method(body, headers1, method, url)
        # return jsonreply

        jsonreply=CM.linktwigmeuser(LL.BASE_URL,UserID,headers1)


        zviceID = body['BusinessTag']

        if body['FormData']['Email'] !='':
                    card = json.loads(jsonreply)['linkeduserid']
                    if card == None:
                        logging.warning('Now assigning emailid')
                        emailID = body['FormData']['Email']
                        # method="POST"
                        # url=LL.BASE_URL+ 'zvice/interaction/' + zviceID
                        # body = {"interactionID": "CommonInteraction_INTERACTION_TYPE_LINK_USERPROFILE", "linkemail": emailID}
                        # jsonresponse1 = hit_url_method(body, headers1, method, url)

                        jsonresponse1 = CM.linkemail(LL.BASE_URL, UserID, emailID, headers1)
                        logging.warning(jsonresponse1)
                        print(jsonresponse1)

                    else:
                        print('Already linked !!')
        else:
            print ('Enter email')