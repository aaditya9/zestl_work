# -*- coding : utf-8 -*--
# -*- coding: utf-8 -*--
import json
import csv
import logon as LL
import common as CM
import re
import requests


def createForm(zviceID, tagID, title, desc, parentCardID):

    r = requests.get("http://twig.me/v1/push/dectest/" + zviceID)
    tagnum = r.json()['decTagID']

    ########## create a form
    # tagID = "BJ66CWKHL4JF5"
    r = requests.get("http://twig.me/v1/push/dectest/" + tagID)
    zviceNum = r.json()['decTagID']

    url = BASE_URL + tagID + "/forms"
    method = "POST"
    if parentCardID == None:
        body = {"FormTitle": title, "FormDescription": desc, "ZviceID": zviceNum, "ZbotID": tagnum, "LinkType": "FORM"}
    else:
        body = {"FormTitle": title, "FormDescription": desc, "ZviceID": zviceNum, "ZbotID": tagnum, "LinkType": "FORM", "parentCardID" : parentCardID}
    jsonresponse = CM.hit_url_method(body, headers1, method, url)

    # print jsonresponse

    print unhide_card(tagID, title, BASE_URL, headers1)
    return jsonresponse

def unhide_card(tagID, title, BASE_URL, headers1):
    body = {"interactionID": "INTERACTION_TYPE_GET_CONFIG_CARDS"}
    method = "POST"
    urlAdd = "zvice/interaction/" + tagID
    url = BASE_URL + urlAdd

    jsondata = CM.hit_url_method(body, headers1, method, url)

    jsondata = json.loads(jsondata)
    # print jsondata['data']

    for element in jsondata['data']['elements']:
        if title in element['title']:
            # jsondata['data']['elements'].remove(element)
            element['hidden'] = False

    body = {}
    body['interactionID'] = "INTERACTION_TYPE_SET_CONFIG_CARDS"
    body['applyforall'] = False
    body['customcards'] = jsondata['data']['elements']
    method = jsondata['homemethod']
    urlAdd = "zvice/interaction/" + tagID
    url = BASE_URL + urlAdd
    # url = BASE_URL + urlAdd

    jsondata = CM.hit_url_method(body, headers1, method, url)


    return jsondata
    # print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"


SERVER = "https://twig.me/"
version = "v4/"
BASE_URL = SERVER + version

# zviceID = "AZ7RZ78HRVCM3"
zbotID = "D94R5WDH393N4"

email = "admin@zestl.com"
pwd = "Zspladmin99"


headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

isbn = "9780141334998"
url =   BASE_URL + "book/isbn/" + isbn
body = {}
response = CM.hit_url_method(body, headers1, "GET", url)
print response
data = {}
try:
    res = json.loads(response)
    data = json.loads(res['data'])
except:
    print "no isbn data returned"
body = {}
try:
    body['title'] = data['title']
except KeyError:
    title = "Panipat cha Vijay पानिपत चा विजय"
    title = "Manahpurvak Khushwant (Ã Â¤Â®Ã Â¤Â¨:Ã Â¤ÂªÃ Â¥â€šÃ Â¤Â°Ã Â¥ÂÃ Â¤ÂµÃ Â¤â€¢ Ã Â¤â€“Ã Â¥ÂÃ Â¤Â¶Ã Â¤ÂµÃ Â¤â€šÃ Â¤Â¤)"
    # title = title.decode(encoding = 'UTF-8')
    # title = title.encode(encoding='UTF-8', errors='ignore')
    body['title'] = title
try:
    body['zviceinfo'] = data['description']
except KeyError:
    body['zviceinfo'] = ""
try:
    body['Author'] = data['author']
except KeyError:
    body['Author'] = ""
try:
    body['Book pages'] = data['pages']
except KeyError:
    body['Book pages'] = ""
try:
    body['isbn'] = data['isbn']
except KeyError:
    body['isbn'] = ""
try:
    body['Mrp '] = data['mrp']
except KeyError:
    body['Mrp '] = ""

try:
    body['Publisher'] = data['publisher']
except KeyError:
    body['Publisher'] = ""

try:
    body['Publisher'] = data['publisher']
except KeyError:
    body['Publisher'] = ""
