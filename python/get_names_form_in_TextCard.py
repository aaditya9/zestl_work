import logon as LL
import common as CM
import json
import password as PP

SERVER = "https://www.twig.me/"
version = "v8/"
BASE_URL = SERVER + version
# zviceID = "8TXR286YC9SYK"    ####  Business ID
# zviceID = "EUNXYEQF7TGHR"
zviceID = "CW7ZBJ8C3H9DL"
email = "admin@zestl.com"
pwd = PP.pwd

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
# cardname = "EYP"
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    if a['backgroundImageUrl'] in "https://twig.me/images/default_cards/text_card.png":
        print a['title'] + "************"
        if a['cardtype'] == "buttoncard":
            method = "GET"
            url = a['actions'][0]['actionUrl']
            body = {}
            jsondata = CM.hit_url_method(body, headers1, method, url)
            # print jsondata
            for sub in json.loads(jsondata)['data']['elements']:
                if sub['backgroundImageUrl'] == "https://twig.me/images/default_cards/form.png":
                    # print "present"
                    title = sub['title']
                    print title