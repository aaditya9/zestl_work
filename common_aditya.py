
# import json
# import base64
import time
# import datetime
from datetime import timedelta
from datetime import datetime
# import urllib2
# from urllib2 import URLError
# from urllib2 import HTTPError
import requests
# import urllib
import json
import logging
# import time
# import os

import logging
# import shelve
import re


# , 'iso-8859-1'

# global pathname
# pathname = "/var/www/cgi-bin/workflow/"
# pathname = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/6DEC_data_FG/"


# def writeshelf(k, v):
#     filename = pathname + "shelvefile"
#     # filename = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/shelvefile"
#
#     d = shelve.open(filename)  # open -- file may get suffix added by low-level
#     key = k
#     d[key] = v  # store data at key (overwrites old data if
#
#     d.close()
#
#
# def readshelf(k):
#     # filename = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/shelvefile"
#     filename = pathname + "shelvefile"
#
#     d = shelve.open(filename)  # open -- file may get suffix added by low-level
#     # library
#     key = k
#
#     if (key in d):
#         data = d[key]
#     else:
#         data = ""
#     #
#     d.close()
#     return data
#
#
# def delshelf(k):
#     filename = pathname + "shelvefile"
#
#     d = shelve.open(filename)  #
#     if (k in d):
#         del d[k]
#     d.close()

#import create_events_aditya as CA

def force_decode(string1, codecs=['utf8']):
    stringelems = list(string1)
    newstring = ""
    for char in stringelems:
        for i in codecs:
            try:
                char = char.decode(i)
                newstring = newstring + char
                # print string.encode('utf8')
            except:
                pass

    logging.warn("cannot decode %s" % ([string1]))
    return newstring


def find_strange_characters(string, count, codecs=['utf8'], ):
    for i in codecs:
        try:
            string.decode(i)
            return count, string
            string = string.decode('utf-8', 'ignore').encode("utf-8")
            # print string.encode('utf8')

        except:
            # print "i was here"
            print string
            string = string.decode('utf-8', 'ignore').encode("utf-8")
            count += 1
            return count, string

            # pass

    # logging.warn("cannot decode %s" % ([string]))



def parse_files(filename):
    count = 0
    with open("./tmp.csv", 'w') as wf:
        with open(filename, 'r') as rf:
            for line in rf:
                if isinstance(line, str):
                    count, line = find_strange_characters(line, count)
                    wf.write(line)
                    line = force_decode(line)
                # print line
                try:
                    line = unicode(line)
                except:
                    print line
                    print type(line)
                    print force_decode(line)
                    return "errors"
    return "success"

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']



def invoke_rest(request_type, rest_url, payload=None, headers=None):
    count = 1
    while True:
        try:
            api_url = rest_url
            if request_type == 'GET':
                r = requests.get(api_url, headers=headers)

                to_ret = {'code': r.status_code, 'reply': r.text}
                # logging.warning("*********************  api ********************")
                # logging.warning(to_ret)
                return to_ret
            elif request_type == 'POST':
                # logging.warning("------------------ PayLoad  ------------------")
                # start = datetime.now()
                # logging.warning("*TIME* : " + str(start) + " *Payload* : " + payload + " *API* : " + api_url)
                r = requests.post(api_url, data=payload, headers=headers)
                to_ret = {'code': r.status_code, 'reply': r.text}
                # start = datetime.now()
                # logging.warning("*Response* : "+ json.dumps(to_ret) + " *API* : " + api_url + " *TIME* : " + str(start))
                return to_ret
            elif request_type == 'PUT':
                r = requests.put(api_url, data=payload, headers=headers)
                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            else:
                return "Invalid request type ", request_type
        except Exception, e:
            print "Error in invoking " + request_type + ", " + api_url + ", Reattempting " + str(count)
            count = count + 1
            time.sleep(50.0 / 1000.0);  # Sleep 50 milli sec
            # return "Exception:", e, " in getting the API call"


def getBaseStructure(zbotID, headers1, BASE_URL):
    url = BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    method = "POST"
    response = hit_url_method(RequestBody, headers1, method, url)
    # return response
    # with open('/Users/sujoychakravarty/Dropbox/Zestl-scripts/rundir/tmp', 'w') as f:
    #     f.write(str(response))
    print response
    return json.loads(response)

def getAllUserGroups(headers, zviceID, BASE_URL,val):
    val1 = '"' + val + '"'
    # jsondata = invoke_rest('GET', BASE_URL + 'usergroups/' + zviceID + "?filter={\"limit\":10000,\"offset\":0,\"groupname\":\"COEHOD\"}" , None, headers)
    jsondata = invoke_rest('GET',BASE_URL + 'usergroups/' + zviceID + "?filter={\"limit\":10000,\"offset\":0,\"groupname\":" + val1 + "}",None, headers)
    # jsondata = invoke_rest('GET', BASE_URL + 'usergroups/' + zviceID ,None, headers)
    return jsondata['reply']


def change_view_permissions_fullurl(body, headers, BASE_URL):
    jsondata = invoke_rest('POST', BASE_URL , json.dumps(body), headers)
    return jsondata['reply']

