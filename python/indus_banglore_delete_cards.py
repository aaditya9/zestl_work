import logon as LL
import common as CM
import json
pwd = "Zspladmin99"
SERVER = "http://twig.me/"
version = "v7/"
BASE_URL = SERVER + version

zviceID = "AV9Q4BE8GB8TK"    ####  Business ID

email = "admin@zestl.com"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    title = "Picture Gallery"
    if title in a['title']:
        print "1st level"
        url = a['cturl']
        method = a['ctmethod']
        body = {"parentCardID": "870"}
        ja = CM.hit_url_method(body, headers1, method, url)
        print ja
        count = 0
        for subac in json.loads(ja)['data']['elements']:
            # count = 0
            # title = "webviewcard"
            title = "slideshowcard"
            if title in subac['cardtype']:
                print "3rd level"
                print subac['cardtype']
                for subac1 in subac['actions']:
                    title = "More Actions"
                    if title == subac1['title']:
                        print "4rth level"
                        for subac2 in subac1['actions']:
                            title = "Delete"
                            if title == subac2['title']:
                                print "5th level"
                                count = count + 1
                                print count
                                body = {}
                                method = subac2['method']
                                url = subac2['actionUrl']
                                result = CM.hit_url_method(body, headers1, method, url)
                                print result



        # print "1st level"
        # for ac in json.loads(ja)['data']['elements']:
        #     title = "Grade 10: Class Updates "
        #     if title in ac['title']:
        #         print "2nd level"
        #         url = ac['cturl']
        #         method = ac['ctmethod']
        #         body = {"parentCardID": "121"}
        #         ja = CM.hit_url_method(body, headers1, method, url)
        #         print ja
        #         for subac in json.loads(ja)['data']['elements']:
        #             title = "webviewcard"
        #             if title in subac['cardtype']:
        #                 print "3rd level"
        #                 for subac1 in subac['actions']:
        #                     title = "More Actions"
        #                     if title == subac1['title']:
        #                         print "4rth level"
        #                         for subac2 in subac1['actions']:
        #                             title = "Delete"
        #                             if title == subac2['title']:
        #                                 print "5th level"
        #                                 count = count + 1
        #                                 print count
        #                                 body = {}
        #                                 method = subac2['method']
        #                                 url = subac2['actionUrl']
        #                                 result = CM.hit_url_method(body, headers1, method, url)
        #                                 print result