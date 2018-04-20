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
            title = "Action Customization"
            arr = []
            if title == sub['title']:
                print "1----"

                body = {}
                body['CardType'] = None
                body['CardID'] = None
                AcPref = {}
                AcPref['label'] = "Edit"
                AcPref['name'] = "Change the name"
                AcPref['type'] = "EDIT_DETAILS"
                AcPref['visible'] = "true"
                AcPref['operator'] = "true"
                AcPref['leaf'] = "true"
                # arr = []
                arr.append(AcPref)
                body['ActionPref'] = arr
                url = sub['actionUrl']
                method = sub['method']
                print body
                # jaction = CM.hit_url_method(body, headers1, method, url)
                # print jaction