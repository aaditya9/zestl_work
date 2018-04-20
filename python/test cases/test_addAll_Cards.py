import logon as LL
import common as CM
import json
import addAll_Card_functions as CF

SERVER = "http://35.154.64.11/"
version = "v7/"
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
        if cardtype == a['cardtype']:
            print "1st level"

            for ac in a['actions']:
                title = "Add Cards"
                if title in ac['title']:
                    print "2nd level"

                    ######### To add a Form Card  ##########
                    result = CF.create_form_card(ac)
                    print result

                    #######To add a Text card #####
                    # result = CF.create_text_card(ac)
                    # print result

                    ##### To add a Link card ####
                    # result = CF.create_Link_card(ac)
                    # print result

                    ###### To add a Forum card  ####
                    # result = CF.create_Forum_card(ac)
                    # print result

                    #####  To add a Location Tacking card   ###
                    # result = CF.create_LocationTrack_card(ac)
                    # print result

                    ##### To add a Calendar Card ###
                    # result = CF.create_Calendar_card(ac)
                    # print result

                    ###### To add a Gallery card ###
                    # result = CF.create_Gallery_card(ac)
                    # print result

                    #### To add a Attendance card ####
                    # result = CF.create_Attendance_card(ac)
                    # print result

                    #### To add a Product card ####
                    # result = CF.create_product_card(ac)
                    # print result

                    #### To add a Baner card ####
                    # result = CF.create_Baner_card(ac)
                    # print result

                    ##### To add a Department ###
                    # result = CF.create_Department(ac)
                    # print result

                    jsonreply = json.loads(result)
                    print jsonreply

                    if jsonreply['error'] == True:
                        message = "Error creating " + jsonreply['message'] + "\n"
                        ef.write(message)
                        print "Error creating "
                        print jsonreply['message']
                    else:
                        if jsonreply['error'] == False:
                            message = "created successfully " + jsonreply['message'] + "\n"
                            ef.write(message)
                            print "Done"
                            print jsonreply['message']