
import json
import csv
import logon as LL
import common as CM
import re
import requests


def createForm(zviceID, tagID, title, desc, parentCardID):

    r = requests.get("https://twig.me/v1/push/dectest/" + zviceID)
    tagnum = r.json()['decTagID']

    ########## create a form
    # tagID = "BJ66CWKHL4JF5"
    r = requests.get("https://twig.me/v1/push/dectest/" + tagID)
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

zviceID = "EUNXYEQF7TGHR" ##### Dept ID
zbotID = "B969YSR37AT7G"    ####  Business ID

email = "admin@zestl.com"
pwd = "Zspladmin99"

# delfile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/delgrps.csv"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

# jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
# tagids = []
# for element in jsondata['data']['elements']:
#     if element['cardtype'] == "basecard" and element['tagId'] != zviceID and element['tagId'] != "EF9PHJBFDZ2GA":
#         tagids.append(element['tagId'])
#     # print element['title'] + " : " + element['backgroundImageUrl']
# print tagids

formElementFile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/subject_SELECTION_FORM_20dec.csv"
title = "Grade 8 SUBJECT SELECTION FORM"
desc = "Click new to submit"
hasHeader1 = "Y"

# tagids = [ "WHJQ7E4X68VBZ"]

tagids = [ "EUNXYEQF7TGHR"]    ###Dept ID
print "here"

for tag in tagids:
    print tag
    jsondata = CM.getBaseStructure(tag, headers1, BASE_URL)
    for card in jsondata['data']['elements']:
        if "Grade 8" in card['title']:
            parentCardID = json.loads(card['ctjsondata'])['parentCardID']
            url = card['cturl']
            body = json.loads(card['ctjsondata'])
            method = "POST"
            jcards = CM.hit_url_method(body, headers1, method, url)
            print "^^^^^^^^^^^^^^^^^^"
            print jcards

            for element in json.loads(jcards)['data']['elements']:
                # print element['title']
                if "IGCSE Subject Options 2017-18 Batch"  in element['title']:
                    print element['title']
                    subparentCardID = json.loads(element['ctjsondata'])['parentCardID']
                    url = element['cturl']
                    body = json.loads(element['ctjsondata'])
                    method = "POST"
                    subjcards = CM.hit_url_method(body, headers1, method, url)
                    print "^^^^^^^^^^^^^^^^^^"
                    print subjcards

                    for subelement in json.loads(subjcards)['data']['elements']:
                        # print subelement['title']
                        if title  in subelement['title']:
                            print subelement['title']

                            print "============================"
                            print title + " found"
                            print "============================"


                            for action in subelement['actions']:

                                # print action
                                if 'More Actions' in action['title']:
                                    for a in action['actions']:
                                        if "Edit" in a['title']:

                                            url = a['actionUrl']
                                            data = json.loads(a['data'])
                                            # print a
                                            print data
                                            method = a['method']
                                            print " &&&&&&&&&&&&&&&&&&&&&&& "
                                            print "HERE=================="
                                            body = {}

                                            body["FormDescription"] = data["FormDescription"]
                                            body["FormID"] = data["FormID"]

                                            body["FormTitle"] = data["FormTitle"]
                                            print data["FormTitle"]
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

                                            print data['Elements'][0]['Elements']
                                            if data['Elements'][0]['Elements'] == None:
                                                print "HERE============TOOOOOO======"

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
                                                        if type == "RADIO_GROUP":
                                                            spinelements = row[4].split(";")
                                                            addElement['Options'] = spinelements
                                                        elarray.append(dict(addElement))

                                                zeroelem['Elements'] = elarray
                                                tempAr.append(dict(zeroelem))
                                                print "HERE=================="


                                                body['Elements'] = tempAr

                                                body['DataSource'] = data['DataSource']

                                                print body

                                                # jsonresponse = CM.hit_url_method(body, headers1, method, url)
                                                print " &&&&&&&&&&&&&&&&&&&&&&& "
                                                print jsonresponse
