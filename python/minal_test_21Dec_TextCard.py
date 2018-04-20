
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
            title = "Add Cards"
            if title in ac['title']:
                print "2nd level"

                for subac in ac['actions']:
                    title1 = "Add Text Card"
                    if title1 in subac['title']:
                        print "3rd level"

                        body = {}
                        tcardname = "abc"
                        icardDes = "done"



                        body['cardData'] = {"title": tcardname, "desc": icardDes, "Flags":False}
                        body['cardType'] = "TEXT"
                        body['opType'] = 1
                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
                        method = "POST"
                        url = subac['actionUrl']
                        print url
                        print "-"
                        jaction = CM.hit_url_method(body, headers1, method, url)
                        # print jaction
                        # print "------"