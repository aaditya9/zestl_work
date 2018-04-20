
import logon as LL
import common as CM
import json
import common as CM

SERVER = "http://twig-me.com/" #Production
version = "v13/"
BASE_URL = SERVER + version
zviceID = "83H6LVUBRXWZ5"
email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

# def getAllUserGroups(headers, zbotID):
#     jsondata = LL.invoke_rest('GET', BASE_URL + 'usergroups/' + zbotID + "?filter={\"limit\":1000,\"offset\":0}",
#                               None, headers)
#     return jsondata['reply']
#
# result = getAllUserGroups(headers,"WHGJ7HTVTDFH3")
# print result
def add_tags(CardIds,tagName,BASE_URL,zviceID,headers1):
    url = BASE_URL + zviceID + "/tags/" + zviceID
    method = 'POST'
    body = {"TaggedCardIDs": CardIds, "Tags": tagName}
    response = LL.hit_url_method(body, headers1, method, url)
    return response

def get_all_tagIds(tagName,BASE_URL,zviceID,headers1):
    url = BASE_URL + "search/" + zviceID + "/tags/" + zviceID + "/cards"
    body = {"Tags": tagName}
    method = 'POST'
    response = LL.hit_url_method(body, headers1, method, url)
    return response

# CardIds = "4"
# tagName = "MInalGrp"
# result = add_tags(CardIds, tagName, BASE_URL, "WHGJ7HTVTDFH3", headers1)
# print result


# tagName = "MInalGrp"
# result = get_all_tagIds(tagName,BASE_URL,"WHGJ7HTVTDFH3",headers1)
# print result

body = {}
method = "GET"
url = BASE_URL + zviceID + "/formdetails/" + str(44)
# url = "http://www.twig-me.com/v13/submission_edit_action/83H6LVUBRXWZ5/formsubmission/68"
jasub = CM.hit_url_method(body, headers1, method, url)
print jasub
jasub = json.loads(jasub)
#
# element = {}
# body = {}
input_data = {"Not Applicable" : "false","SKIP" : "false"}
#
# def hide_card(headers1,BASE_URL,zviceID,c_name):
#     url = BASE_URL + "zvice/interaction/" + zviceID
#     method = "POST"
#     body = {"interactionID": "INTERACTION_TYPE_GET_CONFIG_CARDS"}
#     elements = []
#     jsondata = json.loads(hit_url_method(body, headers1, method, url))
#     elements = unpaginate(jsondata['data']['elements'], elements, headers1)
#     for el in elements:
#         if el['title'] == c_name:
#             el[
#                 'hidden'] = True  # IF U want to hide the cards then falg is TRUE. AND if u want to show the cards then flag is FALSE
#     body = {}
#     body['customcards'] = elements
#     body['applyforall'] = False
#     method = "POST"
#     url = BASE_URL + "zvice/interaction/" + zviceID
#     method = "POST"
#     body["interactionID"] = "INTERACTION_TYPE_SET_CONFIG_CARDS"
#     body['custom_theme'] = jsondata['data']['custom_theme']
#     jsondata = json.loads(hit_url_method(body, headers1, method, url))
#     url = BASE_URL + "zvice/interaction/" + zviceID
#     method = "POST"
#     body = {"interactionID": "INTERACTION_TYPE_GET_CONFIG_CARDS"}
#     jsondata = json.loads(hit_url_method(body, headers1, method, url))
#     # return jsondata
# CM.hide_card(headers1, BASE_URL, body['BusinessTag'], str(body['WorkflowID']))


for a in jasub['data']['form']['Elements'][0]['Elements']:
    print a['ElementID']
    print a['FormMetaID']
    print a['Value']

    # element[a['ElementID']] = a['FormMetaID']
    for k,v in input_data.items():
        if k == a['ElementID']:
            # if a['Value'] == None:
            body[a['FormMetaID']] = v
            # else:body[a['FormMetaID']] = a['Value']
print body
# method = "POST"
method = "PUT"
# url = "http://www.twig-me.com/v13/83H6LVUBRXWZ5/forms/1/submissions/"
url = "http://www.twig-me.com/v13/83H6LVUBRXWZ5/forms/44/submissions/68"
jsonresponse = CM.hit_url_method(body, headers1, method, url)
print jsonresponse


# def form_submission_using_NEW_API(BASE_URL,zviceID,form_ID,input_data):
#     form_ID = str(form_ID)
#     body = {}
#     method = "GET"
#     url = BASE_URL + zviceID + "/formdetails/" + form_ID
#     jasub = CM.hit_url_method(body, headers1, method, url)
#     jasub = json.loads(jasub)
#
#     body = {}
#     for a in jasub['data']['form']['Elements'][0]['Elements']:
#         for k, v in input_data.items():
#             if k == a['ElementID']:
#                 body[a['FormMetaID']] = v
#     print body
#     method = "POST"
#     url = BASE_URL + zviceID + "/forms/" + form_ID + "/submissions/"
#     jsonresponse = CM.hit_url_method(body, headers1, method, url)





# ********************* Code for Editing the task  ********************************#

# if body['Cmd'] == "form-submit":
#     # inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
#
#     # if body['Cmd'] == "workflow-create":
#     # *************  Commeting  ********
#     tagName = "MKT_CONFIG:WFID_210"
#     # result = CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1)
#     result = json.loads(CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1))
#
#     for alltag in result['data']['elements']:
#
#         if "Task Assignment Form" in alltag['allTags']:
#             print "present"
#             data = json.loads(alltag['content'])
#             elem = {}
#             for subelm in data['Elements'][0]['Elements']:
#                 try:
#                     g_ID = subelm['Value']
#                     g_ID = json.loads(g_ID)
#                     g_ID = g_ID['GroupIDs']
#                     c_id = subelm['MetaData']['PYTHON']
#                     elem[c_id] = g_ID
#                 except:
#                     print "ha ha ha"
#             # print elem
#             result = CM.edit_task_for_workflow(BASE_URL, body['BusinessTag'], headers1, elem)
#             # print result
#             print "------"



#*************************************************************************************************************#