def set_card_permissions(BASE_URL,allowedusers, cardID, zviceID, acttype, headers1):
    val = allowedusers
    usergroups = getAllUserGroups(headers1, zviceID, BASE_URL,val)
    grplist = json.loads(usergroups)['output']['usergroup']
    try:
        grpID = grplist[allowedusers]
        actionType = acttype
        RequestBody = {
                       "opType": "1",
                       "actionType": actionType,
                       "groupID": grpID,
                       "cardID": cardID,
                       "cardType": "GenericCard"
                       }
        url = BASE_URL + 'card/permissions/' + zviceID
        response = change_view_permissions_fullurl(RequestBody, headers1, url)
    except:
        response = "Could not change permision " + acttype + " : " + allowedusers
    return response


def submit_form_blank(id, zviceID, BASE_URL, headers1):
    body = {}
    url = BASE_URL + "submit_action/" + zviceID + "/form/" + str(id)
    method = "GET"
    jsonresponse = hit_url_method(body, headers1, method, url)
    for subac1 in json.loads(jsonresponse)['data']['ondemand_action']:
        data1 = json.loads(subac1['data'])
    body = data1
    method = subac1['method']
    url = subac1['actionUrl']
    jsonresponse = hit_url_method(body, headers1, method, url)
    jsonreply = json.loads(jsonresponse)
    return jsonreply['cardid']


def get_submission_id(w_ID, zviceID, BASE_URL, headers1):
    body = {}
    method = "GET"
    url = BASE_URL +  zviceID + "/forms/submissions/workflow/" + w_ID
    jsonresponse = hit_url_method(body, headers1, method, url)
    return jsonresponse

def submit_form(a, form_id, zviceID, BASE_URL, headers1):
    for row in form_id:
        id = row
        body = {}
        url = BASE_URL + "submit_action/" + zviceID + "/form/" + str(id)
        method = "GET"
        jsonresponse = hit_url_method(body, headers1, method, url)

        for subac1 in json.loads(jsonresponse)['data']['ondemand_action']:
            data1 = json.loads(subac1['data'])
            c = 0
            for element in data1['Elements'][0]['Elements']:
                # if element['ElementID'] == "Work FlowId":
                if element['ElementID'] == "WorkflowID":
      #              print "found element"
                    data1['Elements'][0]['Elements'][c]["Value"] = a
                c = c + 1
       #         print "Element position: " + str(c)
        body = data1
        method = subac1['method']
        url = subac1['actionUrl']
        jsonresponse = hit_url_method(body, headers1, method, url)

def get_form_submission(submission_id,zviceID, BASE_URL, headers1):
    body = {}
    url = BASE_URL + "submission_edit_action/" + zviceID + "/formsubmission/" + str(submission_id)
    method = "GET"
    jsonresponse = hit_url_method(body, headers1, method, url)
    return jsonresponse
    # return json.loads(jsonresponse)['data']['ondemand_action'][0]['inputs']


def edit_form_submission(submission_id,field_name,zviceID, BASE_URL, headers1, val):
    for row in field_name:
        body = {}
        url = BASE_URL + "submission_edit_action/" + zviceID + "/formsubmission/" + submission_id
        method = "GET"
        jsonresponse = hit_url_method(body, headers1, method, url)

        for subac1 in json.loads(jsonresponse)['data']['ondemand_action']:
            data1 = json.loads(subac1['data'])
            c = 0
            for element in data1['Elements'][0]['Elements']:
                if element['ElementID'] == row:
                    data1['Elements'][0]['Elements'][c]["Value"] = val
                c = c + 1
        body = data1
        method = subac1['method']
        url = subac1['actionUrl']
        jsonresponse = hit_url_method(body, headers1, method, url)
        return jsonresponse

def publish_submission(submission_id,zviceID, BASE_URL, headers1):
    url =  BASE_URL + "formsubmission/" + zviceID + "/publish/" + submission_id
    method = "POST"
    body = {}
    body['Flags'] = "true"
    jsonresponse = hit_url_method(body, headers1, method, url)
    return jsonresponse


def add_tags(CardIds,tagName,BASE_URL,zviceID,headers1):
    url = BASE_URL + zviceID + "/tags/" + zviceID
    method = 'POST'
    body = {"TaggedCardIDs": CardIds, "Tags": tagName}
    response = hit_url_method(body, headers1, method, url)
    return response

def unpaginate(inp, elements,headers1):
    for element in inp:
        if element['cardtype'] == "nextcard":
            url = element['url']
            method = element['method']
            body = json.loads(element['content'])
            jsondata = json.loads(hit_url_method(body, headers1, method, url))
            elements = unpaginate(jsondata['data']['elements'], elements, headers1)
        else:
            elements.append(element)
    return elements


def EDIT_submission_using_NEW_API(BASE_URL,zviceID,headers1,form_ID,input_data,submission_ID):
    form_ID = str(form_ID)
    submission_ID = str(submission_ID)
    body = {}
    method = "GET"
    url = BASE_URL + zviceID + "/formdetails/" + form_ID

    jasub = hit_url_method(body, headers1, method, url)
    jasub = json.loads(jasub)
    body = {}
    for a in jasub['data']['form']['Elements'][0]['Elements']:
        for k, v in input_data.items():
            if k == a['ElementID']:
                body[a['FormMetaID']] = v
    method = "PUT"
    url = BASE_URL + zviceID + "/forms/" + form_ID + "/submissions/" + submission_ID
    jsonresponse = hit_url_method(body, headers1, method, url)
    return jsonresponse



