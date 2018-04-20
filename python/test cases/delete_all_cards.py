import logon as LL
import common as CM
import json

SERVER = "http://35.154.64.11/"
version = "v5/"
BASE_URL = SERVER + version

zviceID = "876MD568TAUH2"

email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    #************** FORM CARD ************#

    # title = "test_case_form"
    # if title == a['title']:
    #     print "go to next"
    #
    #     for ac in a['actions']:
    #         title = "More Actions"
    #         if title == ac['title']:
    #             print "go to next 1"
    #
    #             for sub in ac['actions']:
    #                 title = "Delete"
    #                 if title == sub['title']:
    #                     print "ready to delete"
    #                     body = {}
    #                     body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_DELETE_FORM"
    #                     body['FormID'] = 1718
    #                     body['ZviceID'] = "876MD568TAUH2"
    #                     body['categorytype'] = "FormCard"
    #                     url = sub['actionUrl']
    #                     method = "POST"
    #                     jaction = CM.hit_url_method(body, headers1, method, url)
    #                     print jaction

    #*********** TEXT CARD  ******************#
    # title = "test_case_text card"
    # if title == a['title']:
    #     print "go to next"
    #
    #     for ac in a['actions']:
    #         title = "More Actions"
    #         if title == ac['title']:
    #             print "go to next 1"
    #
    #             for sub in ac['actions']:
    #                 title = "Delete"
    #                 if title == sub['title']:
    #                     print "ready to delete"
    #                     body = {}
    #                     body['cardID'] = 1719
    #                     body['opType'] = 2
    #                     body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
    #                     url = sub['actionUrl']
    #                     method = "POST"
    #                     jaction = CM.hit_url_method(body, headers1, method, url)
    #                     print jaction

    #********* LINK CARD *************#
    # title = "test_linkCard"
    # if title == a['title']:
    #     print "go to next"
    #
    #     for ac in a['actions']:
    #         title = "More Actions"
    #         if title == ac['title']:
    #             print "go to next 1"
    #
    #             for sub in ac['actions']:
    #                 title = "Delete"
    #                 if title == sub['title']:
    #                     print "ready to delete"
    #                     body = {}
    #                     body['cardID'] = 1720
    #                     body['opType'] = 2
    #                     body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
    #                     url = sub['actionUrl']
    #                     method = "POST"
    #                     jaction = CM.hit_url_method(body, headers1, method, url)
    #                     print jaction

    #******* LOCATION TRACK CARD **********#
    # title = "test_location track"
    # if title == a['title']:
    #     print "go to next"
    #
    #     for ac in a['actions']:
    #         title = "More Actions"
    #         if title == ac['title']:
    #             print "go to next 1"
    #
    #             for sub in ac['actions']:
    #                 title = "Delete"
    #                 if title == sub['title']:
    #                     print "ready to delete"
    #                     body = {}
    #                     body['LTCardID'] = 1722
    #                     url = sub['actionUrl']
    #                     method = "POST"
    #                     jaction = CM.hit_url_method(body, headers1, method, url)
    #                     print jaction

#************** CALENDAR CARD ********#
    # title = "test_calendar_card"
    # if title == a['title']:
    #     print "go to next"
    #
    #     for ac in a['actions']:
    #         title = "More Actions"
    #         if title == ac['title']:
    #             print "go to next 1"
    #
    #             for sub in ac['actions']:
    #                 title = "Delete"
    #                 if title == sub['title']:
    #                     print "ready to delete"
    #                     body = {}
    #                     body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_DELETE_CALENDAR"
    #                     body['CalendarID'] = 1724
    #                     body['ZviceID'] ="3000001952"
    #                     body['categorytype'] = "CalendarCard"
    #                     url = sub['actionUrl']
    #                     method = "POST"
    #                     url = sub['actionUrl']
    #                     jaction = CM.hit_url_method(body, headers1, method, url)
    #                     print jaction

#***** Gallery Card *********#
    # title = "test_gallery_card"
    # if title == a['title']:
    #     print "go to next"
    #
    #     for ac in a['actions']:
    #         title = "More Actions"
    #         if title == ac['title']:
    #             print "go to next 1"
    #
    #             for sub in ac['actions']:
    #                 title = "Delete"
    #                 if title == sub['title']:
    #                     print "ready to delete"
    #                     body = {}
    #                     body['GalleryID'] = 1725
    #                     method = "POST"
    #                     url = sub['actionUrl']
    #                     jaction = CM.hit_url_method(body, headers1, method, url)
    #                     print jaction

#******  Attendance scan *******#
    # title = "test_Attendace_card"
    # if title == a['title']:
    #     print "go to next"
    #
    #     for ac in a['actions']:
    #         title = "More Actions"
    #         if title == ac['title']:
    #             print "go to next 1"
    #
    #             for sub in ac['actions']:
    #                 title = "Delete"
    #                 if title == sub['title']:
    #                     print "ready to delete"
    #                     body = {}
    #                     body['FSCardID'] = 1726
    #                     method = "POST"
    #                     url = sub['actionUrl']
    #                     jaction = CM.hit_url_method(body, headers1, method, url)
    #                     print jaction

#*****  Forum Card ********#
    # title = "test_ForumCard"
    # if title == a['title']:
    #     print "go to next"
    #
    #     for ac in a['actions']:
    #         title = "More Actions"
    #         if title == ac['title']:
    #             print "go to next 1"
    #
    #             for sub in ac['actions']:
    #                 title = "Delete"
    #                 if title == sub['title']:
    #                     print "ready to delete"
    #                     body = {}
    #                     method = "POST"
    #                     url = sub['actionUrl']
    #                     jaction = CM.hit_url_method(body, headers1, method, url)
    #                     print jaction

    #******* Baner Card ******#

    # title = "carouselcard"
    # if title == a['cardtype']:
    #     print "go to next"
    #     for sub in a['headerrow']['actions']:
    #         title = "More Actions"
    #         if title == sub['title']:
    #             print "go ahead"
    #             for sub1 in sub['actions']:
    #                 title = "Delete"
    #                 if title == sub1['title']:
    #                     print "ready to delete"
    #                     method = "POST"
    #                     url = sub1['actionUrl']
    #                     body = {}
    #                     body['CardID'] = 1729
    #                     jaction = CM.hit_url_method(body, headers1, method, url)
    #                     print jaction

    #****** Product card  *******#
    title = "carouselcard"
    if title == a['cardtype']:
        print "go to next"
        for sub in a['headerrow']['actions']:
            title = "More Actions"
            if title == sub['title']:
                print "go ahead"
                for sub1 in sub['actions']:
                    title = "Delete"
                    if title == sub1['title']:
                        print "ready to delete"
                        method = "POST"
                        url = sub1['actionUrl']
                        body = {}
                        body['CardID'] = 1727
                        jaction = CM.hit_url_method(body, headers1, method, url)
                        print jaction