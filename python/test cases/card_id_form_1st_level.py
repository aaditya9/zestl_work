import logon as LL
import common as CM
import json

SERVER = "http://35.154.64.11/"
version = "v5/"
BASE_URL = SERVER + version

zviceID = "876MD568TAUH2"

email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    #************** FORM CARD ************#

    title = "3 DEC Calendar"
    if title == a['title']:
        print "go to next"
        pid = a['cardID']
        print pid

        for ac in a['actions']:
            title = "More Actions"
            if title == ac['title']:
                print "go to next 1"

                for sub in ac['actions']:
                    title = "Delete"
                    if title == sub['title']:
                        print "ready to delete"
                        body = {}
                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_DELETE_CALENDAR"
                        body['CalendarID'] = pid
                        body['ZviceID'] = "3000001952"
                        body['categorytype'] = "CalendarCard"
                        print body['CalendarID']
                        url = sub['actionUrl']
                        method = "POST"
                        jaction = CM.hit_url_method(body, headers1, method, url)
                        print jaction