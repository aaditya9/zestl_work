
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
    title = "3Dec form"
    if title in a['title']:
        print "Present"

        for sub in a['actions']:
            title = "More Actions"
            if title in sub['title']:
                print "present 1"

                for sub1 in sub['actions']:
                    title = "Delete"
                    if title in sub1['title']:
                        print "present 2"

                        body = {}
                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_DELETE_FORM"
                        body['FormID'] = "1475"
                        body['ZviceID'] = "876MD568TAUH2"
                        body['categorytype'] = "FormCard"
                        url = sub1['actionUrl']
                        method = "POST"
                        jaction = CM.hit_url_method(body, headers1, method, url)
                        print jaction

