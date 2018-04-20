import logon as LL
import common as CM

SERVER = "http://35.154.64.11/"
version = "v5/"
BASE_URL = SERVER + version

zviceID = "876MD568TAUH2"    ####  Business ID

email = "admin@zestl.com"
pwd = ""

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    title = "test_ForumCard"
    if title == a['title']:
        print "go to next"
        for ac in a['actions']:
            title = "Add Comment"
            if title == ac['title']:
                print "go to next 1"
                method = "POST"
                url = ac['actionUrl']
                body = {}
                body['Text'] = "today is 16 feb"
                jsonresponse = CM.hit_url_method(body, headers1, method, url)
                print jsonresponse