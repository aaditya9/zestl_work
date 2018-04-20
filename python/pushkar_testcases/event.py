
import logon as LL
import common as CM
import info as info
import requests

BASE_URL = info.url
email = info.email
pwd = info.pwd
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

def create_events(body, headers, bId, calendarID):
    return LL.invoke_rest('POST', LL.BASE_URL + bId + '/calendars/' + calendarID + '/events', json.dumps(body),
                          headers)

def add_events(allDay,eventTitle,occur,desc,bId,remind,repeat,self,loc,colour,start,calendarID,end):
    RequestBody = {"AllDay": allDay,
                   "OwnerID": "",
                   "EventID": "",
                   "categorytype": "CalendarEvent",
                   "Title": eventTitle,
                   "Occurrences": occur,
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
    response = create_events(RequestBody, headers1, bId, calendarID)
    print response