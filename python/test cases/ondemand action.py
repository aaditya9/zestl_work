import logon as LL
import common as CM
import json

SERVER = "http://35.154.64.11/"
version = "v8/"
BASE_URL = SERVER + version

zviceID = "876MD568TAUH2"

email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    title = "Minal Test"
    if title == a['title']:
        print "----"

        for sub in a['actions']:
            title = "All actions"
            if title == sub['title']:
                print "1----"
                body = {}
                url = sub['actionUrl']
                method = sub['method']
                jaction = CM.hit_url_method(body, headers1, method, url)
                print jaction

                for sub1 in json.loads(jaction)['data']['ondemand_action']:
                    title = "Add Card"
                    if title == sub1['title']:
                        print "ON demand"
                        body = {}
                        url = sub1['actionUrl']
                        method = sub1['method']
                        jaction = CM.hit_url_method(body, headers1, method, url)
                        print jaction

                        for sub2 in json.loads(jaction)['data']['ondemand_action']:
                            title = "Add Text Card"
                            if title == sub2['title']:
                                print "ON demand 1"
                                body = {}
                                tcardname = "text_21 card"
                                icardDes = "text_21 card"
                                body['cardData'] = {"title": tcardname, "desc": icardDes, "Flags": False}
                                body['cardType'] = "TEXT"
                                body['opType'] = 1
                                body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
                                method = "POST"
                                url = sub2['actionUrl']
                                jaction = CM.hit_url_method(body, headers1, method, url)
                                print jaction