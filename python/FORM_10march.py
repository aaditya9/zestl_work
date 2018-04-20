import logon as LL
import common as CM

SERVER = "https://twig.me/"
version = "v7/"
BASE_URL = SERVER + version

zviceID = "8SFKZCV5PFAXV"
email = "admin@zestl.com"
pwd = ""

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    title = "Calendar"
    # cardtype = "basecard"
    if title in a['title']:
        print "1st level"
        for ac in a['actions']:
            title = "Explore"
            if title in ac['title']:
                print "2nd level"
                body = {}
                url = ac['actionUrl']
                method = "GET"
                body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_SHOW_CALENDAR_EVENTS"
                body['CalendarID'] = 66
                body['ZviceID'] = 3000090721
                body['DefaultView'] = 4
                body['categoryType'] = "CalendarCard"
                jaction = CM.hit_url_method(body, headers1, method, url)
                print jaction




    #             for subac in ac['actions']:
    #                 title1 = "Add Form"
    #                 if title1 in subac['title']:
    #                     print "3rd level"
    #                     body = {}
    #                     url =subac['actionUrl']
    #                     print subac['actionUrl']
    #                     body = {}
    #                     title = "10March_form"
    #                     desc = "10March_form"
    #                     business_tag = "876MD568TAUH2"
    #                     user_tag = "876MD568TAUH2"
    #
    #                     body = {"FormTitle": title, "FormDescription": desc, "ZviceID": business_tag,
    #                             "ZbotID": user_tag,
    #                             "LinkType": "FORM"}
    #
    #                     method = "POST"
    #                     url = subac['actionUrl']
    #                     jaction = CM.hit_url_method(body, headers1, method, url)
    #                     print jaction
    #                     print "------"