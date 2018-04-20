import base64
import time
import urllib2
from urllib2 import URLError
from urllib2 import HTTPError
import requests
import urllib
import json
import time
import os
import re
import sys
import csv
import StringIO
import itertools
import hashlib \

# import lib.login1 as LL
import logon as LL
import common as CM


# def getBaseStructure(zbotID, headers1):
#     url = LL.BASE_URL + 'zvice/detailscard/' + zbotID
#     print "$^%^&%*^&*^&^*^&*^&^*&^"
#     print (url, zbotID)
#     RequestBody = {}
#     response = hit_url(RequestBody, headers1, zbotID, url)
#     with open('/Users/sujoychakravarty/Dropbox/Zestl-scripts/rundir/tmp', 'w') as f:
#         f.write(str(response))
#     return json.loads(response)

def returnBaseLevel(base_column):
    baseset = 0
    cardType = [None] * 40
    numcards = 0
    cardfound = 0
    cardDetails = {}
    cardstarted = 0
    endCard = 0
    rownum = 0
    cards = {}
    cardtypes = {}
    cardfoundLocation = -1
    isdept = 0

    for i in base_column:
        rownum += 1  ### this corresponds to the xls row number
        re.sub(r'[^\x00-\x7f]', r' ', i)
        i = unicode(i, 'cp1252')
        i = i.encode(encoding='UTF-8', errors='ignore')
        # i = i.encode(encoding='UTF-8',errors='ignore')

        ### first lookout for the base card
        if ('base card' in i.lower()):  ## the base card was found
            foundbase = 1
            cardfoundLocation = rownum - 1
        elif ('card' in i.lower() and baseset == 0):  ### the first card must be the base card
            sys.exit("base zbot ID is not provided")  ## call an exception
        if (foundbase == 1 and 'tag' in i.lower()):  ### the tag ID of the organization
            zbotID = re.sub(r'(\w{13}).*\(\wag\).*', r'\1', i)
            cardDetails[numcards] = "cID = " + zbotID
            base_column[cardfoundLocation] = base_column[cardfoundLocation] + '\tcID ' + zbotID
            numcards += 1
            foundbase = 0
            baseset = 1

        if ('card' in i.lower() and baseset == 1 and cardstarted == 0):  # brand new card
            isdept = 0
            cardType[numcards] = re.sub(r'(\w+)\s+\ward.*', r'\1', i)  # cardtype
            startCard = rownum  # unnecssaray info
            cardDetails[numcards] = i  # keep copying all teh card info into this
            cardID = zbotID + "_" + str(numcards)
            cardstarted = 1
            numcards += 1
            cardfoundLocation = rownum - 1
            if 'department' in i.lower():
                print "=======found dept ========="
                isdept = 1
        elif ('card' in i.lower() and baseset == 1 and cardstarted == 1):  # the next card has started
            isdept = 0
            cardType[numcards] = re.sub(r'(\w+)\s+\ward.*', r'\1', i)
            endCard = rownum - 1

            cardDetails[numcards - 1] += '\t(start) ' + str(startCard) + '\t(end) ' + str(
                endCard) + '\t(cID) ' + cardID  # close out the previous card
            base_column[cardfoundLocation] = base_column[cardfoundLocation] + '\t(cID) ' + cardID
            startCard = rownum
            cardID = zbotID + "_" + str(numcards)
            cardstarted = 1
            cardDetails[numcards] = i
            cardfoundLocation = rownum - 1
            numcards += 1
            if 'department' in i.lower():
                print "=======found dept ========="
                isdept = 1
        elif ('tag' in i.lower() and isdept == 1):
            zbotdep = re.sub(r'(\w{13}).*\(\wag\).*', r'\1', i)
            print "=======found dept zbotdep ========="
            cardID = zbotID + "_" + zbotdep
        elif (i == "" and cardstarted == 1):
            cardstarted = 0  ### the card is over
            endCard = rownum - 1
            cardDetails[numcards - 1] += '\t(start) ' + str(startCard) + '\t(end) ' + str(
                endCard) + '\t(has children)' + '\t(cID) ' + cardID
            # close out the previous card
            base_column[cardfoundLocation] = base_column[cardfoundLocation] + '\t(cID) ' + cardID
        elif (cardstarted == 1):
            # endCard = rownum
            cardDetails[numcards - 1] += '\t' + i  # more card info here
    if (cardstarted == 1):  ### ran out of more info - so close the open card and return
        endCard = rownum
        cardDetails[numcards - 1] += '\t' + i + '\t(start) ' + str(startCard) + '\t(end) ' + str(
            endCard) + '\t(cID) ' + cardID
        base_column[cardfoundLocation] = base_column[cardfoundLocation] + '\t(cID) ' + cardID

    for k, v in cardDetails.items():
        # print v.split('\t')
        cards[k] = v.split('\t')  ## each card is now a list
        cardtypes[k] = cardType[k]  ## corresponding cardtype is also a list

    # print cards

    return cards, cardtypes, zbotID, base_column