def EDIT_submission_metadata(BASE_URL,zviceID,headers1,form_ID,metadata,submission_ID):
    form_ID = str(form_ID)
    submission_ID = str(submission_ID)
    body = {}
    method = "GET"
    url = BASE_URL + zviceID + "/formdetails/" + form_ID

    jasub = hit_url_method(body, headers1, method, url)
    jasub = json.loads(jasub)
    body = {}
    body['MetaData'] = metadata
    method = "PUT"
    url = BASE_URL + zviceID + "/forms/" + form_ID + "/submissions/" + submission_ID
    jsonresponse = hit_url_method(body, headers1, method, url)
    return jsonresponse

def create_txt_card(name, icardDes, zviceID, headers1, parentCardID, BASE_URL, disallowcom, publish):
    body = {}
    url = BASE_URL + "zvice/interaction/" + zviceID
    method = "POST"
    body['Title'] = name
    if parentCardID != "":
        body['parentCardID'] = parentCardID
    body['cardData'] = {"title": name, "desc": icardDes, "Flags": publish, "DisallowCommentsInside" : disallowcom}
    body['cardType'] = "TEXT"
    body['opType'] = 1
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
    jsonreply = hit_url_method(body, headers1, method, url)
    jsonreply = json.loads(jsonreply)
    return jsonreply['cardid']

def add_tags_future(CardIds,tagName,BASE_URL,zviceID,headers1, wid):
    url = BASE_URL + zviceID + "/tags/" + zviceID
    method = 'POST'
    tagName = tagName + ",DOCSEARCH::WFID_" + str(wid)
    body = {"TaggedCardIDs": CardIds, "Tags": tagName,"WorkflowID" : int(wid)}
    response = hit_url_method(body, headers1, method, url)
    return response


def get_tags_by_cardID(cardID,BASE_URL,zviceID,headers1):  # if u pass tag name to this then this will return all the card ids to u**********#
    url = BASE_URL + "search/" + zviceID + "/tags/" + zviceID + "/cards"
    body = {"TaggedCardIDs": str(cardID)}
    method = 'POST'
    try:
        response = hit_url_method(body, headers1, method, url)
    except:
        logging.error("get tags on a card failed")
    return response


def get_all_tagIds(tagName,BASE_URL,zviceID,headers1):  # if u pass tag name to this then this will return all the card ids to u**********#
    url = BASE_URL + "search/" + zviceID + "/tags/" + zviceID + "/cards"
          # + "?filter={'limit':100, 'offset':0}"
    body = {"Tags": tagName}
    method = 'POST'
    try:
        response = hit_url_method(body, headers1, method, url)
    except:
        logging.error("get card from tag failed")
    return response

def form_submission_using_NEW_API(BASE_URL,zviceID,headers1,form_ID,input_data):
    form_ID = str(form_ID)
    body = {}
    method = "GET"
    url = BASE_URL + zviceID + "/formdetails/" + form_ID
    jasub = hit_url_method(body, headers1, method, url)
    jasub = json.loads(jasub)
    body = {}
    for a in jasub['data']['form']['Elements'][0]['Elements']:
        try:
            body[a['FormMetaID']] = a['DefaultValue']
            for k, v in input_data.items():
                if k in a['ElementID']:
                    body[a['FormMetaID']] = v
        except:
            logging.warning("Empty form submission requested for form " + form_ID)
    method = "POST"
    url = BASE_URL + zviceID + "/forms/" + form_ID + "/submissions/"
    jsonresponse = hit_url_method(body, headers1, method, url)
    jsonreply = json.loads(jsonresponse)
    return jsonreply['cardid']


def form_submission_using_NEW_API_meta(BASE_URL,zviceID,headers1,form_ID,input_data, metadata):
    form_ID = str(form_ID)
    body = {}
    method = "GET"
    url = BASE_URL + zviceID + "/formdetails/" + form_ID
    jasub = hit_url_method(body, headers1, method, url)
    jasub = json.loads(jasub)
    body = {}
    for a in jasub['data']['form']['Elements'][0]['Elements']:
        try:
            body[a['FormMetaID']] = a['DefaultValue']
            for k, v in input_data.items():
                if k in a['ElementID']:
                    body[a['FormMetaID']] = v
        except:
            logging.warning("Empty form submission requested for form " + form_ID)
    body['MetaData'] = metadata
    method = "POST"
    url = BASE_URL + zviceID + "/forms/" + form_ID + "/submissions/"
    jsonresponse = hit_url_method(body, headers1, method, url)
    jsonreply = json.loads(jsonresponse)
    return jsonreply['cardid']


def get_formID_using_KEY_Value_API(BASE_URL,headers1,zviceID,form_key):
    body = {}
    url = BASE_URL + "workflow/" + zviceID + "/" + form_key
    method = "GET"
    jasub = hit_url_method(body, headers1, method, url)
    return jasub

def set_groups(BASE_URL, body, headers, zviceID):
    return invoke_rest('POST', BASE_URL + 'usergroups/add/' + zviceID, json.dumps(body), headers)

