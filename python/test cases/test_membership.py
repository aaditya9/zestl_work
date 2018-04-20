import logon as LL
import common as CM
import json


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
    # cardtype = "Minal Test"
    if cardtype in a['cardtype']:
        # if cardtype in a['title']:
        print "1st level"
        for b in a['actions']:
            title = "Settings"
            if title == b['title']:
                print "2nd level"
                for c in b['actions']:
                    title = "Membership Plans"
                    if title in c['title']:
                        print "3rd level"
                        url = c['actionUrl']
                        print c['actionUrl']
                        method = "GET"
                        body = {}
                        jsonresponse = CM.hit_url_method(body, headers1, method, url)
                        print jsonresponse

                        ########## Edit Membership #######

                        for sub in json.loads(jsonresponse)['data']['elements']:
                            title = "Gym"
                            if title in sub['title']:
                                print "title"
                                for sub1 in sub['actions']:
                                    title = "Edit Membership Plan"
                                    if title == sub1['title']:
                                        print "ready to edit"
                                        url = sub1['actionUrl']
                                        method = "PUT"
                                        body = {}
                                        body['Title'] = "Gym minal"
                                        body['Description'] = "Gym"
                                        body['Fees'] = "100"
                                        body['Duration'] = "2"
                                        body['NumSessions'] = "2"
                                        body['SessionDuration'] = "2"
                                        body['SessionDurationUnit'] = "2"
                                        jsonresponse = CM.hit_url_method(body, headers1, method, url)
                                        print jsonresponse




                                        ###################3  To delete the membership #############

                        # for sub in json.loads(jsonresponse)['data']['elements']:
                        #     title = "Gym"
                        #     if title in sub['title']:
                        #         print "title"
                        #         for sub1 in sub['actions']:
                        #             title = "Delete Membership Plan"
                        #             if title == sub1['title']:
                        #                 print "ready to delete"
                        #                 body = {}
                        #                 method = "POST"
                        #                 url = sub1['actionUrl']
                        #                 jsonresponse = CM.hit_url_method(body, headers1, method, url)
                        #                 print jsonresponse


                        ##############   To create the membership    #########33
                        # for sub in json.loads(jsonresponse)['data']['floating_menu']['floating_buttons']:
                            # title = "Add New Membership Plan"
                            # if title in sub['title']:
                            #     print "ready to add"
                            #     url = sub['actionUrl']
                            #     method = "POST"
                            #     body = {}
                            #     body['Title'] = "Gym"
                            #     body['Description'] = "Gym"
                            #     body['Fees'] = "100"
                            #     body['Duration'] = "2"
                            #     body['NumSessions'] = "2"
                            #     body['SessionDuration'] = "2"
                            #     body['SessionDurationUnit'] = "2"
                            #     jsonresponse = CM.hit_url_method(body, headers1, method, url)
                            #     print jsonresponse