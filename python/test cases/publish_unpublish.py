
import logon as LL
import common as CM


SERVER = "http://35.154.64.11/"
version = "v8/"
BASE_URL = SERVER + version

zviceID = "876MD568TAUH2"    ####  Business ID

email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

for a in jsondata['data']['elements']:
    title = "test_case_form"
    if title == a['title']:
        print "go to next"
        for b in a['actions']:
            title = "Publish/Hide"
            if title == b['title']:
                print "ready"
                method = "POST"
                url = b['actionUrl']
                body = {}

                body['Flags'] = "true"
                body['FlagsInside'] = "true"
                jsonresponse = CM.hit_url_method(body, headers1, method, url)
                print jsonresponse