def create_user_group(BASE_URL,headers1,grpname,zviceID):
    body = {'groupName': grpname, 'groupDesc': ""}
    result = set_groups(BASE_URL, body, headers1, zviceID)
    return result

def hide_card(headers1,BASE_URL,zviceID,c_name):
    url = BASE_URL + "zvice/interaction/" + zviceID
    method = "POST"
    body = {"interactionID": "INTERACTION_TYPE_GET_CONFIG_CARDS"}
    elements = []
    jsondata = json.loads(hit_url_method(body, headers1, method, url))
    elements = unpaginate(jsondata['data']['elements'], elements, headers1)
    for el in elements:
        if el['title'] == c_name:
            el[
                'hidden'] = True  # IF U want to hide the cards then falg is TRUE. AND if u want to show the cards then flag is FALSE
    body = {}
    body['customcards'] = elements
    body['applyforall'] = False
    method = "POST"
    url = BASE_URL + "zvice/interaction/" + zviceID
    method = "POST"
    body["interactionID"] = "INTERACTION_TYPE_SET_CONFIG_CARDS"
    body['custom_theme'] = jsondata['data']['custom_theme']
    jsondata = json.loads(hit_url_method(body, headers1, method, url))
    url = BASE_URL + "zvice/interaction/" + zviceID
    method = "POST"
    body = {"interactionID": "INTERACTION_TYPE_GET_CONFIG_CARDS"}
    jsondata = json.loads(hit_url_method(body, headers1, method, url))
    # return jsondata



def create_task_for_workflow(BASE_URL,zviceID,headers1,cardID,details, subflow,priority):
    adminGrpName = subflow + "mgr"

    try:
        admingrpID = find_out_grp_ID(adminGrpName, headers1, zviceID, BASE_URL)
    except:
        admingrpID = -1
    method = "POST"
    url = BASE_URL + "tasks/add/" + zviceID
    body = {}
    body['CardID'] = cardID
    body['Title'] = details['title']
    if admingrpID != None:
        body['UserGroupIDLevel2'] = int(admingrpID)
    # now = datetime.datetime.now()
    # startdate = datetime.datetime.utcnow()
    # sd = startdate.strftime('%Y-%m-%d %H:%M:%S')
    # body['StartDate'] = sd
    # dura = int(details['duration'])
    # duedate = datetime.datetime.utcnow() + timedelta(days=int(details['duration']))
    # dd = duedate.strftime('%Y-%m-%d %H:%M:%S')
    body['Duration'] = details['duration'].strip()
    body['Status'] = "Not Assigned"
    body['Priority'] = priority


    # body['Priority'] = "Medium"
    response = hit_url_method(body, headers1, method, url)
    response = json.loads(response)
    jresponse = {}
    if response['error']:
        jresponse['error'] = True
        jresponse['taskID'] = 0
        return jresponse
    else:
        jresponse['error'] = False
        jresponse['taskID'] = response['taskID']
        return jresponse


def add_user(BASE_URL, body, headers, zbotID, grpID):
    jsondata = invoke_rest('POST', BASE_URL + 'usergroups/' + grpID + '/user/add/' + zbotID, body, headers)

    # print "User Group API response : Code : " + str(jsondata['code'])
    # print "======================="
    # print jsondata['reply']
    # print "======================="
    return jsondata['reply']


def add_usergrps_grps(BASE_URL, body, headers, zbotID, grpID):
    jsondata = invoke_rest('POST', BASE_URL + 'usergroups/' + grpID + '/usergroup/add/' + zbotID, body, headers)
    # print "User Group API response : Code : " + str(jsondata['code'])
    # print "======================="
    # print jsondata['reply']
    # print "======================="
    return jsondata['reply']


def edit_task_for_workflow(BASE_URL,zviceID,headers1,task_Id,g_Id):
    # for k, v in details.items():
    method = "POST"
    url = BASE_URL + "tasks/edit/" + zviceID
    body = {}
    body['TaskID'] = task_Id
    body['Status'] = "Assigned"
    # for gid in v:
    # try:
    body['UserGroupIDLevel1'] = int(g_Id)
    # except:
    #     logging.warning("no group specified for task")
    # print body
    response = hit_url_method(body, headers1, method, url)
    return response
    # response = json.loads(response)
    # jresponse = {}
    # if response['error']:
    #     jresponse['error'] = True
    #     jresponse['taskID'] = 0
    #     return jresponse
    # else:
    #     jresponse['error'] = False
    #     jresponse['taskID'] = response['taskID']
    #     return jresponse

def edit_task_for_workflow_stat(BASE_URL,zviceID,headers1,task_Id,g_Id, statusd):
    # for k, v in details.items():
    method = "POST"
    url = BASE_URL + "tasks/edit/" + zviceID
    body = {}
    body['TaskID'] = task_Id
    if "Assigned" in statusd:
        body['Status'] = "Assigned"
    # for gid in v:
    # try:
    body['UserGroupIDLevel1'] = int(g_Id)
    # except:
    #     logging.warning("no group specified for task")
    # print body
    response = hit_url_method(body, headers1, method, url)
    return response
    # response = json.loads(response)
    # jresponse = {}
    # if response['error']:
    #     jresponse['error'] = True
    #     jresponse['taskID'] = 0
    #     return jresponse
    # else:
    #     jresponse['error'] = False
    #     jresponse['taskID'] = response['taskID']
    #     return jresponse


