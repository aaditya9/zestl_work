import logon as LL
import common as CM

SERVER = "https://twig.me/"
version = "v7/"
BASE_URL = SERVER + version

# BASE_URL ="https://twig.me/v7/" ### Production

zviceID = "8SFKZCV5PFAXV"    ####  Business ID

email = "admin@zestl.com"
pwd = "Zspladmin99"
tag = "3YT5ZY5DV3RDL"
tag1 = "3U65UQ7KLYGEB"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    cardtype = "basecard"
    if cardtype in a['cardtype']:
        print "1st level"

        for b in a['actions']:
            title = "Settings"
            if title == b['title']:
                print "----"
                for c in b['actions']:
                    title = "SuperAdmin"
                    if title == c['title']:
                        print "done"

                        for data in c['inputs'][5]['properties']:
                            title = "default"
                            if title == data['name']:
                                print "----"
                                id = data['value']
                                print id
                                if id == tag:
                                    print "matching"
                                    method = "POST"
                                    url = ""
                                    body = {"title": "Minal", "desc": "","interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
                                    body['PrimaryOwnerITagID'] = tag1
                                    subja = CM.hit_url_method(body, headers1, method, url)
                                    print subja
                                    # data['value'] = tag1
                                    # print "success"
                                # else:print "go for next"
                        # method = "POST"
                        # url = c['actionUrl']
                        # body = {}
                        # jaction = CM.hit_url_method(body, headers1, method, url)
                        # print jaction

                        # tag = body['PrimaryOwnerITagID']
                        # print tag




