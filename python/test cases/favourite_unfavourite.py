import logon as LL
import common as CM

SERVER = "http://35.154.64.119/"
version = "v5/"
BASE_URL = SERVER + version

zviceID = "876MD568TAUH2"    ####  Business ID

email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
#********** Favourite ************#
for a in jsondata['data']['elements']:
    title = "Minal lib"
    if title == a['title']:
        print "go to next"
        for ac in a['actions']:
            title = "Favorite"
            if title == ac['title']:
                print "go to next 1"
                body = {}
                body['currentvalue'] = False   #**** put True value to favourite . and put False value to Unfavourite******
                method = "PUT"
                url = ac['actionUrl']
                print  url
                jsonresponse = CM.hit_url_method(body, headers1, method, url)
                print jsonresponse