def master_logger(message):
    logging.debug(message)


def create_groups(grpname, grpdesc, headers, zviceID, BASE_URL):
    body = {'groupName': grpname,'groupDesc': grpdesc }
    try:
        method = "POST"
        url = BASE_URL + 'usergroups/add/' + zviceID
        resp = json.loads(hit_url_method(body, headers, method, url))
        resp = str(resp['output']['groupdetails']['groupid'])
        return resp

    except:
        return ""


def create_form_elements(BASE_URL,headers1,zviceID,cardID,form,form_element):
    method = "GET"
    url = BASE_URL + zviceID + "/forms/" + str(cardID)
    body = {}
    j1 = json.loads(hit_url_method(body, headers1, method, url))
    for element in j1['data']['elements']:
        if form in element['title']:
            for action in element['actions']:
                if 'More actions' in action['title']:
                    body = {}
                    url = BASE_URL + "all_actions/" + zviceID + "/form/" + str(cardID)
                    method = "GET"
                    jsonresponse = hit_url_method(body, headers1, method, url)
                    for a in json.loads(jsonresponse)['data']['ondemand_action']:
                        if "Edit" in a['title']:
                            url = a['actionUrl']
                            data = json.loads(a['data'])
                            method = a['method']
                            body = {}
                            body["FormDescription"] = data["FormDescription"]
                            body["FormID"] = data["FormID"]
                            body["FormTitle"] = data["FormTitle"]
                            body["ZviceID"] = data["ZviceID"]
                            body["ZbotID"] = data["ZbotID"]
                            body["ModifiedBy"] = data["ModifiedBy"]
                            body["DateModified"] = data["DateModified"]
                            body["CreatedBy"] = data["CreatedBy"]
                            body["DateCreated"] = data["DateCreated"]
                            body["query"] = data["query"]
                            body["Flags"] = data["Flags"]
                            zeroelem = {}

                            passthrough = True
                            if passthrough:
                                tempAr = []
                                zeroelem["ElementType"] = "SECTION"
                                zeroelem["SequenceNo"] = 1
                                zeroelem["FieldLabel"] = form
                                elarray = []
                                seqNo = 1
                                for row in form_element:
                                    elID = row['label']
                                    fldlabel = row['label']
                                    type = row['type']
                                    hint = row['placeholder']
                                    req = row['required']
                                    isEdit = row['editable']
                                    de_value = row['placeholder']

                                    if "python" in row:
                                        extra = row['python']
                                    else:extra = ""

                                    if "tagsUsed" in row:
                                        tagsused = row['tagsUsed']
                                    else:tagsused = ""

                                    # if "status_python" in row:
                                    #     status_extra = row['status_python']
                                    # else:status_extra = ""

                                    seqNo += 1
                                    addElement = {}
                                    addElement['ElementID'] = elID
                                    addElement['ElementType'] = type
                                    addElement['FieldLabel'] = fldlabel
                                    addElement['Hint'] = hint
                                    addElement['Required'] = req
                                    addElement['SequenceNo'] = seqNo
                                    addElement['MetaData'] = {"IsEditable": isEdit,"PYTHON" : extra, "tagsUsed" : tagsused}

                                    if addElement['ElementType'] == "EDIT_TEXT":
                                        addElement['DefaultValue'] = hint
                                    else:addElement['DefaultValue'] = de_value

                                    if type == "AUTO_COMPLETE":
                                        grp_ID = row['values']
                                        addElement['MetaData'] = {
                                            "PYTHON": extra,
                                            "tagsUsed": tagsused,
                                            "IsEditable": isEdit,
                                            "IsDataValid": "true",
                                            "DataSourceKey": grp_ID,
                                            "Column": "ZviceID",
                                            "Query": "null",
                                            "Url":BASE_URL + "zvice/interaction/" + zviceID,
                                            "Method": "POST",
                                            "AllowUserInput": "false",
                                            "IsAdminOnly": "false",
                                            "JsonData": {
                                              "interactionID": "CommonInteraction_INTERACTION_TYPE_SEARCH_FOR_AUTOCOMPLETE",
                                              "searchType": 5,
                                              "ExtraParams": {
                                                "GroupID": grp_ID,
                                                "CardID": cardID
                                              }
                                            },
                                            "UseThisToSendNotification": "true",
                                            "OriginalIsEditable": "true",
                                            "LazyLoad": "false",
                                            "LoadsWidgets": "false",
                                            "IsUserGroupAutoSearch": "true",
                                            "AttachUserSearch": "false",
                                            "IsDataValid": "true",
                                            "OriginalIsEditable": "true"
                                          }

                                    if type == "SPINNER" or type == "RADIO_GROUP":
                                        spinelements = row['values'].split(";")
                                        addElement['Options'] = spinelements

                                    elarray.append(dict(addElement))
                                zeroelem['Elements'] = elarray
                                tempAr.append(dict(zeroelem))
                            body['Elements'] = tempAr
                            body['DataSource'] = data['DataSource']
                            jsonresponse = hit_url_method(body, headers1, method, url)
                            return jsonresponse

