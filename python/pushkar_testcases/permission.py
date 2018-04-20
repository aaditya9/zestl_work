import logon as LL
import common as CM
import info as info
import json

BASE_URL = info.url
email = info.email
pwd = info.pwd
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

def getAllUserGroups(headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('GET', BASE_URL + 'usergroups/' + zbotID + "?filter={\"limit\":1000,\"offset\":0}", None, headers)
    return jsondata['reply']

def set_card_permissions(grpName, cardID, acttype, ZbotID):
    BASE_URL = info.url
    usergroups = getAllUserGroups(headers1, ZbotID, BASE_URL)
    print usergroups
    grplist = json.loads(usergroups)['output']['usergroup']
    grpID = grplist[grpName]
    print grpID
    body = {}
    body['opType'] = "1"
    body['actionType'] = acttype
    body['groupID'] = grpID
    body['cardID'] = cardID
    body['cardType'] = "GenericCard"
    url = BASE_URL + 'card/permissions/' + ZbotID
    method = "POST"
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def auto_Notification(cardID,bId):
    body = {'cardType': 'GenericCard', 'cardID': cardID, 'policyType': 'AUTO_UPDATE_CARD_MAIL', 'policyVal': "true"}
    method = "POST"
    url = BASE_URL + 'cards/policy/' + bId
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def Mail_Notification_comm_pref(cardID, bId):
    body = {'cardType': 'GenericCard', 'cardID': cardID, 'actionType': 'MAIL', 'sendMail': "true",'sendNotification': "true"}
    method = "PUT"
    url = BASE_URL + "cards/permsissions/extraperm/" + bId
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

        # def View_Permission(bId,Group_ID,type):
#     body = {}
#     body['groupID'] = Group_ID
#     body['cardType'] = ""
#     body['cardID'] = ""
#     body['actionType'] = type
#     body['copyToCommPrefMail'] = True
#     body['copyToCommPrefSMS']= True
#     url = BASE_URL + "card/permissions/" + bId
#     method = "POST"
#     if type == "VIEW":
#         body['opType'] = 5  # ***** VIEW ******#
#         jaction = CM.hit_url_method(body, headers1, method, url)
#         return jaction
#     else:
#         body['opType'] = 1  # ***** ADMIN ******#
#         jaction = CM.hit_url_method(body, headers1, method, url)
#         return jaction