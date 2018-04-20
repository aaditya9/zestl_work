import logon as LL
import common as CM
import json

SERVER = "http://35.154.64.11/"
version = "v5/"
BASE_URL = SERVER + version

zviceID = "876MD568TAUH2"    ####  Business ID

email = "admin@zestl.com"
pwd = "TwigMeNow"
# errorFile = "report.txt"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
# with open(errorFile, "w") as ef:
for a in jsondata['data']['elements']:
    cardtype = "basecard"
    # cardtype = "Minal Test"
    if cardtype in a['cardtype']:
    # if cardtype in a['title']:
        print "1st level"
        for b in a['actions']:
            title = "Settings"
            if title == b['title']:
                print "2nd level"
                for c in b['actions']:
                    title = "User Groups"
                    if title in c['title']:
                        print "3rd level"
                        url = c['actionUrl']
                        print c['actionUrl']
                        method = "GET"
                        body = {}
                        jsonresponse = CM.hit_url_method(body, headers1, method, url)
                        print jsonresponse
                        for sub in json.loads(jsonresponse)['data']['elements']:
                            title = "Test 2"
                            if title == sub['title']:
                                print "3rd level"
                                body = {}
                                url = sub['cardsjsonurl']
                                method = "GET"
                                jsonresponse = CM.hit_url_method(body, headers1, method, url)
                                print jsonresponse
                                for sub1 in json.loads(jsonresponse)['data']['elements']:
                                    title = "textcard"
                                    if title == sub1['cardtype']:
                                        print "4rth level"
                                        for sub2 in sub1['actions']:
                                            title = "Settings"
                                            if title == sub2['title']:
                                                print "5th level"
                                                for sub3 in sub2['actions']:
                                                    title = "Add User to Group"
                                                    if title == sub3['title']:
                                                        print "6th level"
                                                        body = {}
                                                        method = "POST"
                                                        userid = "7J3WGYV6BYCCU"
                                                        url = sub3['actionUrl']
                                                        body['grpUserZviceID'] = userid
                                                        body['groupid'] = 2
                                                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_SEARCH_FOR_AUTOCOMPLETE"
                                                        body['searchType'] = 1
                                                        jsonresponse = CM.hit_url_method(body, headers1, method, url)
                                                        print jsonresponse