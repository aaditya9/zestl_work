import common as CM
import logon as LL
import json

SERVER = "http://35.154.64.11/"
version = "v7/"
BASE_URL = SERVER + version

email = "admin@zestl.com"
pwd = "TwigMeNow"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

######## To add a Form Card   ##############
def create_form_card(ac):
    for subac in ac['actions']:
        title1 = "Add Form"
        if title1 in subac['title']:
            print "3rd level"
            body = {}
            method = subac['method']
            url = subac['actionUrl']
            print subac['actionUrl']
            jaction = CM.hit_url_method(body, headers1, method, url)
            print jaction
            #
            # for subac1 in json.loads(jaction)['data']['ondemand_action']:
            #     title1 = "Add Form"
            #     if title1 in subac1['title']:
            #         print "4rth level"

            title = "form 6 march"
            desc = "test_case_form"
            business_tag = "876MD568TAUH2"
            user_tag = "876MD568TAUH2"
            body = {"FormTitle": title, "FormID": "", "FormDescription": desc, "ZviceID": business_tag,
                    "ZbotID": user_tag,"LinkType": "FORM", "LinkID": ""}
            method = "POST"
            url = subac['actionUrl']
            jaction = CM.hit_url_method(body, headers1, method, url)
            return jaction

#######To add a Text card #####
def create_text_card(ac):
    for subac in ac['actions']:
        title1 = "Add Text"
        if title1 in subac['title']:
            print "3rd level"
            body = {}
            tcardname = "test_case_text card"
            icardDes = "test_case_text card"
            body['cardData'] = {"title": tcardname, "desc": icardDes, "Flags":False}
            body['cardType'] ="TEXT"
            body['opType'] = 1
            body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
            method = "POST"
            url = subac['actionUrl']
            jaction = CM.hit_url_method(body, headers1, method, url)
            return jaction

def create_Link_card(ac):
    for subac in ac['actions']:
        title1 = "Add Link Card"
        if title1 in subac['title']:
            print "3rd level"

            body = {}
            tcardname = "test_linkCard"
            icardDes = "test_linkCard"
            dlink = "www.youtube.com"

            body['cardData'] = {"title": tcardname, "desc": icardDes, "link": dlink}
            body['cardType'] = "LINK"
            body['opType'] = 1
            body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
            method = "POST"
            url = subac['actionUrl']
            jaction = CM.hit_url_method(body, headers1, method, url)
            return jaction

###### To add a Forum card  ####
def create_Forum_card(ac):
    for subac in ac['actions']:
        title1 = "Add Forum"
        if title1 in subac['title']:
            print "3rd level"
            body = {}
            body['Text'] = "test_ForumCard"
            body['Flags'] = False
            body['FlagsInside'] = False
            method = "POST"
            url = subac['actionUrl']
            jaction = CM.hit_url_method(body, headers1, method, url)
            return jaction

#####  To add a Location Tacking card  ###
def create_LocationTrack_card(ac):
    for subac in ac['actions']:
        title1 = "Add Location Tracking"
        if title1 in subac['title']:
            print "3rd level"
            body = {}
            body['Title'] = "test_location track"
            body['Description'] = "test_location track"
            method = "POST"
            url = subac['actionUrl']
            jaction = CM.hit_url_method(body, headers1, method, url)
            return jaction

##### To add a Calendar Card ###
def create_Calendar_card(ac):
    for subac in ac['actions']:
        title1 = "Add Calendar Card"
        if title1 in subac['title']:
            print "3rd level"
            body = {}
            body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_EDIT_CALENDAR"
            body['categorytype'] = "Calendar"
            body['CalendarID'] = ""
            body['ZviceID'] = 3000001952
            body['LinkType'] = "CALENDAR"
            body['Title'] = "test_calendar_card"
            body['Description'] = "test_calendar_card"
            body['DefaultView'] = "List View"
            method = "POST"
            url = subac['actionUrl']
            jaction = CM.hit_url_method(body, headers1, method, url)
            return jaction

###### To add a Gallery card ###
def create_Gallery_card(ac):
    for subac in ac['actions']:
        title1 = "Add Gallery Card"
        if title1 in subac['title']:
            print "3rd level"
            body = {}
            body['Title'] = "test_gallery_card"
            body['Description'] = "test_gallery_card"
            body['Flags'] = False
            method = "POST"
            url = subac['actionUrl']
            jaction = CM.hit_url_method(body, headers1, method, url)
            return jaction


###### To add a Attendace card ###
def create_Attendance_card(ac):
    for subac in ac['actions']:
        title1 = "Add Attendance Scan"
        if title1 in subac['title']:
            print "3rd level"
            body = {}
            body['Title'] = "test_Attendace_card"
            body['Description'] = "test_Attendace_card"
            body['ScanType'] = "FAST"
            body['MembershipPlanID'] = "NONE"
            url = subac['actionUrl']
            method = "POST"
            jaction = CM.hit_url_method(body, headers1, method, url)
            return jaction


###### To add a Product card ###
def create_product_card(ac):
    for subac in ac['actions']:
        title1 = "Add Product Showcase Card"
        if title1 in subac['title']:
            print "3rd level"
            body = {}
            body['Title'] = "test_product_card"
            body['Description'] = "test_product_card"
            url = subac['actionUrl']
            method = "POST"
            jaction = CM.hit_url_method(body, headers1, method, url)
            return jaction

###### To add a Baner card ###
def create_Baner_card(ac):
    for subac in ac['actions']:
        title1 = "Add Banner Card"
        if title1 in subac['title']:
            print "3rd level"
            body = {}
            body['Title'] = "test_baner_card"
            body['Description'] = "test_baner_card"
            url = subac['actionUrl']
            method = "POST"
            jaction = CM.hit_url_method(body, headers1, method, url)
            return jaction

######## To add a Department Card ########
def create_Department(ac):
    for subac in ac['actions']:
        title1 = "Add Department"
        if title1 in subac['title']:
            print "3rd level"
            body = {}
            body['title'] = "Test_Department"
            body['zviceinfo'] = "Test_Department"
            body['zviceid'] = "E9YFEQ3GC9ZQQ"
            body['zbotid'] = "876MD568TAUH2"
            body['zvicetype'] = "ZTAG"
            body['zvicelink'] = "NEW"
            body['lat'] = "-"
            body['long'] = "-"
            body['zviceloc'] = "---"
            body['tagprofilestr'] = "ORGANISATION"
            url = subac['actionUrl']
            method = "PUT"
            jaction = CM.hit_url_method(body, headers1, method, url)
            return jaction