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
    cardtype = "basecard"
    if cardtype in a['cardtype']:
        print "1st level"
        for ac in a['actions']:
            title = "Customize"
            if title in ac['title']:
                print "2nd level"
                body = {}
                body['interactionID'] = "INTERACTION_TYPE_GET_CONFIG_CARDS"
                method = "POST"
                url = ac['actionUrl']
                jaction = CM.hit_url_method(body, headers1, method, url)
                print jaction
                print "---"
                for sub in json.loads(jaction)['data']['elements']:
                    title = "Location"
                    if title in sub['title']:
                        print "3rd level"
                        body = {}
                        body['profileId'] = "LocationCard"
                        body['hidden'] = "True"
                        # body['configureHide'] = "False"
                        url = "http://35.154.64.11/v5/zvice/detailscard/876MD568TAUH2"
                        method = "POST"
                        jaction_1 = CM.hit_url_method(body, headers1, method, url)
                        print jaction_1
                        print "--"






