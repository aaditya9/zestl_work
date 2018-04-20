
import logon as LL
import common as CM
import json
import create_userGroup_function as CS

SERVER = "http://35.154.64.11/"
version = "v5/"
BASE_URL = SERVER + version

zviceID = "876MD568TAUH2"    ####  Business ID

email = "admin@zestl.com"
pwd = "TwigMeNow"
errorFile = "report.txt"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
with open(errorFile, "w") as ef:
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
                        title = "User Groups"
                        if title in c['title']:
                            print "3rd level"
                            url = c['actionUrl']
                            print c['actionUrl']
                            method = "GET"
                            body = {}
                            jsonresponse = CM.hit_url_method(body, headers1, method, url)
                            print jsonresponse

                        # with open(errorFile, "w") as ef:

                        ########  code for create user group  ########
                            # result = CS.create_user_group(jsonresponse)
                            # print result
                            # jsonreply = json.loads(result)
                            # print jsonreply
                            #
                            # if jsonreply['error'] == True:
                            #     message = "Error creating " + jsonreply['message'] + "\n"
                            #     ef.write(message)
                            #     print "Error creating "
                            #     print jsonreply['message']
                            # else:
                            #     print "success"

                        ###############  code for deleting the user group  #############
                        result_1 = CS.delete_user_group(jsonresponse)
                        print result_1

                        #########  Code for Editing the user group Name  ########
                        # result_2 = CS.edit_name_userGroup(jsonresponse)
                        # print result_2

                        ############### Code for  sending Mail    #########
                        # result_3 = CS.mail_mail(jsonresponse)
                        # print result_3

                        ################  Code for Notifyyy  #########
                        # result_4 = CS.mail_notify(jsonresponse)
                        # print result_4

                        ############  Code for sending Message   ##########
                        # result_5 = CS.mail_message(jsonresponse)
                        # print result_5