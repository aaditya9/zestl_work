
import json
import lib.login1 as LL


def getBaseStructure(zbotID, headers1):
    url = LL.BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    response = hit_url(RequestBody, headers1, zbotID, url)
    with open('C:/Users/Minal Thorat/Dropbox/Zestl-scripts/rundir/tmp', 'w') as f:
        f.write(str(response))
    return json.loads(response)

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


headers, headers1 = LL.req_headers()

# zviceID = "9YZ2HAZE4B5TN" ###gold gym try member user
# zviceID = "84YRY2BW2RU4K" ## goldgym try Trainer user
# zviceID = "4CFE6HD5RTTHZ"# minal test user
# zviceID = "B4XUSCNRDDNEP"
# zviceID = "876MD568TAUH2"   #MInal Test Business ID
# zviceID = "XBEER2UPJ4KN2"   #BangloreIndus
# zviceID = "CTYXZYKL7DPT4" ## minal Library test
# zviceID = "55H8PHL5TERCE" ##prod user sayali
# zviceID = "DU8BFMK4WUBZF" ## minal prod user
# zviceID = "8SFKZCV5PFAXV"  ## minal prod business
zviceID = "83H6LVUBRXWZ5"   # dev minal business
# zviceID = "WHGJ7HTVTDFH3"
# zviceID = "87ZWFB9AKKCK8"   # humpy a2
# zviceID = "9J5EDAR3Y2PZA"   #millennium
# zviceID = "WHGJ7HTVTDFH3"
# zviceID = "8SFKZCV5PFAXV"
# zviceID = "AQSYFC5AQY7X8"   # future retailer

jsondata = getBaseStructure(zviceID, headers1)
# print jsondata
tagids = []
for element in jsondata['data']['elements']:
    if element['cardtype'] == "basecard" and element['tagId'] != zviceID:
        tagids.append(element['tagId'])
    # print element['title'] + " : " + element['backgroundImageUrl']
print tagids

# url = "http://35.154.64.11/v7/genericcardsf/" + zviceID  ### test********************

# url = "https://twig.me/v8/genericcards/" + zviceID  ### mai level..prod
# url = "https://twig.me/v8/all_actions/8SFKZCV5PFAXV/form/254"
# url = "https://twig.me/v8/permission_action/8SFKZCV5PFAXV/permission/254"
# url = "https://twig.me/v8/card/get/permissions/8SFKZCV5PFAXV"
# url = "https://twig.me/v8/all_actions/8SFKZCV5PFAXV/attendance/323"
# url = "https://twig.me/v8/zvice/interaction/DU8BFMK4WUBZF"
url = "http://twig-me.com/v13/genericcards/" + zviceID   # DEV server
# url = "http://13.126.76.186/v13/genericcards/" + zviceID    # future group
# url = "http://35.154.64.119/v13/genericcards/" + zviceID
# url = "http://www.twig-me.com/v13/genericcards/WHGJ7HTVTDFH3"
# url = "http://www.twig-me.com/v13/genericcards/WHGJ7HTVTDFH3"
# url =  "http://www.twig-me.com/v13/all_actions/83H6LVUBRXWZ5/form/44"
# url = 'http://www.twig-me.com/v13/WHGJ7HTVTDFH3/calendars/720/eventslist?first_click=1&filter={"list":"upcoming_events","limit":10,"offset":0}'
# url = "http://www.twig-me.com/v13/usergroups/4/WHGJ7HTVTDFH3"
# url = "http://www.twig-me.com/v13/submission_edit_action/83H6LVUBRXWZ5/formsubmission/68"
# url = "https://twig.me/v8/genericcards/B4XUSCNRDDNEP"
# url = "https://twig.me/v8/genericcards/9J5EDAR3Y2PZA"
# url = "http://www.twig-me.com/v13/genericcards/83H6LVUBRXWZ5"
# url = "http://www.twig-me.com/v13/all_actions/83H6LVUBRXWZ5/form/265"
# url = "https://twig.me/v8/all_actions/8SFKZCV5PFAXV/textcard/444"
# url = "https://twig.me/v8/add_card_action/8SFKZCV5PFAXV/textcard/444"
# url = "https://twig.me/v8/add_card_action/8SFKZCV5PFAXV/textcard/444"

# url = "http://35.154.177.221/v8/genericcards/" + zviceID

# body = {"pageNum":2}

# body = {"cardType":"GenericCard","cardID":"225","actionType":"MAIL"}



# body = {"parentCardID": "262"} ####  this will give you particular card json data  ( only put one body at a time )

