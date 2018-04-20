
import base64
import time
import urllib2
from urllib2 import URLError
from urllib2 import HTTPError
import requests
import urllib
import json
# import time
import os
import re
import sys
import csv
import StringIO
import itertools
import copy
import logon as LL
import common as CM
import hashlib

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


def hide_card(tagID, title, BASE_URL, headers1):
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
            element['hidden'] = True

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


def halfwide_card(tagID, title, BASE_URL, headers1):
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
            element['fullwidth'] = False

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

def createCalendar_level0(zviceID, title, desc, headers1, BASE_URL):
    r = requests.get("http://twig.me/v1/push/dectest/" + zviceID)
    tagnum = r.json()['decTagID']

    body = {"Title": title, "Description": desc,
                "interactionID": "CommonInteraction_INTERACTION_TYPE_ADD_CALENDAR", "ZviceID": tagnum,
                "categorytype": "Calendar", "LinkType": "CALENDAR"}
    method = "POST"
    url = BASE_URL + zviceID + "/calendars/"

    # jsonreply = method_url(body, headers1, url, method)
    jsonreply = CM.hit_url_method(body, headers1, method, url)

    jsonreply = json.loads(jsonreply)
    # jsonreply = hit_url_method(body, headers1, method, url)
    print "======calendar response ======="
    print unhide_card(zviceID, title, BASE_URL, headers1)

    return jsonreply

def createForm(zviceID, tagID, title, desc, formElementFile):

    r = requests.get("http://twig.me/v1/push/dectest/" + zviceID)
    tagnum = r.json()['decTagID']

    ########## create a form
    # tagID = "BJ66CWKHL4JF5"
    r = requests.get("http://twig.me/v1/push/dectest/" + tagID)
    zviceNum = r.json()['decTagID']

    url = BASE_URL + tagID + "/forms"
    method = "POST"
    body = {"FormTitle": title, "FormDescription": desc, "ZviceID": zviceNum, "ZbotID": tagnum, "LinkType": "FORM"}
    jsonresponse = CM.hit_url_method(body, headers1, method, url)

    print jsonresponse

    print unhide_card(tagID, title, BASE_URL, headers1)

    jsondata = CM.getBaseStructure(tagID, headers1, BASE_URL)
    # print json.dumps(jsondata)
    for element in jsondata['data']['elements']:
        if title in element['title']:
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
                            # print "*******^^^^^^^^^"
                            print data['Elements']
                            if data['Elements'] == None:
                                tempAr = []
                                zeroelem["ElementType"] = "SECTION"
                                zeroelem["SequenceNo"] = 1
                                zeroelem["FieldLabel"] = title
                                elarray = []
                                ##### add the elements here
                                with open(formElementFile, 'r') as my_file:
                                    data1 = csv.reader(my_file, delimiter=',')
                                    if hasHeader1 == "Y":
                                        row1 = data1.next()
                                    # method = "POST"
                                    seqNo = 1
                                    for row in data1:
                                        # print "^^^^^^^^^^^^^^^^^"
                                        # print row
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
                                        # print "***** &&&&&&&   ******"
                                        # print elarray
                                #### add element loop ends
                                zeroelem['Elements'] = elarray
                                tempAr.append(dict(zeroelem))
                                # print "**********"
                                # print tempAr
                            else:
                                tempAr = copy.deepcopy(data['Elements'])
                                for item in data['Elements'][0]:
                                    print "eeeeeeeeeeeeeeeee"
                                    print item
                                    if 'MetaID' in item:
                                        print "dddddddddddddddddddd"
                                        print item
                                        del tempAr[0][item]
                                    if item == "Elements":
                                        print data['Elements'][0][item]

                                        print " found   found    found"
                                        no = -1
                                        for xx in data['Elements'][0][item]:
                                            no += 1
                                            for k, v in xx.items():
                                                if 'MetaID' in k:
                                                    print xx
                                                    print "ddddddd------------ddddddddddddd"
                                                    print k
                                                    del tempAr[0][item][no][k]
                                print "********** Insert here **************"
                                addElement = {}
                                addElement['ElementID'] = "tf2"
                                addElement['ElementType'] = "EDIT_TEXT"
                                addElement['FieldLabel'] = "tf2"
                                addElement['Hint'] = "Hint text"
                                addElement['Required'] = 0
                                addElement['SequenceNo'] = 5

                                print tempAr[0]['Elements']
                                print " &&&&&&&&&&&&&&&&&&&&&&& "

                                tempAr[0]['Elements'].append(dict(addElement))

                                print tempAr[0]['Elements']
                            # except KeyError:
                            #     print "no elements"


                            body['Elements'] = tempAr

                            body['DataSource'] = data['DataSource']

                            print body

                            jsonresponse = CM.hit_url_method(body, headers1, method, url)
                            print " &&&&&&&&&&&&&&&&&&&&&&& "
                            return jsonresponse

def create_text_card_level0(title, desc, zviceID, BASE_URL, headers1):
    body = {}
    body['cardData'] = {"title": title, "desc": desc, "Flags": "true"}
    body['cardType'] = "TEXT"
    body['opType'] = 1
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"

    method = "POST"
    url = BASE_URL + "zvice/interaction/" + zviceID

    # jsonreply = method_url(body, headers1, url, method)
    jsonreply = CM.hit_url_method(body, headers1, method, url)
    jsonreply = json.loads(jsonreply)
    print "##############"
    print unhide_card(zviceID, title, BASE_URL, headers1)
    return jsonreply['cardid']


inputLoginFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/login.csv"

formElementFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/SiteVisitReport.csv"
ratefile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/rate.csv"

hasHeader = 'N'
hasHeader1 = 'Y'
hasHeaderzvice = 'Y'


SERVER = "https://twig.me/"
version = "v4/"
BASE_URL = SERVER + version

with open(inputLoginFile, 'r') as f:
    data = csv.reader(f, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()

    for row in data:
        email = row[0]
        password = row[1]

        headers, headers1 = LL.req_headers(email, password, BASE_URL)
        if headers1 == None:
            print email
            print password
            print "Login Failed"
            print headers1
            print "----------------"
        else:
            print email
            print password
            print "Login Pass"
            print headers1
            print "++++++++++++++++"

        zbotID = "9KTT97HP4ZX3A"

        zvicefile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/drivers.csv"


        with open(zvicefile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeaderzvice == "Y":
                row1 = data.next()
            for row in data:
                zviceID = row[0]

                print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                print zviceID

                print create_text_card_level0("About Me", "", zviceID, BASE_URL, headers1)

                print createForm(zbotID, zviceID, "Rate The Ride", "Click New to submit rating", ratefile)

                print createCalendar_level0(zviceID, "Check Availability", "Green time slots indicate available", headers1, BASE_URL)
                print createForm(zbotID, zviceID, "Book Next Trip", "", formElementFile)


                print hide_card(zviceID, "Contact Details", BASE_URL, headers1)
                print hide_card(zviceID, "More Details", BASE_URL, headers1)
                print hide_card(zviceID, "My Memberships", BASE_URL, headers1)
                print halfwide_card(zviceID, "Check Availability", BASE_URL, headers1)
                print halfwide_card(zviceID, "Book Next Trip", BASE_URL, headers1)


