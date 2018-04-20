import json
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
    title = "test_case_text card"
    if title == a['title']:
        print "Found 1st level"

        for ac in a['actions']:
            title = "Add Cards"
            if title in ac['title']:
                print "Found 2nd level"

                for subac in ac['actions']:
                    title = "Add Form"
                    if title in subac['title']:
                        print "3rd level"

                        body = {}
                        fname = "Form Inside22"
                        fdesc = "inside"
                        business_tag = "876MD568TAUH2"
                        user_tag = "876MD568TAUH2"
                        # pid = "1517"
                        data1 = json.loads(subac['data'])
                        pid = data1['parentCardID']
                        print pid
                        #try this if you understand the code. take your time
                        body = {"FormTitle": fname, "FormDescription": fdesc, "ZviceID": business_tag,
                                "ZbotID": user_tag,
                                "LinkType": "FORM", "parentCardID" : pid}
                        # Q: is this the cardID of the text card you are adding inside?
                        # 1517   -- now try and see if it gets created in the correct place. we were not telling it where to create
                        # yes
                        method = "POST"
                        url = subac['actionUrl']
                        print url
                        print body

                        ## you will notice that this is actually subac['data']
                        # and the n i have taken this value from json.loads(subac['data'])['whwteverthevairableiscalled']
                        # print ac['actions'][3]['data']
                        # - making
                        # sense? think
                        # about
                        # tit and write
                        # it

                        jaction = CM.hit_url_method(body, headers1, method, url)
                        print jaction
                        print "------"