def find_out_grp_ID(grp_name,headers1,zviceID,BASE_URL):
    body = {}
    url = BASE_URL + "usergroups/autosearch/" + zviceID
    method = "POST"
    body['searchQuery'] = grp_name
    response = hit_url_method(body, headers1, method, url)
    response = json.loads(response)
    grps = {}
    for ele in response['data']['elements']:
        if ele['title'] == grp_name:
            grps[ele['title']] = ele['select']
    for k, v in grps.items():
        if k == grp_name:
            return str(v)
        else:
            return ""
    # usergroups = getAllUserGroups(headers1,zviceID,BASE_URL)
    # grpvals = json.loads(usergroups)
    # grps = grpvals['output']
    # grpname = grps['usergroup']
    # dict1 = grpname
    # grpID = dict1[grp_name]
    # grpID = str(grpID)
    # return grpID

def form_card(BASE_URL,headers1,title,zviceID,p_cardID):
    r = requests.get("http://twig.me/v1/push/dectest/" + zviceID)
    tagnum = r.json()['decTagID']
    body = {"FormTitle": title, "FormDescription": "", "ZviceID": tagnum, "ZbotID": zviceID,"LinkType": "FORM", "parentCardID" : str(p_cardID)}
    method = "POST"
    url = BASE_URL+ zviceID +"/forms"
    jsondata = json.loads(hit_url_method(body, headers1, method, url))
    return jsondata['cardid']

def add_val_in_table(BASE_URL,headers1, key, value, zviceID,wfid_keyVal):
    url = BASE_URL + "workflow/" + zviceID + "/" + key + "/value/" + str(value)
    method = "POST"
    body = {}
    body['wid'] = wfid_keyVal
    response = hit_url_method(body, headers1, method, url)
    return response
    # return response

def combine_tag_gives_cardID(BASE_URL,zviceID, headers1,combine_tag):
    method = "POST"
    url = BASE_URL + "filter/" + zviceID + "/tags/" + zviceID
    body = {}
    body['Tags'] = combine_tag
    jsonresponse = hit_url_method(body, headers1, method, url)
    return jsonresponse

def add_user_InBusiness(business_id,u_name,u_email, headers1, BASE_URL):
    method = "POST"
    url = BASE_URL + 'zvice/interaction/' + business_id
    body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat', 'long': 'long', 'tagprofile': 0,
            'media_type': 'image/jpg',
            'media_ext': 'jpg', 'media': "", 'media_size': 0, 'zbotid': business_id}
    body['title'] = u_name
    body['linkemail'] = u_email
    body['autogentag'] = "true"
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"
    jsonreply = hit_url_method(body, headers1, method, url)
    return jsonreply

def add_user_to_group(g_ID,user_id,zviceID, headers1, BASE_URL):
    body = {}
    body['grpUserZviceID'] = user_id
    body['groupid'] = g_ID
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_SEARCH_FOR_AUTOCOMPLETE"
    body['searchType'] = 1
    method = "POST"
    url = BASE_URL + 'usergroups/user/add/' + zviceID
    jsonreply = hit_url_method(body, headers1, method, url)
    return jsonreply

def convertTo_Grid(BASE_URL,zviceID,headers1):
    url = BASE_URL + "zvice/interaction/" + zviceID
    method = "POST"
    body = {"interactionID": "INTERACTION_TYPE_GET_CONFIG_CARDS"}
    elements = []
    jsondata = json.loads(hit_url_method(body, headers1, method, url))
    elements = unpaginate(jsondata['data']['elements'], elements, headers1)
    body = {}
    theme = jsondata['data']['custom_theme']
    theme['view_type'] = "GRID"
    theme['number_of_columns'] = 3
    body['customcards'] = elements
    body['applyforall'] = False
    url = BASE_URL + "zvice/interaction/" + zviceID
    method = "POST"
    body["interactionID"] = "INTERACTION_TYPE_SET_CONFIG_CARDS"
    body['custom_theme'] = jsondata['data']['custom_theme']
    jsondata = json.loads(hit_url_method(body, headers1, method, url))


def attachment_API(BASE_URL,zviceID,headers1,sub_ID,m_url,m_name,m_size):
    body = {}
    method = "POST"
    url = BASE_URL + "cards/" + str(sub_ID) + "/attachment/s3/" + zviceID
    body['S3URL'] = m_url
    body['fileName'] = m_name
    body['fileSize'] = m_size
    jasub = hit_url_method(body, headers1, method, url)
    return jasub

def create_FORUM_card(forum_name,zviceID,BASE_URL,headers1,p_CardId):
    body = {}
    body['parentCardID'] = p_CardId
    body['Text'] = forum_name
    body['Flags'] = "true"
    body['FlagsInside'] = "true"
    method = "POST"
    url = BASE_URL + "forum/" + zviceID
    jaction = hit_url_method(body, headers1, method, url)
    resutl = json.loads(jaction)
    f_id = resutl['cardid']
    return f_id