body = {} #######3  whole jason
# body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_CONTACT_DETAILS"}
# body = {"parentCardID":19721}
# body = {"cardType":"ORG_BASE_CARD"}
# body = {"cardType":"","cardID":"","actionType":"VIEW"}
# body = {"cardType":"","cardID":"","actionType":"MAIL"}
# body = {"cardType":"GenericCard","cardID":"254","actionType":"ALLOWED_USERS"}

# body = {"interactionID" : "CommonInteraction_INTERACTION_TYPE_EDIT_FORM", "categorytype" :"FormCard"}
# body['interactionID'] = "INTERACTION_TYPE_GET_CONFIG_CARDS"
# url = "http://35.154.64.11/v5/876MD568TAUH2/forms/1718/submissions/"
method = "POST"
# method = "GET"
# body['data'] = {"nameto" : "Minal T", "emailto":"minal@zestl.com", "userid":"3163"}
# body['cardtype'] = "mastercard"
# body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_SHOW_GENERIC_NOTES"
# body['notetype'] = "P"
# body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_GENERIC_NOTES","notetype":"P","useclubbing":"false" }

# body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_CONTACT_DETAILS", "genericCardType":"ContactCard"}  ## used for Contac card..... if i want to edit contact details

# http://35.154.64.11/v5/genericcards/876MD568TAUH2"

jsonresponse = hit_url_method(body, headers1, method, url)
print jsonresponse
print "++++++++ ------------- +++++++++++"

# print jsonresponse
## what are you trying to do.
## my form inside text card. so i want go inside text
 # and just fyi - you are immediately overwriting the value of body on the v nex line

# url = "https://twig.me/v1/zvice/interaction/ACTY37DGEBN6C"
# body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_GENERIC_NOTES","notetype":"P","useclubbing":False}
# method = "POST"
# # url = "https://twig.me/v1/permissions/communication/CYE5WLGBESTAT"
# # url = "https://twig.me/v1/zvice/interaction/CYE5WLGBESTAT"
# #
# # body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_GET_CARDS_PERMISSIONS_USR_GRPS","cardType":"GenericCard","cardID":"180","actionType":"MAIL"}
# #
# url = "https://twig.me/v1/zvice/interaction/ACTY37DGEBN6C"
# body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_GENERIC_NOTES","notetype":"P","useclubbing":False}
# method = "POST"
# url = "https://twig.me/v1/genericcards/CW7ZBJ8C3H9DL"
# body = {"parentCardID":79}
# body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_CALENDAR_EVENTS","CalendarID":107,"ZviceID":3000004598,"DefaultView":"Month","categoryType":"CalendarCard"}
# method = "POST"
# url = "https://twig.me/v3/CW7ZBJ8C3H9DL/calendars/107/events"


# url = "https://twig.me/v1/permissions/communication/CYE5WLGBESTAT"
# url = "https://twig.me/v1/zvice/interaction/CYE5WLGBESTAT"

#
#
# jsonresponse = hit_url_method(body, headers1, method, url)
# print "++++++++ ------------- +++++++++++"
#
# print jsonresponse
#
# print "++++++++ ------------- +++++++++++"
# print "++++++++ ------------- +++++++++++"
# print "++++++++ ------------- +++++++++++"
# print "++++++++ ------------- +++++++++++"
#
# jsondata = json.loads(jsonresponse)
# for element in jsondata['data']['elements']:
#     for action in element['actions']:
#         if 'Delete' in action['title']:
#             print action['inputs'][1]['properties'][1]['value']
#
# BASE_URL = LL.BASE_URL
#
# #
# # print "+++++++++++++++++++++++++++++++++++"
# #
# # url =  "https://twig.me/v1/usergroups/3/9J5EDAR3Y2PZA"
# # method = "GET"
# # body = {}
# # jsondata = hit_url_method(body, headers1, method, url)
# # with open('/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/rundir/tmpgrps', 'w') as wf:
# #     wf.write(str(jsondata))
# # jsondata = json.loads(jsondata)
# # jsondata = jsondata['data']['elements']
# # for element in jsondata:
# #     if "basecard" in element['cardtype']:
# #         zviceID = element['tagId']
# #         url = "https://twig.me/v1/usergroups/3/user/" + zviceID + "/delete/9J5EDAR3Y2PZA"
# #         method = "POST"
# #         print "===deleting user " + element['title']
# #         jsondata = hit_url_method(body, headers1, method, url)
# #         print jsondata
# # print jsondata
#
# # url = "https://twig.me/v1/usergroups/3/user/9FBFN2U24YE4M/delete/9J5EDAR3Y2PZA"
# # method = "POST"
# # jsondata = hit_url_method(body, headers1, method, url)
# # print jsondata
#