def returnJsonParams(cards, whichCardType):
    body = {}
    for x in cards:
        title = x['title']
        cardtype = x['cardtype']
        # print (title, cardtype)
        if re.search('basecard', cardtype):
            for a in x['actions']:
                if re.search('Add Cards', a['title']):
                    for b in a['actions']:
                        if re.search(whichCardType.lower(), b['title'].lower()):
                            actionUrl = b['actionUrl']
                            method = b['method']
                            for key, val in b.items():
                                if b['inputs'] != None:
                                    # print (whichCardType, b)
                                    for k in b['inputs']:
                                        for v in k['properties']:
                                            if v['name'] == 'id':
                                                keys = v['value']
                                                ks = 1
                                            elif v['name'] == 'hint' and ks == 1:
                                                values = "user defined"
                                                ks = 0
                                                body[keys] = values
                                            elif re.search('fault', v['name']) and ks == 1:
                                                values = v['value']
                                                ks = 0
                                                body[keys] = values
                                            elif v['name'] == 'text' and ks == 1:
                                                values = 'user input'
                                                ks = 0
                                                body[keys] = values
                                            elif v['name'] == 'list' and ks == 1:
                                                values = 'user selected'
                                                ks = 0
                                                body[keys] = values
                                            elif (v['name'] == 'hidden') or (v['name'] == 'idtype'):
                                                abc = 0
                                            elif ks == 0:
                                                abc = 0
                                            else:
                                                values = "failed all else " + v['name']
                                                ks = 0
                                                body[keys] = values
                                                # except KeyError:
                                elif ('Form' in b['title']):
                                    body = b['data']
                            return body, actionUrl, method


def method_url(body, headers, BASE_URL, method):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, body, headers)
    return jsondata['reply']


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def addCardIDs(cards, column):
    cardtypeFound = ''
    title = ''
    valid = 0
    print "==============column========================"
    print column
    for key, val in column.items():
        # column[key]['cardID'] = ''
        for v in val:
            # print "===============values are here    " + str(v) + "       =================="
            if (any(x in v.lower() for x in ('text card', 'forum card', 'gallery card', 'calendar card', 'form card'))):
                valid = 1
            if ('title' in v.lower() and valid == 1):
                # valid = 0
                title = re.sub(r'(.*)\(\s*title\s*\).*', r'\1', v.lower())
                # print "===============here and now outside ==========="
                # print title
                valid = 0
                for card in cards:
                    if title in card['title']:
                        # print "===============here and now title ==========="
                        for q in card['actions'][0]['actions']:
                            if "Add Text Card" in q['title']:
                                # print q['inputs'][5]['properties'][1]['value'] ##this is the cardID
                                column[key].append(str(q['inputs'][5]['properties'][1]['value']) + " (cID) ")
    print "========NEw column=============="
    return column

    #     entries =  val.split(",")
    #     for e in entries:
    #         if title in e:
    #             title = re.sub(r'(.*)\(\s*title\s*\).*', r'\1', e.lower())
    #             print "===============here and now outside ==========="
    #             print title
    # if title in card['title']:
    #     print "===============here and now ==========="
    #     print card['title']

    return ()


def returnCardLevel(prev_column, thisColumn, next_column):
    baseset = 0
    cardType = [None] * 1000
    numcards = 0
    cardfound = 0
    cardDetails = {}
    cardstarted = 0
    endCard = 0
    rownum = 0
    cards = {}
    cardtypes = {}
    parenttitle = ""
    parenttag = ""
    parentcarddtype = ""
    cardfoundLocation = -1
    isdept = 0
    parentCID = ''

    for i in thisColumn:
        re.sub(r'[^\x00-\x7f]', r' ', i)
        # i = i.decode('utf8')
        i = unicode(i, 'cp1252')
        i = i.encode(encoding='UTF-8',errors='ignore')


        rownum += 1
        if ('card' in i.lower() and cardstarted == 0):
            isdept = 0
            cardType[numcards] = re.sub(r'(\w+)\s+\ward.*', r'\1', i)
            startCard = rownum
            cardDetails[numcards] = i
            cardstarted = 1
            m = rownum - 1

            while ('card' not in prev_column[m].lower()):
                if ('title' in prev_column[m].lower()):
                    parenttitle = prev_column[m]
                elif ('tag' in prev_column[m].lower()):
                    parenttag = prev_column[m]
                m -= 1
            parentCID = re.sub(r'.*\(cID\)\s+(\w+)', r'\1', prev_column[m])
            parentcarddtype = re.sub(r'(.*)\(cID\)\s+\w+', r'\1', prev_column[m])
            cardID = parentCID + "_" + str(numcards)
            cardfoundLocation = rownum - 1
            numcards += 1
            if 'department' in i.lower():
                print "=======found dept ========="
                isdept = 1

        elif ('card' in i.lower() and cardstarted == 1):
            isdept = 0
            cardType[numcards] = re.sub(r'(\w+)\s+\ward.*', r'\1', i)
            endCard = rownum - 1
            cardDetails[numcards - 1] += '\t(start) ' + str(startCard) + '\t(end) ' + str(
                endCard) + '\t(parenttag) ' + parenttag + '\t(parenttype) ' + parentcarddtype + '\t(cID) ' + cardID
            thisColumn[cardfoundLocation] = thisColumn[cardfoundLocation] + '\t(cID) ' + cardID
            startCard = rownum
            cardstarted = 1
            cardDetails[numcards] = i
            m = rownum - 1

            while ('card' not in prev_column[m].lower()):
                if ('title' in prev_column[m].lower()):
                    parenttitle = prev_column[m]
                elif ('tag' in prev_column[m].lower()):
                    parenttag = prev_column[m]
                m -= 1
            parentcarddtype = re.sub(r'(.*)\(cID\)\s+\w+', r'\1', prev_column[m])
            # parentcarddtype = prev_column[m]
            parentCID = re.sub(r'.*\(cID\)\s+(\w+)', r'\1', prev_column[m])
            cardID = parentCID + "_" + str(numcards)
            cardfoundLocation = rownum - 1
            numcards += 1
            if 'department' in i.lower():
                print "=======found dept ========="
                isdept = 1
        elif ('tag' in i.lower() and isdept == 1):
            zbotdep = re.sub(r'(\w{13}).*\(\wag\).*', r'\1', i)
            print "=======found dept zbotdep ========="
            cardID = parentCID + "_" + zbotdep

        elif (i == "" and cardstarted == 1):
            cardstarted = 0
            endCard = rownum - 1
            if next_column[endCard] != "":
                cardDetails[numcards - 1] += '\t(start) ' + str(startCard) + '\t(end) ' + str(
                    endCard) + '\t(has children)' + '\t(parenttag) ' + parenttag + '\t(parenttype) ' + parentcarddtype + '\t(cID) ' + cardID
                thisColumn[cardfoundLocation] = thisColumn[cardfoundLocation] + '\t(cID) ' + cardID
            else:
                # cardstarted = 0
                cardDetails[numcards - 1] += '\t(start) ' + str(startCard) + '\t(end) ' + str(
                    endCard) + '\t(parenttag) ' + parenttag + '\t(parenttype) ' + parentcarddtype + '\t(cID) ' + cardID
                thisColumn[cardfoundLocation] = thisColumn[cardfoundLocation] + '\t(cID) ' + cardID
        elif (cardstarted == 1):
            # endCard = rownum
            cardDetails[numcards - 1] += '\t' + i

    if (cardstarted == 1):
        endCard = rownum
        cardDetails[numcards - 1] += '\t' + i + '\t(start) ' + str(startCard) + '\t(end) ' + str(
            endCard) + '\t(parenttag) ' + parenttag + '\t(parenttype) ' + parentcarddtype + '\t(cID) ' + cardID
        thisColumn[cardfoundLocation] = thisColumn[cardfoundLocation] + '\t(cID) ' + cardID

    for k, v in cardDetails.items():
        # print v.split('\t')
        cards[k] = v.split('\t')
        cardtypes[k] = cardType[k]

    # print cards

    return cards, cardtypes, thisColumn


