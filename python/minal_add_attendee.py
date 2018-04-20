
import json
import csv
import logon as LL
import common as CM
import re
import requests


SERVER = "http://35.154.64.11/"
version = "v5/"
BASE_URL = SERVER + version


zviceID = "876MD568TAUH2"    ####  Business ID

email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    title = "Test calendar"
    if title in a['title']:
        body = {}
        # body['EventID'] = "1703"
        body['CalendarID'] = "6"
        body['categoryType'] = "CalendarCard"
        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_SHOW_CALENDAR_EVENTS"
        method = "GET"
        # url = a['cardsjsonurl']
        url = "http://35.154.64.11/v5/876MD568TAUH2/calendars/6/events/?filter={\"interval\":30,\"month\":1,\"year\":2017}"
        ja = CM.hit_url_method(body, headers1, method, url)
        print ja
        print "found 1"
        for ac in json.loads(ja)['data']['elements']:
            title = "Minal"
            if title in ac['title']:
                print "Found 2"

                body = {}
                body['EventID'] = "1703"
                body['CalendarID'] = "6"
                body['categoryType'] = "CalendarCard"
                body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_SHOW_CALENDAR_EVENTS"
                method = "GET"

                # body = {}
                # body['EventID'] = "1703"
                # method = "GET"
                url = "http://35.154.64.11/v5/876MD568TAUH2/calendars/6/events/1703"
                jasub = CM.hit_url_method(body, headers1, method, url)
                print jasub

                # for subac in json.loads(jasub)['actions']:
                #     title = "More Actions"
                #     if title in subac1['title']:
                #         print "3rd level"


                for subac in json.loads(jasub)['data']['elements']:
                    title = "Minal"
                    if title in subac['title']:
                        print "Found 2"

                # for subac in json.loads(jasub)['actions']:
                        for subac1 in subac['actions']:
                            title = "More Actions"
                            if title in subac1['title']:
                                print "3rd level"

                                for subac2 in subac1['actions']:
                                    title = "Add Attendee"
                                    if title in subac2['title']:
                                        print "found"

                                        body = {}
                                        # body['Name'] ="minal"
                                        body['ChildTagID'] = "6VT32S759JLR5"
                                        body['interactionID']= "CommonInteraction_INTERACTION_TYPE_SEARCH_FOR_AUTOCOMPLETE"
                                        body['searchType'] = 1
                                        # body['EmailID'] = "minal@gmail.com"
                                        #{"url":"http:\/\/35.154.64.11\/v5\/zvice\/interaction\/876MD568TAUH2","method":"POST","jsondata":"
                                        method = "POST"
                                        url = subac2['actionUrl']
                                        jaction = CM.hit_url_method(body, headers1, method, url)
                                        print jaction