def EDIT_submission_using_NEW_API_using_ChangeIn_URL(BASE_URL,zviceID,headers1,form_ID,input_data,submission_ID):
    form_ID = str(form_ID)
    submission_ID = str(submission_ID)
    body = {}
    method = "GET"
    fieldsmeta = json.dumps({"HideEditAction": False, "IsFormLinked": "true"})
    url = BASE_URL + zviceID + "/formdetails/" + form_ID

    jasub = hit_url_method(body, headers1, method, url)
    jasub = json.loads(jasub)
    body = {}
    for a in jasub['data']['form']['Elements'][0]['Elements']:
        for k, v in input_data.items():
            if k == a['ElementID']:
                body[a['FormMetaID']] = v
    body['MetaData'] = fieldsmeta
    method = "PUT"
    url = BASE_URL + zviceID + "/forms/" + form_ID + "/submissions/" + submission_ID + "?donotcall=t"
    jsonresponse = hit_url_method(body, headers1, method, url)
    return jsonresponse

def edit_form_spinner_element(BASE_URL,zviceID,headers1,jsonresponse,f_title,brand_name):
    for sub in json.loads(jsonresponse)['data']['ondemand_action']:
        if "Edit" in sub['title']:
            url = sub['actionUrl']
            data1 = json.loads(sub['data'])
            method = sub['method']
            body1 = {}
            body1["FormDescription"] = data1["FormDescription"]
            body1["FormID"] = data1["FormID"]
            body1["FormTitle"] = data1["FormTitle"]
            body1["ZviceID"] = data1["ZviceID"]
            body1["ZbotID"] = data1["ZbotID"]
            body1["ModifiedBy"] = data1["ModifiedBy"]
            body1["DateModified"] = data1["DateModified"]
            body1["CreatedBy"] = data1["CreatedBy"]
            body1["DateCreated"] = data1["DateCreated"]
            body1["query"] = data1["query"]
            body1["Flags"] = data1["Flags"]
            title = data1["FormTitle"]
            zeroelem = {}
            val = data1['Elements'][0]['Elements']  # This line is for taking existing elements from FORM #
            for elm in val:
                if f_title in elm['ElementID']:
                    spiner = elm['Options']
                    spinner_elements = brand_name
                    spiner.append(spinner_elements)
                    elm['Options'] = spiner
            passthrough = True
            if passthrough:
                tempAr = []
                zeroelem["ElementType"] = "SECTION"
                zeroelem["SequenceNo"] = 1
                zeroelem["FieldLabel"] = title
                zeroelem['Elements'] = val
                tempAr.append(dict(zeroelem))
            body1['Elements'] = tempAr
            body1['DataSource'] = data1['DataSource']
            jsonresponse = hit_url_method(body1, headers1, method, url)
            return jsonresponse


def get_all_tasks_on_cardID(BASE_URL,zviceID,headers1,cardID):
    method = "GET"
    body1 = {}
    url = BASE_URL + "tasks/" + zviceID + "/" + str(cardID)
    jsonresponse = hit_url_method(body1, headers1, method, url)
    return jsonresponse


def edit_task_forOnlyFor_changeStatus(BASE_URL,zviceID,headers1,task_Id,task_status):
    method = "POST"
    url = BASE_URL + "tasks/edit/" + zviceID
    body1 = {}
    body1['TaskID'] = task_Id
    body1['Status'] = task_status
    response = hit_url_method(body1, headers1, method, url)
    return response

def tags_give_base_cardInfo(BASE_URL,c_name,headers1):
    url = BASE_URL + "zvice/basecard/"  # Base card
    method = "POST"
    b = {}
    b['tagIds'] = [c_name]
    jasub = hit_url_method(b, headers1, method, url)
    return jasub

def search_form_submission(BASE_URL,headers1,zviceID,form_ID,field_key,f_value):
    method = "POST"
    url = BASE_URL + "search/" + zviceID + "/forms/" + form_ID + "/submissions"
    b = [{"FieldLabel": field_key, "Value": f_value}]
    jsonresponse = hit_url_method(b, headers1, method, url)
    return jsonresponse

def form_submission_using_NEW_API_genepath(BASE_URL,zviceID,headers1,form_ID,input_data):
    form_ID = str(form_ID)
    body = {}
    method = "GET"
    url = BASE_URL + zviceID + "/formdetails/" + form_ID
    # jasub = hit_url_method(body, headers1, method, url)
    jasub = hit_url_method(body, headers1, method, url)
    jasub = json.loads(jasub)
    body = {}
    for a in jasub['data']['form']['Elements'][0]['Elements']:
        try:
            body[a['FormMetaID']] = a['DefaultValue']
            for k, v in input_data.items():
                if k == a['ElementID']:
                    body[a['FormMetaID']] = v
        except:
            logging.warning("Empty form submission requested for form " + form_ID)
    method = "POST"
    url = BASE_URL + zviceID + "/forms/" + form_ID + "/submissions/"
    jsonresponse = hit_url_method(body, headers1, method, url)
    jsonreply = json.loads(jsonresponse)
    return jsonreply['cardid']


def textCard_metadata(cardID,metaDATA,BASE_URL,zviceID,headers1):
    method = "PUT"
    url = BASE_URL + "org/" + zviceID + "/workflow/cardmetadata/" + str(cardID)
    b = {}
    b['WFMetaData'] = metaDATA
    jsonresponse = hit_url_method(b, headers1, method, url)
    return jsonresponse

def get_textcard_metadata(cardID,BASE_URL,zviceID,headers1):
    method = "GET"
    b = {}
    url = BASE_URL + "org/" + zviceID + "/workflow/cardmetadata/" + cardID
    jsonresponse = hit_url_method(b, headers1, method, url)
    return jsonresponse


def create_workFlow_ID(zviceID, BASE_URL, headers1):
    method = "POST"
    b = {}
    b['title'] = "workflow"
    b['workflowtypeid'] = 1
    url = BASE_URL + "workflow/" + zviceID
    jsonresponse = hit_url_method(b, headers1, method, url)
    return jsonresponse


def EDIT_submission_using_NEW_API_with_metadata(BASE_URL,zviceID,headers1,form_ID,input_data,submission_ID,fieldsmeta):
    form_ID = str(form_ID)
    submission_ID = str(submission_ID)
    body = {}
    method = "GET"
    url = BASE_URL + zviceID + "/formdetails/" + form_ID

    jasub = hit_url_method(body, headers1, method, url)
    jasub = json.loads(jasub)
    body = {}
    for a in jasub['data']['form']['Elements'][0]['Elements']:
        for k, v in input_data.items():
            if k == a['ElementID']:
                body[a['FormMetaID']] = v
    body['MetaData'] = fieldsmeta
    method = "PUT"
    url = BASE_URL + zviceID + "/forms/" + form_ID + "/submissions/" + submission_ID
    jsonresponse = hit_url_method(body, headers1, method, url)
    return jsonresponse


def findtagid(p_id,ZbotID,url,headers1):   #New api for finding usertagid
    body={}
    method="GET"
    b_url=url+ "org/" + ZbotID + "/user/search/moredetails?filter={\"md_header\":\"PID\",\"search\":" + "\"" + p_id + "\"" + "}"
    result =hit_url_method(body, headers1, method, b_url)
    rr = json.loads(result)
    user_array = rr["data"]["users"]
    return user_array
    # print(user_array)
    # if len(user_array)!=0:
    #     user_tagid = user_array[0]
    #     return  user_tagid# calling update func for update user info
    # else:
    #     print ('USERID are not present so Creating new user \n')
    #     return CA.create_user(p_id)

def patientinfo(calendarID,businessID,zviceID,headers1,EventID,url): #New api for fill pateint information
    body = {}
    body['ChildTagID']=zviceID
    body['EventID']=EventID
    method = "POST"
    b_url=url + businessID +"/calendars/"+str(calendarID)+'/events/'+str(EventID)+'/attendees'
    jsonresponse = hit_url_method(body, headers1, method, b_url)
    return  jsonresponse


def add_contactdetails(zviceID,BASE_URL,headers1,mobile): #New api for fill contact details
    method = "POST"
    body = {}
    # address = row[addressCol].strip( url = BASE_URL + 'zvice/interaction/' + zviceID)
    body['Contact'] = mobile
    body["interactionID"] = "CommonInteraction_INTERACTION_TYPE_MODIFY_CONTACT_INFO"
    url = BASE_URL + 'zvice/interaction/' + zviceID
    jsonreply = hit_url_method(body, headers1, method, url)
    print('Contact Details get added\n')
    print jsonreply

def add_moredetails(zviceID,BASE_URL,notename,note,headers1): #New api for fill more details
        method = "PUT"
        url = BASE_URL + 'ztag/notes_PP/' + zviceID
        tagNote = {"NoteHeader": notename, "Note": note};
        body = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes',
                'tagnotes': json.dumps(tagNote)}
        jsonreply = hit_url_method(body, headers1, method, url)
        print jsonreply
        print('More Details get added\n')

def get_user_tagid(BASE_URL,headers1,zbotID,doctor):
    actionUrl = BASE_URL + "zvice/interaction/" + zbotID
    method = "POST"
    responseBody = {'username': '', 'expired': 'false',
                    'interactionID': 'CommonInteraction_INTERACTION_TYPE_SEARCH_LIB_USER_PROFILE', "pagesize": 5000}

    jsondata = hit_url_method(responseBody, headers1,method,actionUrl)
    for a in json.loads(jsondata)['data']['elements']:
        if doctor == a['title']:
            tagid = a['tagId']
            return tagid
        else:
            tagid=''
    return tagid


def linktwigmeuser(BASE_URL,UserID,headers1): #New api for link twigmeuser
    body = {}
    url = BASE_URL + UserID + '/linktotwigmeuser'
    method = "GET"

    jsonreply = hit_url_method(body, headers1, method, url)
    return jsonreply

def linkemail(BASE_URL,zviceID,emailID,headers1): #New api for link emailID to user
    method = "POST"
    url=BASE_URL+ 'zvice/interaction/' + zviceID
    body = {"interactionID": "CommonInteraction_INTERACTION_TYPE_LINK_USERPROFILE", "linkemail": emailID}
    jsonresponse1 = hit_url_method(body, headers1, method, url)
    return jsonresponse1



def delete_event(BASE_URL,bId,calendarID,event_id,headers1):
    calendarID=str(calendarID)
    event_id=str(event_id)
    url=BASE_URL + "delete/" + bId + "/calendars/" + calendarID + "/events/" + event_id
    method = "POST"
    body = {}
    body['categorytype'] = "CalendarEvent"
    jsonresponse = hit_url_method(body, headers1, method, url)
    return jsonresponse