body['zvicetype'] = "ZTAG"
body['lat'] = "---"
body['long'] = "---"
body['zviceloc'] = "---"
body['tagprofile'] = 2
body['zvicelink'] = "NEW"
body['zbotid'] = "D94R5WDH393N4"

body['zviceid'] = "7NZ3VPM93THKX"


url = BASE_URL + "zvice/register"
method = "PUT"

response = CM.hit_url_method(body, headers1, method, url)
print response
print "============"
# jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
# tagids = []
# for element in jsondata['data']['elements']:
#     if element['cardtype'] == "basecard" and element['tagId'] != zviceID and element['tagId'] != "EF9PHJBFDZ2GA":
#         tagids.append(element['tagId'])
#     # print element['title'] + " : " + element['backgroundImageUrl']
# print tagids

formElementFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/KPCA_Current_task_status_form.csv"
title = "Current Task Status"
desc = "Click new to submit"
hasHeader1 = "Y"

# tagids = [ "WHJQ7E4X68VBZ"]

tagids = [ "AZ7RZ78HRVCM3"]

for tag in tagids:
    print tag
    jsondata = CM.getBaseStructure(tag, headers1, BASE_URL)
    for card in jsondata['data']['elements']:
        if "Task" in card['title']:
            parentCardID = json.loads(card['ctjsondata'])['parentCardID']
            url = card['cturl']
            body = json.loads(card['ctjsondata'])
            method = "POST"
            jcards = CM.hit_url_method(body, headers1, method, url)
            print "^^^^^^^^^^^^^^^^^^"
            print jcards


            for element in json.loads(jcards)['data']['elements']:
                if title  in element['title']:
                    print element['title']

                    print title + " found"
                    print "============================"
                    for action in element['actions']:
                        print action
                        if 'More Actions' in action['title']:
                            for a in action['actions']:
                                if "Edit" in a['title']:
                                    url = a['actionUrl']
                                    data = json.loads(a['data'])
                                    method = a['method']
                                    print " &&&&&&&&&&&&&&&&&&&&&&& "
                                    body = {}

                                    body["FormDescription"] = data["FormDescription"]
                                    body["FormID"] = data["FormID"]

                                    body["FormTitle"] = data["FormTitle"]
                                    # body["ZviceID"]=  "CVEPKDHYA2FCS"
                                    body["ZviceID"] = data["ZviceID"]
                                    body["ZbotID"] = data["ZbotID"]
                                    body["ModifiedBy"] = data["ModifiedBy"]
                                    body["DateModified"] = data["DateModified"]
                                    body["CreatedBy"] = data["CreatedBy"]
                                    body["DateCreated"] = data["DateCreated"]
                                    body["query"] = data["query"]
                                    body["Flags"] = data["Flags"]
                                    zeroelem = {}
                                    print data['Elements']
                                    if data['Elements'] == None:
                                        tempAr = []
                                        zeroelem["ElementType"] = "SECTION"
                                        zeroelem["SequenceNo"] = 1
                                        zeroelem["FieldLabel"] = title
                                        elarray = []
                                        with open(formElementFile, 'r') as my_file:
                                            data1 = csv.reader(my_file, delimiter=',')
                                            if hasHeader1 == "Y":
                                                row1 = data1.next()
                                            seqNo = 1
                                            for row in data1:

                                                elID = row[0]
                                                fldlabel = row[0]
                                                type = row[1]
                                                hint = row[2]
                                                req = row[3]
                                                seqNo += 1
                                                addElement = {}
                                                addElement['ElementID'] = elID
                                                addElement['ElementType'] = type
                                                addElement['FieldLabel'] = fldlabel
                                                addElement['Hint'] = hint
                                                addElement['Required'] = req
                                                addElement['SequenceNo'] = seqNo
                                                if type == "SPINNER":
                                                    spinelements = row[4].split(";")
                                                    addElement['Options'] = spinelements
                                                elarray.append(dict(addElement))

                                        zeroelem['Elements'] = elarray
                                        tempAr.append(dict(zeroelem))


                                    body['Elements'] = tempAr

                                    body['DataSource'] = data['DataSource']

                                    print body

                                    jsonresponse = CM.hit_url_method(body, headers1, method, url)
                                    print " &&&&&&&&&&&&&&&&&&&&&&& "
                                    print jsonresponse