def readStructure(fname):
    baseset = 0
    cardType = {}
    numcards = 0
    cardfound = 0
    cardDetails = {}
    cardstarted = 0
    endCard = 0
    rownum = 0
    # cardType1 = {}
    # cardDetails1 = {}


    with open(fname, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        column = {}
        nullElement = ""

        for row in data:
            for j in range(len(row)):
                try:
                    column[j].append(row[j])
                except:
                    column[j] = []
                    column[j].append(row[j])
            j = len(row)
            try:
                column[j].append(nullElement)
            except:
                column[j] = []
                column[j].append(nullElement)
    return column


def returnCall(whichCardType, body, iCard):
    textcardData = {}
    if ('depart' in whichCardType.lower()):
        body['title'] = iCard['title']
        body['zviceinfo'] = "Enter info here"
        body['zviceid'] = iCard['zviceID']
        body['tagprofilestr'] = 'ORGANISATION'
        print "==========ddddddd============"
        # print body
        # response = method_url(body, headers1, actionUrl, method)
        # print response
        # response = returnCardcustomStatus(cards)
        # print "************************"
        # print response
    elif ('text' in whichCardType.lower()):
        # RequestBody = {"cardData":
        #                   {"desc":desc, "title":title},
        #                   "opType":"1",
        #                   "parentCardID":parentID,
        #                   "cardType": ctype,
        #                   "interactionID":"CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
        #             }        body['title'] = iCard['title']
        textcardData['desc'] = "Enter info here"
        textcardData['title'] = iCard['title']
        body['cardData'] = textcardData
        print "==========ttttt============"
        # print body
    elif ('forum' in whichCardType.lower()):
        body['text'] = iCard['title']
        body['desc'] = "Enter info here"
        print "==========fffffff============"
        # print body
    elif ('calendar' in whichCardType.lower()):
        body['Title'] = iCard['title']
        body['Description'] = "Enter info here"
        print "==========cccccc============"
        # print body
    elif ('gallery' in whichCardType.lower()):
        body['Title'] = iCard['title']
        body['Description'] = "Enter info here"
        print "==========ggggg============"
        # print body
    elif ('form' in whichCardType.lower()):
        # print "$$$$$$$$$$$$$$$$"
        body = json.loads(body)
        # print body['FormID']
        body['FormTitle'] = iCard['title']
        body['FormDescription'] = "Enter info here"
        print "==========form form============"
        # print body
    else:
        print "creating " + whichCardType + " is not yet supported"
    return body


def returnAllCards(cardDetails, zbotID):
    order = -1
    finalCards = {}
    for k, v in cardDetails.items():
        print v
        # print "++++++++++++++++++++++++++++++"

        for a, b in v.items():
            order += 1
            indiCard = {}
            Ptags = []
            indiCard['level'] = k
            # print b   ######these are the individual cards to be created
            print "---------b here -------"
            print b
            for d in b:
                if 'parenttitle' in d.lower():
                    # Ptitle = re.sub(r'\(parenttitle\)\s+(.*)\(\s*title\s*\).*', r'\1', d.lower())
                    Ptitle = re.sub(r'\(parenttitle\)\s+(.*)\(\s*title\s*\).*', r'\1', d , flags = re.I)

                    print "==============ptptptptptptp================="
                    indiCard['Ptitle'] = Ptitle
                elif 'title' in d.lower():
                    print "==============tttttttttttttt================="
                    # title = re.sub(r'(.*)\(\s*title\s*\).*', r'\1', d.lower())
                    title = re.sub(r'(.*)\(\s*title\s*\).*', r'\1', d, flags = re.I)
                    indiCard['title'] = title
                elif 'description' in d.lower():
                    print "==============tttttttttttttt================="
                    # title = re.sub(r'(.*)\(\s*title\s*\).*', r'\1', d.lower())
                    desc = re.sub(r'(.*)\(\s*description\s*\).*', r'\1', d, flags=re.I)
                    indiCard['desc'] = desc
                elif '(cid)' in d.lower():
                    print "==============ptagttttttptagtttttt================="
                    Ptag = re.sub(r'\(CID\)\s+(.*)', r'\1', d.upper())
                    indiCard['cid'] = Ptag
                    Ptags = Ptag.split("_")
                    depth = 0
                    for i in range(0, len(Ptags)):
                        print Ptags[i]
                        if (re.search(r'\w{13}', Ptags[i])):
                            if (i == len(Ptags) - 1):
                                zviceID = Ptags[i]
                                indiCard['zviceID'] = zviceID
                            else:
                                Ptag = Ptags[i]
                                indiCard['Ptag'] = Ptag
                                zviceID = Ptags[i]
                                indiCard['zviceID'] = zviceID
                        else:
                            depth += 1
                        indiCard['depth'] = depth
                elif 'parenttype' in d.lower():
                    print "==============ttptypetttttptypettttt================="
                    if re.search(r'\(parenttype\)\s+(\w+)\s+card.*', d.lower()):
                        Ptype = re.sub(r'\(parenttype\)\s+(\w+)\s+card.*', r'\1', d.lower())
                    else:
                        Ptype = "not found"
                    indiCard['Ptype'] = Ptype
                elif 'tag' in d.lower():
                    print "==============ttagtttttttagttttt================="
                    zviceID = re.sub(r'\s*(\w{13})\s+\(\s*TAG\s*\).*', r'\1', d.upper())
                    indiCard['zviceID'] = zviceID
                elif 'card' in d.lower():
                    print "==============tttctypettttttctttt================="
                    Ctype = re.sub(r'\s*(\w+).*card.*', r'\1', d.lower())
                    indiCard['Ctype'] = Ctype
            print "===========ic======ic==================="
            try:
                indiCard['order'] = order
                finalCards[indiCard['cid']] = indiCard
                # print indiCard['cid']
            except KeyError:
                print (k, a)

                # print  "==================all the cards =========="
    finalCards[zbotID] = {'Ptype': 'none', 'Ctype': 'base', 'zviceID': zbotID, 'cid': zbotID, 'depth': 0, 'level': 0, 'title': 'base', 'Ptag': zbotID, "order" : 0 }
    return finalCards


def returnCallText(jsondata, detail):
    for element in jsondata['data']['elements']:
        # print element['cardtype']
        if 'basecard' in element['cardtype']:
            # print element['actions']
            for action in element['actions']:
                if 'Add Cards' in action['title']:
                    print "$$$$$$$$$$$ i was here $$$$$$$$$$"
                    for b in action['actions']:
                        if "Add Text Card" in b['title']:
                            url = re.sub(r'(.*)\w{13}', r'\1', b['actionUrl'])
                            url = url + detail['zviceID']
    return url  ## eureka - the right call is found


def returnCallDept(jsondata):
    print jsondata['data']['elements']
    for element in jsondata['data']['elements']:
        # print element['cardtype']
        if 'basecard' in element['cardtype']:
            print element['actions']
            for action in element['actions']:
                if 'Add Cards' in action['title']:
                    print "$$$$$$$$$$$ i was here $$$$$$$$$$"
                    for b in action['actions']:
                        if "Add Department" in b['title']:
                            url = b['actionUrl']
    return url  ## eureka - the right call is found

### has to be modified
def returnCallForm(jsondata, detail):
    for element in jsondata['data']['elements']:
        # print element['cardtype']
        if 'basecard' in element['cardtype']:
            # print element['actions']
            for action in element['actions']:
                if 'Add Cards' in action['title']:
                    print "$$$$$$$$$$$ i was here $$$$$$$$$$"
                    for b in action['actions']:
                        if "Add Form" in b['title']:
                            url = re.sub(r'(.*)\/\w{13\/(.*)}', r'\1' + detail['zviceID'] + r'\2', b['actionUrl'])
    return url  ## eureka - the right call is found

def returnCallForum(jsondata, detail):
    for element in jsondata['data']['elements']:
        # print element['cardtype']
        if 'basecard' in element['cardtype']:
            # print element['actions']
            for action in element['actions']:
                if 'Add Cards' in action['title']:
                    print "$$$$$$$$$$$ i was here $$$$$$$$$$"
                    for b in action['actions']:
                        if "Add Forum" in b['title']:
                            url = re.sub(r'(.*)\w{13}', r'\1', b['actionUrl'])
                            url = url + detail['zviceID']
    return url  ## eureka - the right call is found

def returnCallLink(jsondata, detail):
    for element in jsondata['data']['elements']:
        # print element['cardtype']
        if 'basecard' in element['cardtype']:
            # print element['actions']
            for action in element['actions']:
                if 'Add Cards' in action['title']:
                    print "$$$$$$$$$$$ i was here $$$$$$$$$$"
                    for b in action['actions']:
                        if "Add Link Card" in b['title']:
                            url = re.sub(r'(.*)\w{13}', r'\1', b['actionUrl'])
                            url = url + detail['zviceID']
    return url  ## eureka - the right call is found

def returnCallCalendar(jsondata, detail):
    for element in jsondata['data']['elements']:
        # print element['cardtype']
        if 'basecard' in element['cardtype']:
            # print element['actions']
            for action in element['actions']:
                if 'Add Cards' in action['title']:
                    print "$$$$$$$$$$$ i was here $$$$$$$$$$"
                    for b in action['actions']:
                        if "Add Calendar Card" in b['title']:
                            url = re.sub(r'(.*)\/\w{13\/(.*)}', r'\1' + detail['zviceID'] + r'\2', b['actionUrl'])
                            # url = url + detail['zviceID']
    return url  ## eureka - the right call is found


def returnCallGallery(jsondata, detail):
    for element in jsondata['data']['elements']:
        # print element['cardtype']
        if 'basecard' in element['cardtype']:
            # print element['actions']
            for action in element['actions']:
                if 'Add Cards' in action['title']:
                    print "$$$$$$$$$$$ i was here $$$$$$$$$$"
                    for b in action['actions']:
                        if "Add Gallery Card" in b['title']:
                            url = re.sub(r'(.*)\/\w{13\/(.*)}', r'\1' + detail['zviceID'] + r'\2', b['actionUrl'])
                            # url = url + detail['zviceID']
    return url  ## eureka - the right call is found

def returnCallAttendance(jsondata, detail):
    for element in jsondata['data']['elements']:
        # print element['cardtype']
        if 'basecard' in element['cardtype']:
            # print element['actions']
            for action in element['actions']:
                if 'Add Cards' in action['title']:
                    print "$$$$$$$$$$$ i was here $$$$$$$$$$"
                    for b in action['actions']:
                        if "Add Attendance Scan" in b['title']:
                            url = re.sub(r'(.*)\w{13}', r'\1', b['actionUrl'])
                            url = url + detail['zviceID']
                            # url = url + detail['zviceID']
    return url  ## eureka - the right call is found

if __name__ == '__main__':
    # sys.('utf8')
    cardType = {}
    cardDetails = {}
    finalCards = {}
    zbotID = ''
    email = 'admin@zestl.com'
    pwd = 'TwigMeNow'
    SERVER = "http://52.8.240.85/"
    version = "v4/"
    BASE_URL = SERVER + version

    # i login
    # headers, headers1 = LL.req_headers()
    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

    ### read the file structure into columns
    column = readStructure(sys.argv[1])

    ##### level 0 necessarily contains the base card and cards here have no 'parents'. hence this is treated seperately
    cardDetails[0], cardType[0], zbotID, column[0] = returnBaseLevel(column[0])

    print "==========zzzzzzzzzzzz============"
    print zbotID
    print " ======== Card Details =============="
    print cardDetails
    print " ======== Card Details =============="

    #### all lower level cards are treated similarly - so i loop through them all to create the array
    print "==============nnnnnnnnnnnn=================="
    for i in range(1, len(column) - 1):
        cardDetails[i], cardType[i], column[i] = returnCardLevel(column[i - 1], column[i], column[i + 1])
    # print cardDetails
    # print cardType

    print "=========column ========"
    print column

    abc = 0
    ks = 1
    body = {}

    # zbotID = LL.zbotID

    # get the base card structure - before creation of other level 0 cards
    # response = getBaseStructure(zbotID, headers1)

    # cards = response['data']['elements']
    # print "========card details ============="
    # print cardDetails

    finalCards = returnAllCards(cardDetails, zbotID)
    print "==========final cards============"
    print finalCards
    print len(finalCards)
    orderedCards = [None] * len(finalCards)
    for cardID, details in finalCards.items():
        orderedCards[details['order']] = details

    print "======= a debug line ====="
    print orderedCards[2]
    print "==========="
    print orderedCards

    hier = {}
    # now start creating the cards
    # for cardID, details in finalCards.items():
    #     print (details['order'], details['Ctype'])
    details = []
    kl = 0
    for kl in range(0, len(column)):
        for i in range(1, len(orderedCards)):

            details = orderedCards[i]
            cardID = details['cid']
            cardexists = 0
            if (details['level'] == kl):

                print details
                jsondata = CM.getBaseStructure(details['Ptag'], headers1, BASE_URL)
                print "=========debug======"
                print jsondata
                # print details
                if "department" in details['Ctype'].lower():
                    body = {}
                    print "===========dept card " + str(details['level']) + " ================="

                    print cardID
                    print details
                    print "----------------"
                    print "-----dept base response -------"
                    print jsondata
                    url = returnCallDept(jsondata)
                    # for element in jsondata['data']['elements']:
                    #     # print element['cardtype']
                    #     if 'basecard' in element['cardtype']:
                    #         # print element['actions']
                    #         for action in element['actions']:
                    #             if 'Add Cards' in action['title']:
                    #                 for b in action['actions']:
                    #                     if "Add Department" in b['title']:
                    #                         url =  b['actionUrl'] ## eureka - the right call is found
                    try:
                        desc1 = details['desc']
                    except KeyError:
                        desc1 = "dep"

                    body = {"title": details['title'], "zviceinfo": desc1, "zviceid": details['zviceID'],
                            "zbotid": details['Ptag'], "zvicetype": "ZTAG", "zvicelink": "NEW", "lat": "-", "long": "-",
                            "zviceloc": "--", "tagprofilestr": "ORGANISATION"}
                    method = "PUT"
                    print "=======The call =========="
                    print url
                    print body
                    print method
                    print "=======end call ========="
                    jsonreply = method_url(body, headers1, url, method)
                    jsonreply = json.loads(jsonreply)
                    print jsonreply
                    print "======department created========"


    kl = 0
    for kl in range(0, len(column)):
        for i in range(1, len(orderedCards)):
            details = orderedCards[i]
            cardID = details['cid']
        # for cardID, details in finalCards.items():
            cardexists = 0
            if (details['level'] == kl):
                print details
                jsondata = CM.getBaseStructure(details['Ptag'], headers1, BASE_URL)
                # print "=========debug======"
                # print jsondata

                if "text" in details['Ctype'].lower():
                    print "===========text card " + str(details['level']) + " ================="
                    print cardID
                    for element in jsondata['data']['elements']:
                        # print element['cardtype']
                        if 'webviewcard' in element['cardtype']:
                            if details['title'] in element['title']:
                                cardexists = 0  ### change this to '1' finally
                                print " ============ CARD CREATION ERROR ================= "
                                print ("A card with this name already exists at this level")
                    if details['depth'] == 1 and cardexists == 0:
                        body = {}
                        print " - - - 0 depth card - - -"
                        print "----------------"
                        print "-----dept base response -------"
                        url = returnCallText(jsondata, details)
                        # for element in jsondata['data']['elements']:
                        #     # print element['cardtype']
                        #     if 'basecard' in element['cardtype']:
                        #         # print element['actions']
                        #         for action in element['actions']:
                        #             if 'Add Cards' in action['title']:
                        #                 print "$$$$$$$$$$$ i was here $$$$$$$$$$"
                        #                 for b in action['actions']:
                        #                     if "Add Text Card" in b['title']:
                        #                         url = re.sub(r'(.*)\w{13}',r'\1',b['actionUrl'])
                        #                         url = url + details['zviceID']
                        #                         print url## eureka - the right call is found
                        try :
                            desc1 = details['desc']
                        except KeyError:
                            desc1 = " "
                        body['cardData'] = {"title": details['title'], "desc": desc1, "Flags" : "true"}
                        # body['desc'] = details['cid']
                        body['cardType'] = "TEXT"
                        body['opType'] = 1
                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
                        #
                        # body = {"title": details['title'], "desc": details['cid'], "cardType" : "TEXT", "opType" : 1,  "interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION" }
                        method = "POST"
                        print "=======The call =========="
                        print url
                        print body
                        print method
                        print "=======end call ========="
                        jsonreply = method_url(body, headers1, url, method)
                        jsonreply = json.loads(jsonreply)
                        print "##############"
                        # print jsonreply
                        # jsonreply = hit_url_method(body, headers1, method, url)
                        print jsonreply['cardid']
                        finalCards[details['cid']]['UID'] = jsonreply['cardid']
                        orderedCards[i]['UID'] = jsonreply['cardid']

                        print "------phew phew -------"
                        #     # print element['actions']
                        #     for action in element['actions']:
                        #         if 'Add Cards' in action['title']:

                        print "$$$$$$%%%%%%%%$$$$$$$$$$$"
                        # print details['title']
                    elif details['depth'] > 1 and cardexists == 0:
                        body = {}
                        depth = details['depth']

                        print " - - - " + str(depth) + " depth card - - -"
                        print "&&&&&&&&&&&&&&&&&&&&&&&&&&&"
                        print details
                        for k, v in details.items():
                            print k
                        parentcid = re.sub(r'(.*)_\d+', r'\1', cardID)
                        print "===============" + parentcid + "================"
                        parentUID = finalCards[parentcid]['UID']
                        print parentUID
                        print "*********************************"
                        print " - - - " + str(depth - 1) + "  depth card - - -"
                        print "----------------"
                        print "-----dept base response -------"
                        url = returnCallText(jsondata, details)
                        # for element in jsondata['data']['elements']:
                        #     # print element['cardtype']
                        #     if 'basecard' in element['cardtype']:
                        #         # print element['actions']
                        #         for action in element['actions']:
                        #             if 'Add Cards' in action['title']:
                        #                 print "$$$$$$$$$$$ i was here $$$$$$$$$$"
                        #                 for b in action['actions']:
                        #                     if "Add Text Card" in b['title']:
                        #                         url = re.sub(r'(.*)\w{13}',r'\1',b['actionUrl'])
                        #                         url = url + details['zviceID']
                        #                         print url## eureka - the right call is found
                        try:
                            desc1 = details['desc']
                        except KeyError:
                            desc1 = " "
                        body['cardData'] = {"title": details['title'], "desc": desc1, "Flags" : "true"}
                        # body['desc'] = details['cid']
                        body['cardType'] = "TEXT"
                        body['opType'] = 1
                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
                        body['parentCardID'] = parentUID
                        method = "POST"
                        print "=======The call =========="
                        print url
                        print body
                        print method
                        print "=======end call ========="
                        jsonreply = method_url(body, headers1, url, method)
                        jsonreply = json.loads(jsonreply)
                        # jsonreply = hit_url_method(body, headers1, method, url)
                        print jsonreply['cardid']
                        orderedCards[i]['UID'] = jsonreply['cardid']

                        finalCards[details['cid']]['UID'] = jsonreply['cardid']

                        print "------phew phew phew-------"
                        #     # print element['actions']
                        #     for action in element['actions']:
                        #         if 'Add Cards' in action['title']:

                        print "$$$$$$%%%%%%%%$888888888888888$$$$$$$$$$"
                        # while depth > 0:
                        #     parentcid = re.sub(r'(.*)_\d+', r'\1', parentcid)
                        #     hier[depth] = finalCards[parentcid]['title']
                        #     depth -= 1
                        # print hier
                elif "calendar" in details['Ctype'].lower():
                    if cardexists == 0:
                        body = {}
                        print " - - - 0 depth card - - -"
                        print "----------------"
                        print "-----dept base response -------"
                        url = returnCallCalendar(jsondata, details)
                        print "^^^^^^^   CALENDAR ^^^^^^^^^"
                        print url
                        r = requests.get("http://twig.me/v1/push/dectest/" + details['Ptag'])
                        tagnum =  r.json()['decTagID']
                        print "===========rrrrrrrrrrrrr============="
                        if details['depth'] == 1:
                            try:
                                desc1 = details['desc']
                            except KeyError:
                                desc1 = " "
                            body = {"Title" : details['title'], "Description" : desc1, "interactionID" : "CommonInteraction_INTERACTION_TYPE_ADD_CALENDAR", "ZviceID" : tagnum, "categorytype" : "Calendar", "LinkType" : "CALENDAR" }
                        else:
                            parentcid = re.sub(r'(.*)_\d+', r'\1', cardID)
                            print "===============" + parentcid + "================"
                            parentUID = finalCards[parentcid]['UID']
                            try:
                                desc1 = details['desc']
                            except KeyError:
                                desc1 = " "
                            body = {"Title": details['title'], "Description": desc1,"interactionID": "CommonInteraction_INTERACTION_TYPE_ADD_CALENDAR", "ZviceID": tagnum, "categorytype": "Calendar", "LinkType": "CALENDAR", "parentCardID" : parentUID}
                        method = "POST"
                        print "=======The call calendar =========="
                        print url
                        print body
                        print method
                        print "=======end call calendar========="
                        jsonreply = method_url(body, headers1, url, method)
                        jsonreply = json.loads(jsonreply)
                        # jsonreply = hit_url_method(body, headers1, method, url)
                        print "======calendar response ======="
                        print jsonreply
                        # finalCards[details['cid']]['UID'] = jsonreply['cardid']

                    print "===========text card " + str(details['level']) + " ================="
                    print cardID
                    for element in jsondata['data']['elements']:
                        # print element['cardtype']
                        if 'webviewcard' in element['cardtype']:
                            if details['title'] in element['title']:
                                cardexists = 0  ### change this to '1' finally
                                print " ============ CARD CREATION ERROR ================= "
                                print ("A card with this name already exists at this level")
                    # if details['depth'] == 1 and cardexists == 0:
                    body = {}
                    print " - - - calendar card - - -"
                    print "----------------"
                    print "-----dept base response -------"
                    url = returnCallCalendar(jsondata, details)
                    print "^^^^^^^   CALENDAR ^^^^^^^^^"
                    print url

                elif "gallery" in details['Ctype'].lower():
                    if cardexists == 0:
                        body = {}
                        print " - - - 0 depth card - - -"
                        print "----------------"
                        print "-----dept base response -------"
                        url = returnCallGallery(jsondata, details)
                        print "^^^^^^^   GALERY ^^^^^^^^^"
                        print url
                        r = requests.get("http://twig.me/v1/push/dectest/" + details['Ptag'])
                        tagnum =  r.json()['decTagID']
                        print "===========rrrrrrrrrrrrr============="
                        if details['depth'] == 1:
                            try:
                                desc1 = details['desc']
                            except KeyError:
                                desc1 = " "
                            body = {"Title" : details['title'], "Description" : desc1 }
                        else:
                            parentcid = re.sub(r'(.*)_\d+', r'\1', cardID)
                            print "===============" + parentcid + "================"
                            parentUID = finalCards[parentcid]['UID']
                            try:
                                desc1 = details['desc']
                            except KeyError:
                                desc1 = " "
                            body = {"Title": details['title'], "Description": desc1, "parentCardID" : parentUID}
                        method = "POST"
                        print "=======The call gallery =========="
                        print url
                        print body
                        print method
                        print "=======end call gallery========="
                        jsonreply = method_url(body, headers1, url, method)
                        jsonreply = json.loads(jsonreply)
                        # jsonreply = hit_url_method(body, headers1, method, url)
                        print "======gallery response ======="
                        print jsonreply
                        # finalCards[details['cid']]['UID'] = jsonreply['cardid']

                    print "===========text card " + str(details['level']) + " ================="
                    print cardID
                    for element in jsondata['data']['elements']:
                        # print element['cardtype']
                        if 'webviewcard' in element['cardtype']:
                            if details['title'] in element['title']:
                                cardexists = 0  ### change this to '1' finally
                                print " ============ CARD CREATION ERROR ================= "
                                print ("A card with this name already exists at this level")
                    # if details['depth'] == 1 and cardexists == 0:
                    body = {}
                    print " - - - calendar card - - -"
                    print "----------------"
                    print "-----dept base response -------"
                    url = returnCallCalendar(jsondata, details)
                    print "^^^^^^^   CALENDAR ^^^^^^^^^"
                    print url

                elif "form" in details['Ctype'].lower():
                    if cardexists == 0:
                        body = {}
                        print " - - - 0 depth card - - -"
                        print "----------------"
                        print "-----dept base response -------"
                        url = returnCallForm(jsondata, details)
                        print "^^^^^^^   FORM ^^^^^^^^^"
                        print url
                        r = requests.get("http://twig.me/v1/push/dectest/" + details['Ptag'])
                        tagnum =  r.json()['decTagID']
                        r = requests.get("http://twig.me/v1/push/dectest/" + zbotID)
                        zbotnum = r.json()['decTagID']
                        print "===========rrrrrrrrrrrrr============="
                        if details['depth'] == 1:
                            try:
                                desc1 = details['desc']
                            except KeyError:
                                desc1 = " "
                            body = {"FormID" :"", "FormDescription" : desc1, "FormTitle" : details['title'], "ZviceID":tagnum,"ZbotID":zbotnum,"LinkType":"FORM","LinkID":""}
                        else:
                            parentcid = re.sub(r'(.*)_\d+', r'\1', cardID)
                            print "===============" + parentcid + "================"
                            parentUID = finalCards[parentcid]['UID']
                            try:
                                desc1 = details['desc']
                            except KeyError:
                                desc1 = " "
                            body = {"FormID": "", "FormDescription": desc1, "FormTitle" : details['title'],"ZviceID": tagnum, "ZbotID": zbotnum, "LinkType": "FORM", "LinkID": "", "parentCardID": parentUID}
                            # body = {"Title": details['title'], "Description": details['cid'], "parentCardID" : parentUID}
                        method = "POST"
                        print "=======The call form =========="
                        print url
                        print body
                        print method
                        print "=======end call form========="
                        jsonreply = method_url(body, headers1, url, method)
                        jsonreply = json.loads(jsonreply)
                        # jsonreply = hit_url_method(body, headers1, method, url)
                        print "======form response ======="
                        print jsonreply
                        # finalCards[details['cid']]['UID'] = jsonreply['cardid']

                    print "===========text card " + str(details['level']) + " ================="
                    print cardID
                    for element in jsondata['data']['elements']:
                        # print element['cardtype']
                        if 'webviewcard' in element['cardtype']:
                            if details['title'] in element['title']:
                                cardexists = 0  ### change this to '1' finally
                                print " ============ CARD CREATION ERROR ================= "
                                print ("A card with this name already exists at this level")
                    # if details['depth'] == 1 and cardexists == 0:
                    body = {}
                    print " - - - form card - - -"
                    print "----------------"
                    print "-----dept base response -------"
                    url = returnCallCalendar(jsondata, details)
                    print "^^^^^^^   FORM ^^^^^^^^^"
                    print url

                elif "forum" in details['Ctype'].lower():
                    if cardexists == 0:
                        body = {}
                        print " - - - 0 depth card - - -"
                        print "----------------"
                        print "-----dept base response -------"
                        url = returnCallForum(jsondata, details)
                        print "^^^^^^^   FORUM ^^^^^^^^^"
                        print url
                        if details['depth'] == 1:
                            body = {"Text" : details['title'], "Flags" : "true", "FlagsInside" : "true"}
                        else:
                            parentcid = re.sub(r'(.*)_\d+', r'\1', cardID)
                            print "===============" + parentcid + "================"
                            parentUID = finalCards[parentcid]['UID']
                            # body = {"cardData": {"text": details['title']}, "cardType": "CHAT", "opType": 1, "interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION", "parentCardID" : parentUID}
                            body = {"Text" : details['title'], "parentCardID" : parentUID, "Flags" : "true", "FlagsInside" : "true"}


                        method = "POST"
                        print "=======The call forum =========="
                        print url
                        print body
                        print method
                        print "=======end call forum========="
                        jsonreply = method_url(body, headers1, url, method)
                        jsonreply = json.loads(jsonreply)
                        # jsonreply = hit_url_method(body, headers1, method, url)
                        print "======forum response ======="
                        print jsonreply
                        # finalCards[details['cid']]['UID'] = jsonreply['cardid']

                    print "===========text card " + str(details['level']) + " ================="
                    print cardID
                    for element in jsondata['data']['elements']:
                        # print element['cardtype']
                        if 'webviewcard' in element['cardtype']:
                            if details['title'] in element['title']:
                                cardexists = 0  ### change this to '1' finally
                                print " ============ CARD CREATION ERROR ================= "
                                print ("A card with this name already exists at this level")
                    # if details['depth'] == 1 and cardexists == 0:
                    body = {}
                    print " - - - forum card - - -"
                    print "----------------"
                    print "-----dept base response -------"
                    url = returnCallCalendar(jsondata, details)
                    print "^^^^^^^   FORUM ^^^^^^^^^"
                    print url
#### attendance card not written out yet - dont support
                # elif "attendance" in details['Ctype'].lower():
                #     if cardexists == 0:
                #         body = {}
                #         print " - - - 0 depth card - - -"
                #         print "----------------"
                #         print "-----dept base response -------"
                #         url = returnCallForum(jsondata, details)
                #         print "^^^^^^^   ATTENDANCE ^^^^^^^^^"
                #         print url
                #         if details['depth'] == 1: ## complains here - probably attendance not defined above
                #             body = {"Title" : details['title'] , "Description" : details['cid'] }
                #         else:
                #             print " Attendance card at this level not allowed"
                #         method = "POST"
                #         print "=======The call forum =========="
                #         print url
                #         print body
                #         print method
                #         print "=======end call forum========="
                #         jsonreply = method_url(body, headers1, url, method)
                #         jsonreply = json.loads(jsonreply)
                #         # jsonreply = hit_url_method(body, headers1, method, url)
                #         print "======forum response ======="
                #         print jsonreply
                #
                #         # ###finalCards[details['cid']]['UID'] = jsonreply['cardid']
                #
                #     print "===========text card " + str(details['level']) + " ================="
                #     print cardID
                #     for element in jsondata['data']['elements']:
                #         # print element['cardtype']
                #         if 'webviewcard' in element['cardtype']:
                #             if details['title'] in element['title']:
                #                 cardexists = 0  ### change this to '1' finally
                #                 print " ============ CARD CREATION ERROR ================= "
                #                 print ("A card with this name already exists at this level")
                #     # if details['depth'] == 1 and cardexists == 0:
                #     body = {}
                #     print " - - - forum card - - -"
                #     print "----------------"
                #     print "-----dept base response -------"
                #     url = returnCallAttendance(jsondata, details)
                #     print "^^^^^^^   FORUM ^^^^^^^^^"
                #     print url
                ## uncomment till here
                else:
                    print "===========other card " + str(details['level']) + " ================="
                    print cardID
                    print details
print " -------- :):):):):):) ----------------"
print finalCards
print "+++++++++++++++++++++++++++++++++++++++"
print "+++++++++++++++++++++++++++++++++++++++"
print "+++++++++++++++++++++++++++++++++++++++"

print orderedCards
for i in range (0,len(orderedCards)):
    orderedCards[i]['title']
