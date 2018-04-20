import logon as LL
import common as CM
import info as info
import json
import sys
import requests
import urllib2

import hashlib\

BASE_URL = info.url
email = info.email
pwd = info.pwd
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

def add_events(allDay,eventTitle,occur,desc,bId,remind,repeat,self,loc,colour,start,calendarID,end,remind2,flag):
    decurl = "http://twig.me/v1/push/dectest/" + bId
    response = urllib2.urlopen(decurl)
    html = response.read()
    decTag = json.loads(html)['decTagID']

    body = {}
    body['AllDay'] = allDay
    body['OwnerID'] = ""
    body['EventID'] = ""
    body['categorytype'] = "CalendarEvent"
    body['Title'] = eventTitle
    body['Occurrences'] = occur
    body['Description'] = desc
    body['ZviceID'] = decTag
    body['RemindBefore'] = remind
    body['RemindBeforeTwo'] = remind2
    body['RepeatEvent'] = repeat
    body['SelfRSVP'] = self
    body['Location'] = loc
    body['Color'] = colour
    body['StartDateTime'] = start
    body['MaxAttendees'] = ""
    body['CalendarID'] = calendarID
    body['EndDateTime'] = end
    body['RemindCommPref'] = flag

    method = "POST"
    url = BASE_URL + bId + '/calendars/' + calendarID + '/events'
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction